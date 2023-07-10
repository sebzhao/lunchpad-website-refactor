'use client'
import Image from 'next/image'
import { useState } from 'react'
import outputcrepe from '../assets/outputcrepe.png'
import { ThreeCircles } from 'react-loader-spinner'

export default function Output({ uploaded, getResult, loading, image }) {


  return (
    <main>

      <div className='relative flex justify-center items-center border-2 border-dashed h-72 w-96 cursor-pointer rounded-2xl'>


        {loading && uploaded ?
          null : <Image src={image} fill alt="output file" style={{ 'objectFit': 'cover' }} className='rounded-2xl' />
        }
        {
          loading ? <ThreeCircles
            height="100"
            width="100"
            color="#4fa94d"
            wrapperStyle={{}}
            wrapperClass=""
            visible={true}
            ariaLabel="three-circles-rotating"
            outerCircleColor=""
            innerCircleColor=""
            middleCircleColor=""
          /> : null
        }


      </div>

      <section className='uploaded-row mt-3 p-2 flex justify-center items-center rounded-lg bg-blue-100'>
        <button type="button" className='bg-slate-50 p-2 rounded-xl border-2 border-black hover:bg-blue-200' onClick={getResult}>
          Generate new image and it&apos;s recipe!
        </button>
      </section>





    </main>
  )
}
