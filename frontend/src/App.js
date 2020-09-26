import React, { useState } from 'react';
import './App.css';
import CityStats from './components/citystats/default';
import FrontendStats from './components/frontendstats/default';
import LangStats from './components/langstats/default';
import PositionStats from './components/positionstats/default';
import TagStats from './components/tagstats/default';
import TechStats from './components/techstats/default';

function App() {
  const [date, setDate] = useState({startDate: null, endDate: null})
  const backend = process.env.apiurl || "http://localhost:5000"

  function changeDate(period){
    if (period === "all") {
      setDate({
        startDate: '1990-01-01',
        endDate: '2900-01-01'
      })
    }
  }

  return (
    <div className="container-fluid">
      <div className="row" style={{background: "#333", color: '#fff', height: "100vh", justifyContent: "center", alignContent: 'center', alignItems: "center"}}>
        <div className="col-12">
          <h1 className="text-center">
          <a href="https://kodilan.com/" style={{color:"#fff"}}>
            <span style={{color:"#26ae61", fontWeight: 500}}>{'{'} </span>kod<span style={{color:"#26ae61", fontWeight: 500}}>, </span>ilan<span style={{color:"#26ae61", fontWeight: 500}}> {'}'}</span>
            </a> istatistikleri
          </h1>
          <h6 className="text-center text-muted">Bu veriler sadece bu yıla ait olan ilanlara aittir.</h6>
        </div>
        <div className="col-12 mb-5">
          <button onClick={() => changeDate('all')} className="mr-2 btn btn-primary">Tüm Kayıtlar</button>
          <button className="mr-2 btn btn-primary">Bu Yıl</button>
          <button className="mr-2 btn btn-primary">Bu Ay</button>
          <button className="mr-2 btn btn-primary">Bu Hafta</button>
        </div>
        <div className="col-4">
          <CityStats backend={backend} date={date}/>
        </div>
        <div className="col-4">
          <PositionStats backend={backend} date={date}/>
        </div>
        <div className="col-4">
          <TagStats backend={backend} date={date}/>
        </div>
        <div className="col-4">
          <LangStats backend={backend} date={date}/>
        </div>
        <div className="col-4">
          <TechStats backend={backend} date={date}/>
        </div>
        <div className="col-4">
          <FrontendStats backend={backend} date={date}/>
        </div>
      </div>
    </div>
  );
}

export default App;
