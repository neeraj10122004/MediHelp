import React from 'react'
import { GoogleLogin } from '@react-oauth/google';
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';
import { jwtDecode } from "jwt-decode";
import axios from 'axios';

export const Signin =  () => {
  const navigate = useNavigate();
  const check_create_user = async () =>{
    try {
      console.log('check create user')
      console.log(JSON.parse(localStorage.getItem('data')).sub)
      const response = await axios.post(
        'http://localhost:5000//create_verify_user',
        { googleid : JSON.parse(localStorage.getItem('data')).sub }
      );
      
    } catch (error) {
      console.error('Error', error);
    }
  }
  
  useEffect(() => {
    if(localStorage.getItem('token')!=null){
      const data = jwtDecode(localStorage.getItem('token'));
      localStorage.setItem('data',JSON.stringify(data));
      console.log(data)
      console.log(localStorage.getItem('data'))
      check_create_user()
      navigate('/home');
    }
  }, [])
  
  return (
    <div className='flex-row justify-center items-center align-middle'>
      
      <GoogleLogin
  onSuccess={ credentialResponse => {
    console.log(credentialResponse);
    localStorage.setItem('token', credentialResponse.credential);
    const data = jwtDecode(localStorage.getItem('token'));
    localStorage.setItem('data',JSON.stringify(data));
    console.log(data)
    console.log(localStorage.getItem('data'))
    check_create_user();
    navigate('/home');
    
  }}
  onError={() => {
    console.log('Login Failed');
  }}
/>

    </div>
  )
}
