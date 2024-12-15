import React from "react";
import { FaFacebookF, FaTwitter, FaInstagram, FaLinkedin } from "react-icons/fa";

export const Footer = () => {
  return (
    <footer className="bg-gray-100 text-black py-8">
      <div className="container mx-auto px-4">
        {/* Top Section */}
        <div className="flex flex-wrap justify-between items-center">
          {/* Brand Name or Logo */}
          
          <div className="mb-4 md:mb-0">
            <h1 className="text-2xl font-bold">MediHelp</h1>
          </div>

          {/* Navigation Links */}
          <nav className="flex space-x-6">
            <a href="#services" className="hover:underline">
              Services
            </a>
            <a href="#blog" className="hover:underline">
              Blog
            </a>
            <a href="#contact" className="hover:underline">
              Contact
            </a>
          </nav>
        </div>

        {/* Divider */}
        <hr className="my-6 border-gray-700" />

        {/* Middle Section */}
        <div className="flex flex-wrap justify-between items-center">
          {/* Contact Information */}
          <div className="mb-4 md:mb-0">
            <p className="text-sm">Phone: +91 9492995001 | +91 9515621780</p>
            <p className="text-sm">Email: support@MediHelp.com</p>
            <p className="text-sm">Address: Gurgon,Mumbai</p>
          </div>

          {/* Social Media Links */}
          <div className="flex space-x-4">
            <a
              href="https://facebook.com"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-blue-500"
            >
              <FaFacebookF />
            </a>
            <a
              href="https://twitter.com"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-blue-400"
            >
              <FaTwitter />
            </a>
            <a
              href="https://instagram.com"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-pink-500"
            >
               <FaInstagram />
            </a>
            <a
              href="https://linkedin.com"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-blue-600"
            >
              <FaLinkedin />
            </a>
          </div>
        </div>

        {/* Divider */}
        <hr className="my-6 border-gray-700" />

        {/* Bottom Section */}
        <div className="text-center text-sm">
          <p>&copy; {new Date().getFullYear()} AcrossIndia. All Rights Reserved.</p>
        </div>
      </div>
    </footer>
  );
};