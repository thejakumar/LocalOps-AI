from dataclasses import dataclass, field
from pathlib import Path
import shutil, tempfile, uuid
from fastapi import UploadFile, HTTPException

MAX_LOG = 2 * 1024 * 1024
MAX_ZIP = 10 * 1024 * 1024
MAX_FILE = 512 * 1024
MAX_FILES = 200

@dataclass
class Incident:
    id: str
    root: Path
    log_filename: str
    source_filename: str
    report: object | None = None
    budget: int = 8

INCIDENTS: dict[str, Incident] = {}

def _safe_name(name: str | None) -> str:
    if not name or Path(name).name != name or name in {'.', '..'}:
        raise HTTPException(400, 'invalid upload filename')
    return name

async def _read_upload(upload: UploadFile, limit: int) -> bytes:
    data = await upload.read(limit + 1)
    if len(data) > limit:
        raise HTTPException(413, 'upload exceeds size limit')
    return data

def _validate_zip(data: bytes, destination: Path) -> None:
    import zipfile
    import stat
    try:
        with zipfile.ZipFile(__import__('io').BytesIO(data)) as archive:
            infos = archive.infolist()
            if len(infos) > MAX_FILES: raise HTTPException(413, 'too many source files')
            for info in infos:
                p = Path(info.filename)
                if p.is_absolute() or '..' in p.parts or '\\' in info.filename:
                    raise HTTPException(400, 'unsafe archive path')
                mode = info.external_attr >> 16
                if stat.S_ISLNK(mode): raise HTTPException(400, 'symbolic links are not allowed')
                if info.file_size > MAX_FILE: raise HTTPException(413, 'source file exceeds size limit')
            archive.extractall(destination)
    except zipfile.BadZipFile as exc:
        raise HTTPException(400, 'source must be a valid zip archive') from exc

async def create_incident(log: UploadFile, source: UploadFile) -> Incident:
    log_name, source_name = _safe_name(log.filename), _safe_name(source.filename)
    if not log_name.lower().endswith(('.log', '.txt')): raise HTTPException(400, 'log must be .log or .txt')
    if not source_name.lower().endswith('.zip'): raise HTTPException(400, 'source must be a zip')
    log_data = await _read_upload(log, MAX_LOG)
    zip_data = await _read_upload(source, MAX_ZIP)
    root = Path(tempfile.mkdtemp(prefix='localops-'))
    (root / 'incident.log').write_bytes(log_data)
    (root / 'source').mkdir()
    try: _validate_zip(zip_data, root / 'source')
    except Exception:
        shutil.rmtree(root, ignore_errors=True); raise
    item = Incident(uuid.uuid4().hex, root, log_name, source_name)
    INCIDENTS[item.id] = item
    return item
