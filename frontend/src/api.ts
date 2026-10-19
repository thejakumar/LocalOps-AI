import type { Report } from './types'
const configuredApi = import.meta.env.VITE_API_URL || ''
const API = configuredApi && !/^https?:\/\//.test(configuredApi) ? `https://${configuredApi}` : configuredApi
async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API}${path}`, init)
  if (!res.ok) { const detail = await res.text().catch(() => ''); throw new Error(detail || `Request failed (${res.status})`) }
  return res.json() as Promise<T>
}
export async function createIncident(log: File, source: File) {
  const body = new FormData(); body.append('log', log); body.append('source', source)
  return request<{ incident_id: string; id?: string }>('/api/incidents', { method: 'POST', body })
}
export async function investigate(id: string) { return request<{ status?: string }>(`/api/incidents/${encodeURIComponent(id)}/investigate`, { method: 'POST' }) }
export async function getReport(id: string) { return request<Report>(`/api/incidents/${encodeURIComponent(id)}/report`) }
export async function health() { return request<{ status?: string }>('/health') }
