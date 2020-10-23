import React from 'react';
import './App.css';

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
      <p>A</p>
    </div>
  );
}

export default App;
