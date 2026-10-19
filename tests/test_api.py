import io, zipfile
from fastapi.testclient import TestClient
from backend.app.main import app
client=TestClient(app)
def source_zip():
    out=io.BytesIO()
    with zipfile.ZipFile(out,'w') as z:
        for name in ('OrderService.cs','OrdersController.cs'):
            z.write(f'tests/fixtures/{name}',name)
    return out.getvalue()
def test_api_basics_and_grounded_report():
    response=client.post('/api/incidents', files={'log':('incident.log',open('tests/fixtures/incident.log','rb'),'text/plain'),'source':('source.zip',source_zip(),'application/zip')})
    assert response.status_code==201; incident=response.json(); ident=incident['id']
    assert client.get('/health').json()['status']=='ok'
    result=client.post(f'/api/incidents/{ident}/investigate').json()
    assert result['status']=='supported'; assert result['evidence'][0]['file']=='OrderService.cs'; assert result['evidence'][0]['start_line'] <= 5 <= result['evidence'][0]['end_line']
    assert client.get(f'/api/incidents/{ident}/report').status_code==200
    assert client.get(f'/api/incidents/{ident}/trace').json()['tool_trace']
def test_invalid_uploads_and_missing_evidence():
    bad=client.post('/api/incidents', files={'log':('x.exe',b'no','application/octet-stream'),'source':('x.zip',source_zip(),'application/zip')})
    assert bad.status_code==400
    empty=io.BytesIO();
    with zipfile.ZipFile(empty,'w') as z: z.writestr('Other.cs','class Other {}')
    r=client.post('/api/incidents', files={'log':('x.log',b'System.InvalidOperationException\n','text/plain'),'source':('x.zip',empty.getvalue(),'application/zip')})
    assert r.status_code==201
    report=client.post('/api/incidents/'+r.json()['id']+'/investigate').json()
    assert report['status']=='inconclusive'; assert not report['evidence']
