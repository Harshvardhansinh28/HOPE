import React, { useEffect, useRef, useState } from 'react'

export default function AnimatedKPI({ label, value = 0, duration = 900, suffix = '' }){
  const [display, setDisplay] = useState(0)
  const rafRef = useRef()
  const startRef = useRef()
  const from = useRef(0)

  useEffect(()=>{
    cancelAnimationFrame(rafRef.current)
    from.current = display
    const start = performance.now()
    startRef.current = start
    const animate = (t) => {
      const dt = Math.min(1, (t - start)/duration)
      const eased = 1 - Math.pow(1 - dt, 3)
      setDisplay(from.current + (value - from.current) * eased)
      if(dt < 1) rafRef.current = requestAnimationFrame(animate)
    }
    rafRef.current = requestAnimationFrame(animate)
    return () => cancelAnimationFrame(rafRef.current)
  }, [value])

  return (
    <div className="kpi card">
      <div className="label">{label}</div>
      <div className="value">{typeof value === 'number' ? display.toFixed(2) : value}{suffix}</div>
    </div>
  )
}
import React, { useEffect, useState } from 'react'

export default function AnimatedKPI({label, value, suffix = '', duration = 1200}){
  const [display, setDisplay] = useState(0)
  useEffect(()=>{
    let start = null
    const from = 0
    const to = Number(value) || 0
    function step(ts){
      if(!start) start = ts
      const progress = Math.min((ts-start)/duration, 1)
      setDisplay((from + (to-from)*progress).toFixed(2))
      if(progress < 1) requestAnimationFrame(step)
    }
    requestAnimationFrame(step)
  },[value, duration])

  return (
    <div className="kpi-card">
      <div className="kpi-label">{label}</div>
      <div className="kpi-value">{display}{suffix}</div>
    </div>
  )
}
