import React from 'react'
import { GoogleLogin } from '@react-oauth/google';
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';

export const Signin = () => {
  const navigate = useNavigate();
  useEffect(() => {
    if(localStorage.getItem('token')!=null){
      navigate('/home');
    }
  }, [])
  
  return (
    <div>
      
      <GoogleLogin
  onSuccess={credentialResponse => {
    console.log(credentialResponse);
    localStorage.setItem('token', credentialResponse.credential); 
    
  }}
  onError={() => {
    console.log('Login Failed');
  }}
/>

    </div>
  )
}
