import Image from 'next/image'
import annabelle_website from '../assets/annabelle_website.jpg'
import jade_website from '../assets/jade_website.jpg'
import nikhil_website from '../assets/nikhil_website.jpg'
import rahul_website from '../assets/rahul_website.jpg'
import sebastian_website from '../assets/sebastian_website.jpg'
import tanush_website from '../assets/tanush_website.jpg'
import tony_website from '../assets/tony_website.jpg'

export default function Home() {
  return (
    <div className='min-h-screen bg-slate-300'>
      <title>
        Team
      </title>

      <h1 className='flex flex-row center-items justify-center p-28 text-4xl'>
        Meet our Team!
      </h1>

      <div className='grid grid-cols-3 bg-slate-300 mx-32 gap-y-14 font-bold pb-10'>
        <div className='flex flex-col justify-center items-center'>
          <div className='group h-fit w-fit rounded-full bg-black mb-3'>
              {/** Fixme in the future. Should add hover in linkedin. */}
              <Image src={annabelle_website} height={300} width={300} className='rounded-full border-solid border-white border-2 z-10' alt="picture of annabelle"></Image>
          </div>
          <div className='text-center'>
            Annabelle Park 
          </div>
        </div>


        <div className='flex flex-col justify-center items-center'>
          <Image src={jade_website} height={300} width={300} className='rounded-full mb-3 border-solid border-white border-2' alt="picture of jade"></Image>
          <div className='text-center'>
            Jade Wang
          </div>
        </div>

        <div className='flex flex-col justify-center items-center'>
          <Image src={nikhil_website} height={300} width={300} className='rounded-full mb-3 border-solit border-white border-2' alt="picture of nikhil"></Image>
          <div className='text-center'>
            Nikhil Pitta
          </div>
        </div>

        <div className='flex flex-col justify-center items-center'>
          <Image src={rahul_website} height={300} width={300} className='rounded-full mb-3 border-solit border-white border-2' alt="picture of rahul"></Image>
          <div className='text-center'>
            Rahul Vijay
          </div>
        </div>

        <div className='flex flex-col justify-center items-center'>
          <Image src={sebastian_website} height={300} width={300} className='rounded-full mb-3 border-solit border-white border-2' alt="picture of sebastian"></Image>
          <div className='text-center'>
            Sebastian Zhao
          </div>
        </div>

        <div className='flex flex-col justify-center items-center'>
          <Image src={tanush_website} height={300} width={300} className='rounded-full mb-3 border-solit border-white border-2' alt="picture of tanush"></Image>
          <div className='text-center'>
            Tanush Talati
          </div>
        </div>


        <div className='flex flex-col justify-center items-center'>
          <Image src={tony_website} height={300} width={300} className='rounded-full mb-3 border-solit border-white border-2' alt="picture of tony"></Image>
          <div className='text-center'>
            Tony Xin
          </div>
        </div>

      </div>
    </div>
  )
}
