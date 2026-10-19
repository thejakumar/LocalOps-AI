from pathlib import Path
from dataclasses import dataclass

@dataclass
class Budget:
    remaining: int = 8
    def use(self):
        if self.remaining <= 0: return False
        self.remaining -= 1; return True

def _files(root: Path):
    return (p for p in root.rglob('*') if p.is_file() and 'source' in p.parts and p.suffix.lower() in {'.cs','.csproj','.json','.config'})

def search_code(root: Path, query: str, budget: Budget):
    if not budget.use(): return {'error': 'tool budget exhausted', 'matches': []}
    matches=[]
    for p in _files(root):
        try:
            for n,line in enumerate(p.read_text(encoding='utf-8', errors='replace').splitlines(),1):
                if query.lower() in line.lower(): matches.append({'file': str(p.relative_to(root / 'source')), 'line': n, 'text': line[:500]})
        except OSError: continue
    return {'matches': matches[:50]}

def find_symbol(root: Path, symbol: str, budget: Budget):
    return search_code(root, symbol.split('.')[-1], budget)

def read_file_lines(root: Path, file: str, start: int, end: int, budget: Budget):
    if not budget.use(): return {'error': 'tool budget exhausted', 'lines': []}
    if start < 1 or end < start or end - start > 80 or Path(file).name != file and '..' in Path(file).parts: return {'error':'invalid bounded range','lines':[]}
    p=(root/'source'/file).resolve(); base=(root/'source').resolve()
    if base not in p.parents or not p.is_file(): return {'error':'file not found','lines':[]}
    lines=p.read_text(encoding='utf-8', errors='replace').splitlines()
    return {'lines':[{'number':n,'text':lines[n-1]} for n in range(start,min(end,len(lines))+1)], 'file':file}
