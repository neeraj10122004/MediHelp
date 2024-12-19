import React, { useState } from 'react';
import axios from 'axios';
import { Sympmatrix } from './Sympmatrix';
import { Nav } from './Nav';
import { Link } from 'react-router-dom';
import { FaArrowLeft } from 'react-icons/fa';
import { Url } from './Url';

export const Gridstyle = () => {
  const [output, setOutput] = useState(false);
  const [url, setUrl] = useState([]);
  const [elements, setElements] = useState([]);
  const [matrix, setMatrix] = useState(
    Array.from({ length: 11 }, () => Array(12).fill(0))
  );
  const [ou, setOu] = useState('output');
  const name = 'Guest'; // Replace with actual logic for fetching user name
  const photo = null; // Replace with actual logic for fetching user photo

  const submit = async () => {
    try {
      const response = await axios.post(
        'https://5000-neeraj10122004-medihelp-44vvu9arfl4.ws-us117.gitpod.io/submit',
        { matrix }
      );
      console.log('Response from server:', response.data);
      setOu(response.data.predictions);
      setUrl(response.data.url || []);
      console.log(url)
      console.log(response.data.url)
      const newElements = response.data.url.map((item, index) => (
        <div key={index} >
        <div>
        <a href={item.Link}>{item.Title}</a>
        <p>{item.Link}</p>
        <div>
            {item.Snippet}
        </div>
    </div>
        </div>
      ));
      setElements(newElements);

      setOutput(true);
      setMatrix(Array.from({ length: 11 }, () => Array(12).fill(0)));
    } catch (error) {
      console.error('Error submitting the matrix:', error);
    }
  };

  return (
    <>
      {!output && <Nav text="Select your Symptoms " />}
      <div>
        {output ? (
          <>
            <div className="w-lvw h-lvh bg-white">
              <div className="flex items-center justify-between p-10">
                <div className="flex items-center justify-center gap-10">
                  <FaArrowLeft
                    size={30}
                    onClick={() => setOutput(false)}
                    className="text-black cursor-pointer"
                    aria-label="Go Back"
                  />
                </div>
                <div className="flex items-center justify-center gap-5">
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
              <div>
                <p>Output: {ou}</p>
              </div>
              <div>{elements}</div>
            </div>
          </>
        ) : (
          <>
            <Sympmatrix matrix={matrix} setMatrix={setMatrix} />
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

