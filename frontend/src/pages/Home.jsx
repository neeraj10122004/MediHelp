import React from 'react'
import { Navbar } from '../components/Navbar'
import { FaCamera } from 'react-icons/fa'
import { Link, redirect } from 'react-router-dom';
import { Sympmatrix } from '../components/Sympmatrix';
export const Home = () => {
  return (
    <div>
        <Navbar loc="Home"/>
        <Sympmatrix/>
        <div
        className="p-4 fixed w-14 h-14 bottom-10 right-10 bg-slate-600 text-white hover:bg-slate-700 cursor-pointer shadow-lg rounded-full flex justify-center items-center"

      >
         <Link to="/imsearch"> <FaCamera size={30} className="text-white" /> </Link>
      </div>
    </div>
  )
}
