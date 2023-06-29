// components/Navbar.tsx
'use client'
import Link from "next/link";


const Navbar = () => {
  return (
    <div className="flex flex-row justify-between items-center bg-gray-600 shadow-2xl">
        <h1 className='px-5 py-3 text-2xl text-white'>
            Lunchpad
        </h1>

        <div className='flex flex-row items-center m-3'>
            
            <Link href="/" passHref>
                <div className='px-5 py-3 bg-gray-100 rounded-lg'>Home</div>
            </Link>
            
        
            
            <Link href="/team" passHref>
                <div className='px-5 py-3 bg-gray-100 rounded-lg ml-3'>Team</div>
            </Link>


            <Link href="/demo">
                <div className='px-5 py-3 bg-gray-100 rounded-lg ml-3'>Demo</div>
            </Link>


            {/* <Link href="/research">
                <div className='px-5 py-3 bg-gray-100 rounded-lg ml-3'>Research</div>
            </Link> */}
        </div>
    </div>
  );
};
export default Navbar;
