'use client'
import Image from 'next/image'
import Typewriter from 'typewriter-effect'
import lunchpadLogo from './assets/lunchpad-logo.png'

export default function Home() {
  return (
    <div className='h-screen bg-slate-300'>
      <title>
        Home
      </title>

      <div className='flex flex-row text-4xl justify-center items-center py-36'>
        <Typewriter onInit={(typewriter) => {
            typewriter
              .changeDelay(50)
              .typeString('Welcome to Lunchpad, a project that uses AI to make boring food fancy!')
                .callFunction(() => {
                  console.log('String typed out!');
                })
              .start();
          }}
        />
      </div>

      <div className='flex flex-row content-start justify-items-center justify-center'>
        <div className='rounded-full h-96 w-96 bg-slate-100 flex flex-row justify-center items-center self-start shadow-lg' >
          <Image src={lunchpadLogo} width={240} height={240} alt="lunchpad logo"/>
        </div>
        
      </div>
    </div>
  )
}
