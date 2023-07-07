'use client'
import Image from 'next/image'
import { useState } from 'react'
import { MdCloudUpload, MdDelete } from 'react-icons/md'
import { AiFillFileImage } from 'react-icons/ai'
import crepe from '../assets/crepe.jpg'

export default function Uploader({ onSubmit, setImageFile }) {

  const [image, setImage] = useState(crepe)
  const [fileName, setFileName] = useState("No selected file")

  const clearFiles = (event) => {
    event.target.value = ''
  }



  return (
    <main>
      <form className='relative flex justify-center items-center border-2 border-dashed h-72 w-96 cursor-pointer rounded-2xl'
        onClick={() => document.querySelector(".input-field").click()}
      >
        <input type="file" accept='image/*' className='input-field' hidden onClick={clearFiles}
          onChange={({ target: { files } }) => {
            files[0] && setFileName(files[0].name)
            if (files[0]) {
              console.log(files[0])
              setImage(URL.createObjectURL(files[0]))
              setImageFile(files[0])
            }
            files = ""
            onSubmit()

          }}
        />

        {image !== null && image !== crepe &&
          <Image src={image} fill alt={fileName} style={{ 'objectFit': 'cover' }} className='rounded-2xl' />
        }
        {image == crepe &&
          <>
            <Image src={image} fill alt={fileName} style={{ 'objectFit': 'cover' }} className='rounded-2xl opacity-50' />
            <MdCloudUpload color='#1475cf' size={60} className='pr-2 z-50' />
            <p className='z-50'>Browse Files to upload</p>
          </>
        }
        {image == null &&
          <>
            <MdCloudUpload color='#1475cf' size={60} className='pr-2 z-50' />
            <p className='z-50'>Browse Files to upload</p>
          </>
        }

      </form>

      <section className='uploaded-row mt-3 p-5 w-96 flex justify-between items-center rounded-lg bg-blue-100'>
        <AiFillFileImage color='#1475cf' />
        <span className='upload-content flex justify-end items-center'>
          <p className='whitespace-nowrap text-clip overflow-hidden w-60 text-right pr-1'>{fileName}</p>
          -
          <MdDelete
            onClick={() => {
              setFileName("No selected File")
              setImage(null)
              setImageFile(null)
            }} className='pl-1 hover:cursor-pointer'

          />
        </span>
      </section>

    </main>
  )
}
