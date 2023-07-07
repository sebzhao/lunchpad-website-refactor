'use client'
import Output from './Output.jsx'
import Uploader from './Uploader.jsx'
import { FaArrowRight } from 'react-icons/fa';

import outputcrepe from '../assets/outputcrepe.png'
import React from 'react'
import { useState } from 'react'
import { get } from 'http';

const ModelInterface = () => {

    const [uploaded, setUploaded] = useState(false)
    const [inputImage, setInputImage] = useState(null)
    const [image, setImage] = useState(outputcrepe)
    const [ingr, setIngredients] = useState([])
    const [recipe, setRecipe] = useState([])
    const [recipeName, setRecipeName] = useState("")
    const [loading, setLoading] = useState(false)

    // Fix some state issues with deleting.

    const getResult = async () => {
        setLoading(true)
        const formData = new FormData();
        formData.append("image", inputImage);
        const requestOptions = { method: 'post', body: formData };
        let res = await fetch('/v1/generate-image', requestOptions);
        let data = await res.json();
        for (var key in data) {
            console.log(key);
            console.log(data[key]);
        }
        setRecipeName(data.recipeName)
        setRecipe(data.recipe)
        setIngredients(data.ingredients)

        //const newImageFile = URL.createObjectURL(`data:image/jpeg;base64,${data.image}`);
        setLoading(false)
        //setImage(newImageFile);
    }

    const isUploaded = () => {
        setUploaded(true);
    }

    return (
        <div>
            <div className='flex flex-row justify-center items-center pb-24'>
                <div className='flex flex-col pr-5'>
                    <h2>
                        Upload your image here:
                    </h2>
                    <Uploader onSubmit={isUploaded} setImageFile={setInputImage} />
                </div>

                <FaArrowRight size={30} />


                <div className='flex flex-col pl-5'>
                    <h2>
                        Output image:
                    </h2>
                    <Output uploaded={uploaded} getResult={getResult} loading={loading} image={image} />

                </div>

            </div>


            <div className='flex justify-center'>
                {recipeName ?
                    <div className='flex flex-col justify-center bg-slate-200 p-5 rounded-2xl'>
                        {recipeName ? <div> <h1 className="text-4xl pb-3">{recipeName}</h1> </div> : null}

                        <h2 className='text-3xl pb-3'>
                            Ingredients
                        </h2>
                        <ul class='list-disc pl-5 pb-3'>
                            {ingr.map((ingredient) => {
                                return (<li>
                                    <p>{ingredient}</p>
                                </li>)
                            })}
                        </ul>


                        <h2 className='text-3xl pb-3'>
                            Instructions
                        </h2>
                        <ul class='list-decimal pl-5 text-black pb-3'>
                            {recipe.map((step) => {
                                return (<li>
                                    <p>{step}</p>
                                </li>)
                            })}
                        </ul>


                    </div> :
                    <div>
                        <h1 className="text-4xl pb-3">Run our model to get the recipe!</h1>
                    </div>}

            </div>


        </div>

    )
}

export default ModelInterface