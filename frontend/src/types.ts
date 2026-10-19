export type IncidentStatus = 'idle' | 'uploading' | 'queued' | 'running' | 'complete' | 'failed'
export type Evidence = { file: string; start_line?: number; end_line?: number; excerpt?: string; rationale?: string }
export type ToolCall = { tool?: string; name?: string; arguments_summary?: string; result_summary?: string; status?: string; duration_ms?: number }
export type Report = { incident_id?: string; exception_type?: string; status?: 'hypothesis' | 'supported' | 'inconclusive'; probable_cause?: string; evidence?: Evidence[]; proposed_fix?: string; validation_steps?: string[]; tool_trace?: ToolCall[]; warnings?: string[]; created_at?: string }
