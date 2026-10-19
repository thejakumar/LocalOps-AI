from backend.app.parser import parse_dotnet_log
from pathlib import Path
def test_parser_extracts_dotnet_fields():
    parsed=parse_dotnet_log(Path('tests/fixtures/incident.log').read_text())
    assert parsed.exception_type == 'System.NullReferenceException'
    assert 'Demo.OrderService.CalculateTotal' in parsed.symbols
    assert 'OrderService.cs:line 12' in parsed.stack_frames[0]
