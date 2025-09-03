import React, { useEffect, useState } from 'react'
import axios from 'axios'
import AnimatedKPI from '../components/AnimatedKPI'

export default function Dashboard(){
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(()=>{
    const token = localStorage.getItem('hv_token')
    axios.get('/api/v1/threats/detect', { params: {dummy: 1}, headers: { Authorization: token ? `Bearer ${token}` : '' } }).then(r=>{
      setSummary(r.data)
      setLoading(false)
    }).catch(()=>{
      setSummary(null)
      setLoading(false)
    })
  },[])

  return (
    <div>
      <h1>Dashboard</h1>
      <div className="kpi-grid">
        <AnimatedKPI label="Aggregate score" value={summary?.aggregate_score || 0} suffix="" />
        <AnimatedKPI label="Is threat" value={summary?.is_threat ? 1 : 0} />
        <AnimatedKPI label="Top technique score" value={summary?.top_technique?.score || 0} />
      </div>

      {loading && <div className="spinner" />}

      {!loading && summary && (
        <div className="card" style={{marginTop:20}}>
          <h3>Per-technique results</h3>
          <ul>
            {summary.per_technique.map(p => (
              <li key={p.technique} className="tech-row">
                <strong>{p.technique}</strong>
                <div className="bar-wrap"><div className="bar" style={{width: `${Math.min(100, p.score*100)}%`}}></div></div>
                <code>{p.score.toFixed(2)}</code>
              </li>
            ))}
          </ul>
        </div>
      )}

      {!loading && !summary && <div className="card">No status (login required or server offline)</div>}
    </div>
  )
}
