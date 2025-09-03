import React, { useEffect, useState } from 'react'
import axios from 'axios'

export default function Weights(){
  const [weights, setWeights] = useState([])
  const [error, setError] = useState(null)

  useEffect(()=>{
    axios.get('/api/v1/weights/').then(r=>setWeights(r.data)).catch(e=>setError('Could not fetch'))
  },[])

  const update = async (tech, val) =>{
    const fv = parseFloat(val)
    if(Number.isNaN(fv) || fv < 0){ setError('Weight must be a non-negative number'); return }
    try{
      const token = localStorage.getItem('hv_token')
      await axios.put(`/api/v1/weights/${encodeURIComponent(tech)}`, { weight: fv }, { headers: { Authorization: token ? `Bearer ${token}` : '' } })
      setWeights(weights.map(w=> w.technique===tech?{...w, weight: fv}:w))
      setError(null)
    }catch(err){
      setError('Update failed')
    }
  }

  return (
    <div className="card">
      <h2>Agent Weights</h2>
      {error && <div className="error">{error}</div>}
      <table style={{width:'100%'}}>
        <thead><tr><th>Technique</th><th style={{width:140}}>Weight</th><th></th></tr></thead>
        <tbody>
          {weights.map(w=> (
            <tr key={w.technique}>
              <td>{w.technique}</td>
              <td><input defaultValue={w.weight} id={`w-${w.technique}`} style={{width:110}} /></td>
              <td><button onClick={()=>update(w.technique, document.getElementById(`w-${w.technique}`).value)} className="btn">Save</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
