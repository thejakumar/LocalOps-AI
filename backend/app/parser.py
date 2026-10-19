import re
from .models import ParsedLog

EXC = re.compile(r'(?P<type>[A-Za-z_][\w.]*(?:Exception|Error))')
FRAME = re.compile(r'at\s+(?P<symbol>[\w.<>]+(?:\([^)]*\))?)\s+in\s+(?P<file>[^:]+):line\s+(?P<line>\d+)', re.I)
def parse_dotnet_log(text: str) -> ParsedLog:
    exception = None
    for line in text.splitlines():
        match = EXC.search(line)
        if match: exception = match.group('type'); break
    frames, symbols = [], []
    for line in text.splitlines():
        match = FRAME.search(line)
        if match:
            frames.append(line.strip()); symbols.append(match.group('symbol').split('(', 1)[0])
    timestamp = None
    if text.splitlines():
        m = re.search(r'\b(\d{4}-\d\d-\d\d[T ][^ ]+)', text.splitlines()[0]); timestamp = m.group(1) if m else None
    return ParsedLog(exception_type=exception, timestamp=timestamp, stack_frames=frames, symbols=symbols)
