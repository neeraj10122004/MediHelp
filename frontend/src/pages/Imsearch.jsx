import React from 'react'
import { Link, redirect } from 'react-router-dom';
import { Nav } from '../components/Nav';
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';

export const Imsearch = () => {
  const navigate = useNavigate();
      useEffect(() => {
        if(localStorage.getItem('token')==null){
          navigate('/');
        }
      }, [])
  return (

    <div>
        <Nav text={"Upload your Img"}/>
        <div className='flex justify-center items-end gap-10'>
            <div className='w-100 bg-black text-white'>
            di
            </div>

            <div classname='w-100 bg-black text-white'>
            hijhi
            </div>
        </div>
        
    </div>
  )
}
