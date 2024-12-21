import React from 'react'
import { GoogleLogin } from '@react-oauth/google';
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';
import { jwtDecode } from "jwt-decode";

export const Signin = () => {
  const navigate = useNavigate();
  
  useEffect(() => {
    if(localStorage.getItem('token')!=null){
      const data = jwtDecode(localStorage.getItem('token'));
      localStorage.setItem('data',JSON.stringify(data));
      console.log(data)
      console.log(localStorage.getItem('data'))
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
