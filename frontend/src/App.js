import React, { useState } from 'react';
import moment from "moment";
import './App.css';
import CityStats from './components/citystats/default';
import FrontendStats from './components/frontendstats/default';
import LangStats from './components/langstats/default';
import PositionStats from './components/positionstats/default';
import TagStats from './components/tagstats/default';
import TechStats from './components/techstats/default';

function App() {
  const [date, setDate] = useState({startDate: null, endDate: null})
  const backend = process.env.REACT_APP_API_URL || "http://localhost:5000"

  function changeDate(period){
    if (period === "all") {
      setDate({
        startDate: '1990-01-01',
        endDate: '2900-01-01'
      })
    }
    if (period === 'year') {
      var year = new Date().getFullYear();
      setDate({
        startDate: moment().startOf('year').format('YYYY-MM-DD'),
        endDate: moment().endOf('year').format('YYYY-MM-DD'),
      })
    }
    if (period === 'month') {
      var year = new Date().getFullYear();
      setDate({
        startDate: moment().startOf('month').format('YYYY-MM-DD'),
        endDate: moment().endOf('month').format('YYYY-MM-DD'),
      })
    }
    if (period === 'week') {
      var year = new Date().getFullYear();
      var month = new Date().getMonth();
      setDate({
        startDate: moment().startOf('week').format('YYYY-MM-DD'),
        endDate: moment().endOf('week').format('YYYY-MM-DD'),
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
          <button onClick={() => changeDate('year')} className="mr-2 btn btn-primary">Bu Yıl</button>
          <button onClick={() => changeDate('month')} className="mr-2 btn btn-primary">Bu Ay</button>
          <button onClick={() => changeDate('week')} className="mr-2 btn btn-primary">Bu Hafta</button>
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
