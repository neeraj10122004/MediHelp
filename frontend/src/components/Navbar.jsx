import React from 'react';
import { Link, redirect } from 'react-router-dom';

export const Navbar = ({loc}) => {
  return (
    <div className="flex items-center justify-between p-10">
      <div className="flex items-center justify-center gap-10">
        <div>
          <img
            className="rounded-full"
            src=""// Replace with your icon path
            alt="icon"
            width="50"
            height="50"
          />
        </div>
        <div
          className={`rounded-full ${
            loc === "Home" ? "bg-gray-100 p-3" : ""
          }`}
        >
          <Link to="/home">Home</Link>
        </div>
        <div
          className={`rounded-full ${
            loc === "About" ? "bg-gray-100 p-3" : ""
          }`}
        >
          <Link to="/about">About</Link>
        </div>
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
