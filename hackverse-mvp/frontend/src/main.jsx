import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import App from './App'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Weights from './pages/Weights'
import './styles.css'

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<App/>}>
          <Route index element={<Dashboard/>} />
          <Route path='login' element={<Login/>} />
          <Route path='weights' element={<Weights/>} />
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
)
