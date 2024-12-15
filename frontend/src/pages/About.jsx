import React, { useState } from 'react';
import { Navbar } from '../components/Navbar';
import { Footer } from '../components/Footer';
import { FaCamera } from 'react-icons/fa';
import { Link, redirect } from 'react-router-dom';

export const About = () => {

  return (
    <div>
      <Navbar loc="About"/>

      <div className="flex flex-col items-center justify-center text-center p-6 h-full">
        <h1 className="text-3xl font-extrabold text-gray-800 mb-4">
          MediHelp
        </h1>
        <p className="text-lg text-gray-700 max-w-3xl mx-auto mb-6">
          MediHelp is your trusted companion for all your health-related needs. Whether you're looking for medical advice, tracking symptoms, or seeking expert consultations, MediHelp connects you with healthcare professionals to ensure you're getting the best care possible.
        </p>
        <p className="text-lg text-gray-600 mb-8">
          Our platform is designed to provide you with reliable health information, tips, and resources to manage your well-being. Share your experiences, get advice, and stay informed to make empowered decisions about your health.
        </p>
      </div>
      
      <Footer/>
    </div>
  );
};
