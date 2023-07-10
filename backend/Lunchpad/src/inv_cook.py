import argparse
import base64
import io
import os
import pickle
import time
from argparse import Namespace
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import pkg_resources
import ray
import torch
import torch.nn as nn
from diffusers import StableDiffusionImg2ImgPipeline
from Lunchpad.data import DATA_DIR
from Lunchpad.src.model import get_model
from Lunchpad.src.utils.output_utils import prepare_output
from PIL import Image
from ray import serve
from torchvision import transforms

# FIXME: Set up argparser + arguments


@serve.deployment
class InvCookModel:
    def __init__(self):
        self.greedy = True  # Changed first True to False for non-greddy generations.
        self.beam = -1
        self.temperature = 1.0
        use_gpu = True  # running on gpu or cpu
        device = torch.device("cuda" if torch.cuda.is_available() and use_gpu else "cpu")
        map_loc = None if torch.cuda.is_available() and use_gpu else "cpu"

        self.ingrs_vocab = pickle.load(open(os.path.join(DATA_DIR, "ingr_vocab.pkl"), "rb"))
        self.vocab = pickle.load(open(os.path.join(DATA_DIR, "instr_vocab.pkl"), "rb"))

        ingr_vocab_size = len(self.ingrs_vocab)
        instrs_vocab_size = len(self.vocab)

        # Hardcoded args
        args = Namespace(
            aux_data_dir="../data",
            batch_size=128,
            beam=-1,
            crop_size=224,
            decay_lr=True,
            dropout_decoder_i=0.3,
            dropout_decoder_r=0.3,
            dropout_encoder=0.3,
            embed_size=512,
            es_metric="loss",
            eval_split="val",
            finetune_after=-1,
            get_perplexity=False,
            greedy=False,
            image_model="resnet50",
            image_size=256,
            ingrs_only=True,
            label_smoothing_ingr=0.1,
            learning_rate=0.001,
            log_step=10,
            log_term=False,
            loss_weight=[1.0, 0.0, 0.0, 0.0],
            lr_decay_every=1,
            lr_decay_rate=0.99,
            max_eval=4096,
            maxnumims=5,
            maxnuminstrs=10,
            maxnumlabels=20,
            maxseqlen=15,
            model_name="model",
            n_att=8,
            n_att_ingrs=4,
            num_epochs=400,
            num_workers=8,
            numgens=3,
            patience=50,
            project_name="inversecooking",
            recipe1m_dir="path/to/recipe1m",
            recipe_only=False,
            resume=False,
            save_dir="path/to/save/models",
            scale_learning_rate_cnn=0.01,
            suff="",
            temperature=1.0,
            tensorboard=True,
            transf_layers=16,
            transf_layers_ingrs=4,
            transfer_from="",
            use_lmdb=True,
            use_true_ingrs=False,
            weight_decay=0.0,
        )
        args.maxseqlen = 15
        args.ingrs_only = False
        model = get_model(args, ingr_vocab_size, instrs_vocab_size)
        # Load the trained model parameters
        model_path = os.path.join(DATA_DIR, "modelbest.ckpt")
        model.load_state_dict(torch.load(model_path, map_location=map_loc))
        model.to(device)
        model.eval()
        model.ingrs_only = False
        model.recipe_only = False
        self.model = model

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.device = device
        # inputted image path

        transf_list_batch = []  # variables
        transf_list_batch.append(transforms.ToTensor())
        transf_list_batch.append(transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)))
        to_input_transf = transforms.Compose(transf_list_batch)
        self.to_input_transf = to_input_transf

        transf_list = []
        transf_list.append(transforms.Resize(256))
        transf_list.append(transforms.CenterCrop(224))
        transform = transforms.Compose(transf_list)
        self.transform = transform

    def inverse_cook(self, image: bytes, true_ingrs=None, recipe_only=False):
        image_tensor = self.to_input_transf(self.transform(image)).unsqueeze(0).to(self.device)

        true_ingrs = true_ingrs.to(self.device) if not true_ingrs is None else true_ingrs
        self.recipe_only = recipe_only
        with torch.no_grad():
            outputs = self.model.sample(
                image_tensor, greedy=self.greedy, temperature=self.temperature, beam=self.beam, true_ingrs=true_ingrs
            )

        ingr_tensor = outputs["ingr_ids"].cpu()
        ingr_ids = outputs["ingr_ids"].cpu().numpy()
        recipe_ids = outputs["recipe_ids"].cpu().numpy()

        outs, valid = prepare_output(recipe_ids[0], ingr_ids[0], self.ingrs_vocab, self.vocab)

        recipe_name = outs["title"]
        recipe = outs["recipe"]
        ingredients = outs["ingrs"]  # ingredient list
        return recipe_name, recipe, ingredients, ingr_tensor


@serve.deployment
class StableDiffusionModel:
    def __init__(self):
        return
        model_id_or_path = "runwayml/stable-diffusion-v1-5"
        self.pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id_or_path, torch_dtype=torch.float16).to(
            "cuda"
        )

    def generate_image(self, image: bytes, prompt: str):
        image = Image.open("Lunchpad/data/demo_imgs/Creamy-Spinach-Tomato-Pasta-bowl-500x500.jpeg")
        return image
        maxsize = 768
        othersize = int(maxsize * (image.size[1] / image.size[0]))
        image = image.resize((maxsize, othersize))
        images = self.pipe(prompt=prompt, image=image, strength=0.8, guidance_scale=7.5).images
        new_image = images[0]

        return new_image


@serve.deployment
class LunchpadModel:
    def __init__(self, inv_cook_model, stable_diffusion_model):
        self.inv_cook_model = inv_cook_model
        self.stable_diffusion_model = stable_diffusion_model

    async def custom_inference(self, image: bytes):
        # FIXME: Run model inference on original image
        ref = await self.inv_cook_model.inverse_cook.remote(image, true_ingrs=None)
        recipe_name, _, ingredients, ingr_ids = await ref

        prompt = "Fancy food plating of " + recipe_name
        print(prompt)
        # Generate new image
        ref = await self.stable_diffusion_model.generate_image.remote(image, prompt)
        new_image = await ref

        buffered = BytesIO()
        new_image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        # Run through final pass.
        ref = await self.inv_cook_model.inverse_cook.remote(new_image, true_ingrs=ingr_ids, recipe_only=True)

        _, recipe, _, _ = await ref

        # FIXME: Save this into a file that can be retrieved now.
        return recipe_name, recipe, ingredients, img_str


bound_lunchpad_model = LunchpadModel.bind(InvCookModel.bind(), StableDiffusionModel.bind())
