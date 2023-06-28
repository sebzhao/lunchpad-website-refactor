'use client'
import Output from './Output.jsx'
import Uploader from './Uploader.jsx'
import { FaArrowRight } from 'react-icons/fa';

import React from 'react'
import { useState } from 'react'

const ModelInterface = () => {

    const [uploaded, setUploaded] = useState(false)
    const [imageFile, setImageFile] = useState(null)

    const isUploaded = () => {
        setUploaded(true);
    }

    return (
        <div className='flex flex-row justify-center items-center'>
            <div className='flex flex-col pr-5'>
                <h2>
                    Upload your image here:
                </h2>
                <Uploader onSubmit={isUploaded} setImageFile={setImageFile}/>
            </div>

            <FaArrowRight size={30}/>
            
            
            <div className='flex flex-col pl-5'>
                <h2>
                    Output image:
                </h2>
                <Output uploaded={uploaded} imageFile={imageFile}/>
                
            </div>

    </div>
    )
}

export default ModelInterface