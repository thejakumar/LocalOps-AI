import { describe, expect, it, vi } from 'vitest'
import { createIncident } from './api'

describe('incident API client', () => {
  it('uploads both incident inputs and returns the backend id', async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify({ incident_id: 'inc-123' }), { status: 200, headers: { 'Content-Type': 'application/json' } }))
    vi.stubGlobal('fetch', fetchMock)
    const result = await createIncident(new File(['error'], 'incident.log'), new File(['zip'], 'source.zip'))
    expect(result.incident_id).toBe('inc-123')
    expect(fetchMock).toHaveBeenCalledWith('/api/incidents', expect.objectContaining({ method: 'POST', body: expect.any(FormData) }))
  })
})
