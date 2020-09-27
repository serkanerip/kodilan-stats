import React, { useState, useEffect } from 'react';

function TechStats({backend, date}) {
    const [stats, setStats] = useState([]);
    const apiURL = `${backend}/api/v1/stats/web`

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
                        <th>Teknoloji</th>
                        <th>İlan Sayısı</th>
                    </tr>
                </thead>
                <tbody>
                    {stats.slice(0,10).map(stat => (
                        <tr key={stat.tech}>
                            <td>{stat.tech}</td>
                            <td>{stat.total}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    </div>
}

export default TechStats;