'use client'
import Image from 'next/image'
import { useState } from 'react'
import outputcrepe from '../assets/outputcrepe.png'

export default function Output({uploaded, imageFile}) {
  const [image, setImage] = useState(outputcrepe)

  const getResult = async () => {
    // const formData = new FormData();
    // formData.append("image", imageFile); 
    // const requestOptions = {method: 'post', body: formData};
    // let res = await fetch('/v1/generateImage', requestOptions);
    // let data = await res.json();
    // setImage(data.image);
    alert("Unfortunately this requires too much compute to host and I don't have root privileges on the free compute server I have access to. Check the repo if interested on implementation.")
  }
  
  return (
    <main>

      <div className='relative flex justify-center items-center border-2 border-dashed h-72 w-96 cursor-pointer rounded-2xl'>


        {uploaded ?
          null : <Image src={image} fill alt="output file" style={{'objectFit': 'cover'}} className='rounded-2xl'/>
        }
        

      </div>

      <section className='uploaded-row mt-3 p-2 flex justify-center items-center rounded-lg bg-blue-100'>
            <button type="button" className='bg-slate-50 p-2 rounded-xl border-2 border-black hover:bg-blue-200' onClick={getResult}>
                Generate new image!
            </button>
      </section>

    </main>
  )
}
