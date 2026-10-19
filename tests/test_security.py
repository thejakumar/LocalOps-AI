import io, zipfile, pytest
from fastapi import UploadFile
from backend.app.storage import _validate_zip
def zipped(name):
    out=io.BytesIO()
    with zipfile.ZipFile(out,'w') as z: z.writestr(name,'bad')
    return out.getvalue()
def test_traversal_zip_rejected(tmp_path):
    from fastapi import HTTPException
    with pytest.raises(HTTPException): _validate_zip(zipped('../escape.cs'),tmp_path/'source')
