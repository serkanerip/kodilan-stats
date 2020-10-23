import React from 'react';
import './search.css';

export default function Search() {
    return <>
        <div className="search-container">
            <div className="mini-container row">
                <div className="col-12 d-flex">
                    <button className="btn btn-primary">En Popülerler</button>
                    <button className="btn btn-success">... Geçen İlanlardaki En Popüler Tagler</button>
                    <button className="btn btn-secondary"></button>
                    <button className="btn btn-primary">Bir Tag'i Ara</button>
                </div>
                <p>Search page.</p>
            </div>
        </div>
    </>
}