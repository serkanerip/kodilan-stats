import React, { useState, useEffect } from 'react';
import './App.css';
import Search from './components/Search';

function App() {
  const backend = process.env.REACT_APP_API_URL || "http://localhost:5000"

  function fetchStat(params, stat, setter) {
    const apiURL = `${backend}/api/v1/stats/${stat}`
    fetch(`${apiURL + params}`)
        .then(res => res.json())
        .then(data => setter(data.data))
  }
  return (
    <div className="container-fluid">
      <Search/>
    </div>
  );
}

export default App;
