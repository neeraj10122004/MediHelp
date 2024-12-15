import React from 'react';
import { FaExclamationTriangle } from "react-icons/fa";

export const Select = ({ selec, setselec, desc, setdesc }) => {
    const clickDescription = () => {
        setdesc(true);  // Set to show the description
        setselec(false); // Hide the Select component
    };

    const clickGrid = () => {
        setdesc(false); // Set to show the grid box
        setselec(false); // Hide the Select component
    };

    return (
        <div className='w-lvw h-lvh flex justify-center items-center gap-20 '>
            {/* Empty div with text, explaining Description usage */}
            <div className='bg-slate-600 p-4 rounded-md text-white text-center'>
                <p>For simplicity</p>
                <p>Use Description</p>
                <p>for basic information</p>
            </div>
            <div className='flex gap-52'>
            {/* Button for Description */}
            <div className='bg-red-500 p-2 rounded-md text-white cursor-pointer' onClick={clickDescription}>
                Description
            </div>

            {/* Button for Gridbox */}
            <div className='bg-red-500 p-2 rounded-md text-white cursor-pointer' onClick={clickGrid}>
                Selection panel
            </div>
            </div>
            {/* Empty div with text, explaining Grid usage */}
            <div className='bg-slate-600 p-4 rounded-md text-white text-center'>
                <p>For more accurate answers</p>
                <p>Use Grid</p>
                <p>for detailed options</p>
            </div>
            <div
        className="p-4 fixed w-58 break-words border bottom-10 left-10 bg-orange-100 cursor-pointer shadow-lg rounded-md flex justify-center items-center"

      >
        <FaExclamationTriangle size={25}/>
        <div className=' pl-5 text-red-500 '>Disclaimer: MediHelp results are preliminary and should not replace professional medical advice. Always consult a doctor for accurate diagnosis and treatment.</div>
      </div>
        </div>
    );
};
