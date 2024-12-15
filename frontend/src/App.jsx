import { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Home } from './pages/Home';
import { About } from './pages/About';
import { Signin } from './pages/Signin';
import { Userpage } from './pages/Userpage';
import { Imsearch } from './pages/Imsearch';

function App() {

  return (
    <div>
      <Router>
        <Routes>
          <Route
            path="/home"
            element={<Home/>}
          />
          <Route
            path="/about"
            element={<About/>}
          />
          <Route path="/" element={<Signin />} />
          <Route
            path="/userpage"
            element={<Userpage/>}
          />
          <Route
            path="/imsearch"
            element={<Imsearch/>}
          />
        </Routes>
      </Router>
    </div>
  );
}

export default App;

