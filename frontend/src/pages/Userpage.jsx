import React from 'react'
import { Navbar } from '../components/Navbar'
import { FaCamera } from 'react-icons/fa'
import { Link, redirect } from 'react-router-dom';
import { FaExclamationTriangle } from "react-icons/fa";
import { FaCommentMedical } from "react-icons/fa";
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';

export const Userpage = () => {
  const navigate = useNavigate();
      useEffect(() => {
        if(localStorage.getItem('token')==null){
          navigate('/');
        }
      }, [])
  return (
    <div>
        <Navbar loc="Usepage"/>

        <div
        className="p-4 fixed w-14 h-14 bottom-10 right-10 bg-slate-600 text-white hover:bg-slate-700 cursor-pointer shadow-lg rounded-full flex justify-center items-center"

      >
         <Link to="/imsearch"> <FaCamera size={30} className="text-white" /> </Link>
      </div>
      <div className="p-4 fixed w-14 h-14 bottom-28 right-10 bg-slate-600 text-white hover:bg-slate-700 cursor-pointer shadow-lg rounded-full flex justify-center items-center">
        <Link to="/imsearch"> <FaCommentMedical size={30} className="text-white" /> </Link>
      </div>
      <div className="p-4 fixed w-58 break-words border bottom-10 left-10 bg-orange-100 cursor-pointer shadow-lg rounded-md flex justify-center items-center">
          <FaExclamationTriangle size={25}/>
      <div className=' pl-5 text-red-500 '>Disclaimer: MediHelp results are preliminary and should not replace professional medical advice. Always consult a doctor for accurate diagnosis and treatment.</div>
      </div>
    </div>
  )
}
