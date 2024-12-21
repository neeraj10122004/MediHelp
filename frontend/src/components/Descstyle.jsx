import React, { useState } from 'react';
import axios from 'axios';
import { Nav } from './Nav';
import { Link } from 'react-router-dom';
import { FaArrowLeft } from 'react-icons/fa';

export const Descstyle = () => {
  const [textinput, setTextInput] = useState("");
  const [output, setOutput] = useState(false);
  const [url, setUrl] = useState([]);
  const [elements, setElements] = useState([]);
  const [llmresp, setLlmresp] = useState("None");
  const [ou, setOu] = useState('output');
  const name = 'Guest'; // Replace with actual logic for fetching user name
  const photo = null; // Replace with actual logic for fetching user photo

  const submit = async () => {
    try {
      const response = await axios.post(
        'https://5000-neeraj10122004-medihelp-44vvu9arfl4.ws-us117.gitpod.io/submit2',
        { textinput }
      );

      console.log('Response from server:', response.data);
      
      setOu(response.data.predictions || 'output');
      setLlmresp(response.data.llm || "none");
      setUrl(response.data.url || []);
      
      console.log(url);
      console.log(response.data.url);

      const newElements = response.data.url.map((item, index) => (
        <div key={index} className='flex flex-col bg-white p-4 rounded-md gap-1'>
          <div className="flex flex-col gap-4 p-4 rounded-lg shadow-lg bg-slate-200 hover:bg-slate-300 transition duration-200">
            <div className="text-lg font-semibold text-blue-600 hover:underline">
              <a href={item.Link} target="_blank" rel="noopener noreferrer">{item.Title}</a>
            </div>
            <a href={item.Link} className="text-sm text-gray-500 break-words">{item.Link}</a>
            <div className="text-gray-700">
              {item.Snippet}
            </div>
          </div>
        </div>
      ));
      setElements(newElements);

      setOutput(true);
    } catch (error) {
      console.error('Error submitting the matrix:', error);
    }
  };

  return (
    <>
      {!output && <Nav text="Describe your Symptoms " />}
      <div>
        {output ? (
          <>
            <div className="bg-white fixed top-0 left-0 w-full shadow-md z-50">
              <div className="flex items-center justify-between p-5">
                <div className="flex items-center gap-10">
                  <FaArrowLeft
                    size={30}
                    onClick={() => setOutput(false)}
                    className="text-black cursor-pointer"
                    aria-label="Go Back"
                  />
                </div>
                <div className="flex flex-col bg-white p-4 rounded-md gap-1">
                  <div className="flex flex-col gap-4 p-4 rounded-lg shadow-lg bg-gradient-to-r from-blue-100 to-blue-300 hover:bg-slate-300 transition duration-200">
                    {ou}
                  </div>
                </div>
                <div className="flex items-center gap-5">
                  <div>{name}</div>
                  <div className="rounded-full">
                    <Link to="/userpage">
                      <img
                        src={photo || '/default-avatar.png'}
                        alt={name || 'User'}
                        className="rounded-full"
                        width="50"
                        height="50"
                      />
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          
            {/* Add padding to prevent content overlap */}
            <div className="pt-32 h-screen">
              <div className="flex flex-row h-full">
                {/* Left panel - scrollable */}
                <div className="flex-1 overflow-y-auto h-full">
                  {elements}
                </div>
                
                {/* Right panel - fixed */}
                <div className="w-1/2 h-full flex flex-col gap-4 p-4 ">
                  <div className='rounded-lg p-3 shadow-lg bg-slate-200 hover:bg-slate-300 transition duration-200'>
                    {llmresp}
                  </div>
                </div>
              </div>
            </div>
          </>
        ) : (
          <>
            <input 
              type="text" 
              placeholder='Describe your symptoms' 
              value={textinput} 
              onChange={(e) => setTextInput(e.target.value)} 
            />
            <div
              className="p-2 fixed w-58 break-words border bottom-10 right-10 bg-orange-300 cursor-pointer shadow-lg rounded-md flex justify-center items-center"
              onClick={submit}
            >
              <div className="text-white">Submit</div>
            </div>
          </>
        )}
      </div>
    </>
  );
};


