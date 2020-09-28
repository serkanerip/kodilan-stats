import React, { useState, useEffect } from 'react';
import moment from "moment";
import './App.css';
import CityStats from './components/citystats/default';
import FrontendStats from './components/frontendstats/default';
import LangStats from './components/langstats/default';
import PositionStats from './components/positionstats/default';
import TagStats from './components/tagstats/default';
import TechStats from './components/techstats/default';
import MyResponsivePie from './components/langstatspie/default';
import MyChart from './components/barchart';

function App() {
  const [date, setDate] = useState({startDate: '1990-01-01', endDate: '2900-01-01'})
  const [langStats, setLangStats] = useState([])
  const [tagStats, setTagStats] = useState([])
  const [feStats, setFeStats] = useState([])
  const [webStats, setWebStats] = useState([])
  const backend = process.env.REACT_APP_API_URL || "http://localhost:5000"

  function fetchStat(params, stat, setter)
  {
    const apiURL = `${backend}/api/v1/stats/${stat}`
    fetch(`${apiURL + params}`)
        .then(res => res.json())
        .then(data => setter(data.data))
  }
  

    useEffect(() => {
        const params = date.startDate !== null ? 
            `?startDate=${date.startDate}&endDate=${date.endDate}`
            : ''

        fetchStat(params, 'lang', setLangStats)
        fetchStat(params, 'tag', setTagStats)
        fetchStat(params, 'frontend', setFeStats)
        fetchStat(params, 'web', setWebStats)
        fetchStat(params, 'position', () => {})
    }, [date])

  return (
    <div className="container-fluid">
      <div className="row welcome">
        <div className="col-12">
          <h1 className="text-center">
            <a href="https://kodilan.com/" style={{color:"#000"}}>
              <span style={{color:"#26ae61", fontWeight: 500}}>{'{'} </span>kod<span style={{color:"#26ae61", fontWeight: 500}}>, </span>ilan<span style={{color:"#26ae61", fontWeight: 500}}> {'}'}</span>
            </a> istatistikleri
          </h1>
        </div>
      </div>
      <div className="row stats">
        <div className="pie-chart-wrapper col-6">
          <MyResponsivePie data={langStats} title="Programlama Dilleri" />
        </div>
        <div className="pie-chart-wrapper col-6">
          <MyResponsivePie data={tagStats} title="Keywordler" />
        </div>
        <div className="pie-chart-wrapper col-6">
          <MyResponsivePie data={feStats} title="Frontend Teknolojiler" />
        </div>
        <div className="pie-chart-wrapper col-6">
          <MyResponsivePie data={webStats} title="Backend Frameworkler" />
        </div>
      </div>
    </div>
  );
}

export default App;
