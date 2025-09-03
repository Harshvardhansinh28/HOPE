import React from 'react'
import { Outlet, Link } from 'react-router-dom'

export default function App(){
  return (
    <div className="app">
      <header className="header">
        <div className="brand">HACKVERSE</div>
        <nav>
          <Link to="/">Dashboard</Link>
          <Link to="/login">Login</Link>
          <Link to="/weights">Weights</Link>
        </nav>
      </header>
      <main className="main">
        <Outlet />
      </main>
      <footer className="footer">© HACKVERSE</footer>
    </div>
  )
}
