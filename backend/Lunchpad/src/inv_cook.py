import argparse
import io
import os
import pickle
import time
from argparse import Namespace

import matplotlib.pyplot as plt
import numpy as np
import pkg_resources
import torch
import torch.nn as nn
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image
from torchvision import transforms

from Lunchpad.data import DATA_DIR
from Lunchpad.src.model import get_model
from Lunchpad.src.utils.output_utils import prepare_output

# FIXME: Set up argparser + arguments


async def inv_cook(model, image_tensor, greedy, temperature, beam, true_ingrs, ingrs_vocab, vocab):
    with torch.no_grad():
        outputs = model.sample(image_tensor, greedy=greedy, temperature=temperature, beam=beam, true_ingrs=true_ingrs)

    ingr_ids = outputs["ingr_ids"].cpu().numpy()
    recipe_ids = outputs["recipe_ids"].cpu().numpy()

    outs, valid = prepare_output(recipe_ids[0], ingr_ids[0], ingrs_vocab, vocab)

    recipe_name = outs["title"]
    recipe = outs["recipe"]
    ingredients = outs["ingrs"]  # ingredient list
    return recipe_name, recipe, ingredients


async def image_gen(prompt, image):
    model_id_or_path = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id_or_path, torch_dtype=torch.float16).to("cuda")
    images = pipe(prompt=prompt, image=image, strength=0.8, guidance_scale=7.5).images
    new_image = images[0]

    return new_image


async def custom_inference(image: bytes):
    use_gpu = True  # running on gpu or cpu
    device = torch.device("cuda" if torch.cuda.is_available() and use_gpu else "cpu")
    map_loc = None if torch.cuda.is_available() and use_gpu else "cpu"

    ingrs_vocab = pickle.load(open(os.path.join(DATA_DIR, "ingr_vocab.pkl"), "rb"))
    vocab = pickle.load(open(os.path.join(DATA_DIR, "instr_vocab.pkl"), "rb"))

    ingr_vocab_size = len(ingrs_vocab)
    instrs_vocab_size = len(vocab)

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

    # inputted image path
    image = Image.open(io.BytesIO(image)).convert("RGB")  # image
    print("Made an image")

    transf_list_batch = []  # variables
    transf_list_batch.append(transforms.ToTensor())
    transf_list_batch.append(transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)))
    to_input_transf = transforms.Compose(transf_list_batch)

    greedy = True  # Changed first True to False for non-greddy generations.
    beam = -1
    temperature = 1.0

    transf_list = []
    transf_list.append(transforms.Resize(256))
    transf_list.append(transforms.CenterCrop(224))
    transform = transforms.Compose(transf_list)

    image_transf = transform(image)
    image_tensor = to_input_transf(image_transf).unsqueeze(0).to(device)

    # FIXME: Run model inference on original image

    recipe_name, _, ingredients = await inv_cook(
        model, image_tensor, greedy, temperature, beam, None, ingrs_vocab, vocab
    )

    ingredients = ", ".join(ingredients)
    prompt = "Fancy food plating of " + recipe_name
    print(prompt)

    # Generate new image

    new_image = await image_gen(prompt, image)
    new_image_transf = transform(new_image)
    new_image_tensor = to_input_transf(new_image_transf).unsqueeze(0).to(device)

    # Run through final pass.

    _, recipe, _ = await inv_cook(model, new_image_tensor, greedy, temperature, beam, ingredients, ingrs_vocab, vocab)

    # FIXME: JSONify and make a proper response.

    return recipe_name, recipe, ingredients, new_image
