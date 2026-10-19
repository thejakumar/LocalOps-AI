from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from .storage import create_incident, INCIDENTS
from .models import IncidentSummary, Report
from .investigator import investigate

app=FastAPI(title='LocalOps AI')
@app.get('/health')
def health(): return {'status':'ok'}
@app.post('/api/incidents', response_model=IncidentSummary, status_code=201)
async def upload_incident(log: UploadFile=File(...), source: UploadFile=File(...)):
    item=await create_incident(log,source)
    from datetime import datetime, timezone
    return IncidentSummary(id=item.id, log_filename=item.log_filename, source_filename=item.source_filename, created_at=datetime.now(timezone.utc))
def get_item(id):
    if id not in INCIDENTS: raise HTTPException(404,'incident not found')
    return INCIDENTS[id]
@app.post('/api/incidents/{id}/investigate', response_model=Report)
def run_investigation(id: str, budget: int=Query(8, ge=1, le=32)):
    item=get_item(id); item.report=investigate(item,budget); item.budget=budget; return item.report
@app.get('/api/incidents/{id}', response_model=IncidentSummary)
def incident(id: str):
    item=get_item(id); from datetime import datetime, timezone
    return IncidentSummary(id=item.id, log_filename=item.log_filename, source_filename=item.source_filename, created_at=datetime.now(timezone.utc), investigated=item.report is not None)
@app.get('/api/incidents/{id}/report', response_model=Report)
def report(id: str):
    item=get_item(id)
    if item.report is None: raise HTTPException(409,'incident has not been investigated')
    return item.report
@app.get('/api/incidents/{id}/trace')
def trace(id: str):
    item=get_item(id); return {'incident_id': id, 'tool_trace': item.report.tool_trace if item.report else []}
