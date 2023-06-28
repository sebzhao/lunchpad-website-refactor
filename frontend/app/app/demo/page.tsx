
import Uploader from '../components/Uploader.jsx'
import Output from '../components/Output.jsx'
import ModelInterface from '../components/ModelInterface.jsx'


export default function Home() {
  return (
    <div className='min-h-screen bg-slate-300'>
      <title>
        Demo
      </title>

      <h1 className='flex flex-row center-items justify-center p-28 text-4xl'>
        Try out our custom model! 
      </h1>

      
      <ModelInterface/>
    

      
    </div>
  )
}
