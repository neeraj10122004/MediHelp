import React from 'react';
import { Link, redirect } from 'react-router-dom';
import { FaArrowLeft } from 'react-icons/fa';

export const Nav = ({text,loc}) => {
  return (
    <div className="flex items-center justify-between p-10">
      <div className="flex items-center justify-center gap-10">
        <Link to="/home"> <FaArrowLeft size={30} className="text-black" /> </Link>
      </div>
      <div>
        {text}
      </div>
      <div className="flex items-center justify-center gap-5">
        <div>{name || "Guest"}</div>
        <div
          className={`rounded-full ${
            loc === "Userpage" ? "bg-gray-100 p-3" : ""
          }`}
        >
          <Link to="/userpage">
            <img
              src={"photo" || "/default-avatar.png"}
              alt={"name" || "User"}
              className="rounded-full"
              width="50"
              height="50"
            />
          </Link>
        </div>
      </div>
    </div>
  );
};