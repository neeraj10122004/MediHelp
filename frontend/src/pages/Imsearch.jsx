import React from 'react'
import { Link, redirect } from 'react-router-dom';
import { Nav } from '../components/Nav';
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';
import { useState } from 'react';
import { useRef } from 'react';
import axios from 'axios';

export const Imsearch = () => {
  const [temp, settemp] = useState(false)
  const [data, setdata] = useState("")
  const [accuracy, setaccuracy] = useState("")
  const imgref = useRef(null)
  const navigate = useNavigate();
      useEffect(() => {
        if(localStorage.getItem('token')==null){
          navigate('/');
        }
      }, [])
  const uploadimg = async (e) => {
    const files = e.target.files;
    const data = new FormData();
    data.append('file', files[0]);
    


    const res = await axios.post('http://localhost:5000/skin', data, {
      headers: {
          'Content-Type': 'multipart/form-data', // Ensure the correct content type
      },
  });
    e.target.value="";
    const output = res.data;
    setaccuracy(output.confidence)
    setdata(output.disease)



  }
      
  return (

    <div>
        <Nav text={"Upload your Img"}/>
        <div className='flex justify-center items-end gap-10'>
            
           <input type="file" name="file" id="" onChange={uploadimg} />
            <h3>
              {data}
            </h3>
            <h3>
              {accuracy}
            </h3>
        </div>
        
    </div>
  )
}
