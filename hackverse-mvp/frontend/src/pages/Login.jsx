import React, { useState } from 'react'
import axios from 'axios'

export default function Login(){
  const [user, setUser] = useState({username:'', password:''})
  const [error, setError] = useState(null)

  const submit = async (e) =>{
    e.preventDefault()
    setError(null)
    try{
      const form = new URLSearchParams()
      form.append('username', user.username)
      form.append('password', user.password)
      const res = await axios.post('/api/v1/auth/token', form)
      const token = res.data.access_token
      localStorage.setItem('hv_token', token)
      window.location.href = '/'
    }catch(err){
      setError(err.response?.data?.detail || 'Login failed')
    }
  }

  return (
    <div className="card">
      <h2>Sign in</h2>
      <form onSubmit={submit}>
        <label>Username</label>
        <input value={user.username} onChange={e=>setUser({...user, username:e.target.value})} />
        <label>Password</label>
        <input type="password" value={user.password} onChange={e=>setUser({...user, password:e.target.value})} />
        <button className="btn">Sign in</button>
        {error && <div className="error">{error}</div>}
      </form>
    </div>
  )
}
