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
    const pollJob = async (id, count = 0) => {
        const result = await fetch(`/v1/jobs/${id}`)
        const resultData = await result.json()
        if (resultData.status === "finished") {
            setRecipeName(resultData.recipeName)
            setRecipe(JSON.parse(resultData.recipe))
            setIngredients(JSON.parse(resultData.ingredients))
            setLoading(false)
            
            let imageStr = JSON.parse(resultData.image)
            const base64Response = await fetch(`data:image/jpeg;base64,${imageStr}`);
            const blob = await base64Response.blob();
            
            const newURL = URL.createObjectURL(blob);
            setImage(newURL)
        } else if (count > 10){
            return 'error'
        } else {
            setTimeout(() => {
                pollJob(id, count + 1)
        }, 5000)}
        return 'sucess'
    }



    const getResult = async () => {
        setLoading(true)
        const formData = new FormData();
        formData.append("image", inputImage);
        const requestOptions = { method: 'post', body: formData };
        let res = await fetch('/v1/generate-image', requestOptions);
        let data = await res.json();
        let id = data.job_id

        let pollRes = await pollJob(id)
        if (pollRes === 'error') {
            alert('Error processing image. Please try again.')
        }


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
                                return (<li key={ingredient}>
                                    <p>{ingredient}</p>
                                </li>)
                            })}
                        </ul>


                        <h2 className='text-3xl pb-3'>
                            Instructions
                        </h2>
                        <ul class='list-decimal pl-5 text-black'>
                            {recipe.map((step) => {
                                return (<li key={step}>
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