import React, { useEffect, useState } from 'react'
import { api } from '../api/client'
import Card from '../components/Card'

export default function DashboardPage() {
  const [health, setHealth] = useState(null)
  const [status, setStatus] = useState(null)
  const [queue, setQueue] = useState([])
  const [jobs, setJobs] = useState([])
  const [founder, setFounder] = useState(null)
  const [busy, setBusy] = useState(false)

  const refresh = async () => {
    const [h, s, q, j, f] = await Promise.all([
      api.health(),
      api.status(),
      api.queue(),
      api.jobs(),
      api.founder()
    ])
    setHealth(h)
    setStatus(s)
    setQueue(Array.isArray(q) ? q : [])
    setJobs(j?.jobs || [])
    setFounder(f)
  }

  useEffect(() => {
    refresh()
  }, [])

  const seed = async () => {
    setBusy(true)
    await api.seed()
    await refresh()
    setBusy(false)
  }

  const run = async () => {
    setBusy(true)
    await api.run()
    await refresh()
    setBusy(false)
  }

  return (
    <div style={{ padding: 24 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <div style={{ fontSize: 32, fontWeight: 800 }}>Zerenthis V2</div>
          <div style={{ color: '#4b5563' }}>Empire Command Center Spine</div>
        </div>
        <div style={{ display: 'flex', gap: 12 }}>
          <button onClick={seed} disabled={busy} style={btn}>Seed Ideas</button>
          <button onClick={run} disabled={busy} style={btn}>Run Execution</button>
          <button onClick={refresh} disabled={busy} style={btn}>Refresh</button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, minmax(0, 1fr))', gap: 16 }}>
        <Card title="Health"><pre style={pre}>{JSON.stringify(health, null, 2)}</pre></Card>
        <Card title="System"><pre style={pre}>{JSON.stringify(status, null, 2)}</pre></Card>
        <Card title="Founder"><pre style={pre}>{JSON.stringify(founder, null, 2)}</pre></Card>
        <Card title="Idea Queue"><pre style={pre}>{JSON.stringify(queue, null, 2)}</pre></Card>
        <Card title="Jobs"><pre style={pre}>{JSON.stringify(jobs, null, 2)}</pre></Card>
        <Card title="Status">
          <div style={{ color: '#d1d5db' }}>
            Burst 4 adds the dashboard spine and deployment rails.
          </div>
        </Card>
      </div>
    </div>
  )
}

const btn = {
  background: '#111827',
  color: 'white',
  border: 'none',
  borderRadius: 12,
  padding: '10px 14px',
  cursor: 'pointer',
  fontWeight: 700
}

const pre = {
  whiteSpace: 'pre-wrap',
  wordBreak: 'break-word',
  margin: 0,
  color: '#d1d5db',
  fontSize: 12
}
