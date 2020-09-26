import React, { useState, useEffect } from 'react';

function PositionStats({date}) {
    const [stats, setStats] = useState([]);
    const apiURL = "http://localhost:5000/api/v1/stats/position"

    useEffect(() => {
        const params = date.startDate !== null ? 
            `?startDate=${date.startDate}&endDate=${date.endDate}`
            : ''

        fetch(`${apiURL + params}`)
        .then(res => res.json())
        .then(data => setStats(data.data))
    }, [date])

    return <div className="row">
        <div className="col-12">
            <table className="table table-sm table-bordered text-center">
                <thead>
                    <tr>
                        <th>Pozisyon</th>
                        <th>İlan Sayısı</th>
                    </tr>
                </thead>
                <tbody>
                    {stats.slice(0,10).map(stat => (
                        <tr>
                            <td>{stat.position}</td>
                            <td>{stat.toplam_ilan_sayisi}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    </div>
}

export default PositionStats;