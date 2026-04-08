const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

async function request(path, options = {}) {
  const res = await fetch(API_BASE + path, {
    headers: { 'Content-Type': 'application/json' },
    ...options
  })
  const text = await res.text()
  try {
    return JSON.parse(text)
  } catch {
    return { raw: text, status: res.status }
  }
}

export const api = {
  health: () => request('/health'),
  status: () => request('/api/system/status'),
  seed: () => request('/api/decision/seed', { method: 'POST' }),
  queue: () => request('/api/decision/queue'),
  next: () => request('/api/decision/next'),
  run: () => request('/api/execution/run', { method: 'POST' }),
  jobs: () => request('/api/jobs'),
  founder: () => request('/api/founder/panel'),
  flags: () => request('/api/founder/flags'),
  reports: () => request('/api/research/reports'),
  lessons: () => request('/api/learning/lessons')
}
