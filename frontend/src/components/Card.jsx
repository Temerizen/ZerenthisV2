import React from 'react'

export default function Card({ title, children }) {
  return (
    <div style={{
      background: '#111827',
      color: 'white',
      borderRadius: 16,
      padding: 16,
      boxShadow: '0 8px 24px rgba(0,0,0,0.25)',
      minHeight: 120
    }}>
      <div style={{ fontSize: 18, fontWeight: 700, marginBottom: 12 }}>{title}</div>
      <div>{children}</div>
    </div>
  )
}
