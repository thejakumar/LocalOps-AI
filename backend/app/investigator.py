from .parser import parse_dotnet_log
from .tools import Budget, search_code, find_symbol, read_file_lines
from .models import Report, Evidence, TraceEvent

def investigate(item, budget_limit=8):
    parsed=parse_dotnet_log((item.root/'incident.log').read_text(encoding='utf-8',errors='replace'))
    budget=Budget(budget_limit); trace=[]; warnings=[]
    def call(name, fn, *args):
        result=fn(item.root,*args,budget); trace.append(TraceEvent(tool=name, arguments_summary=str(args)[:200], result_summary=str(result)[:500])); return result
    matches=call('search_code', search_code, parsed.symbols[0].split('.')[-1] if parsed.symbols else (parsed.exception_type or 'Exception'))
    evidence=[]
    for match in matches.get('matches',[])[:3]:
        result=call('read_file_lines', read_file_lines, match['file'], max(1,match['line']-2), match['line']+2)
        lines=result.get('lines',[])
        if lines:
            evidence.append(Evidence(file=match['file'], start_line=lines[0]['number'], end_line=lines[-1]['number'], excerpt='\n'.join(x['text'] for x in lines), rationale='The source contains the stack-frame symbol and was read through the bounded source tool.'))
    if evidence:
        cause=f"{parsed.exception_type or 'Exception'} is likely raised in {evidence[0].file} near line {evidence[0].start_line}."
        status='supported'; fix='Add an explicit null/argument guard at the cited dereference and preserve the original failure context.'
    else:
        cause='Insufficient source evidence to identify a probable cause.'; status='inconclusive'; fix='Collect the matching source file and a complete stack trace before changing code.'; warnings.append('No grounded source match was available; no file or line is asserted.')
    if budget.remaining == 0: warnings.append('Investigation stopped at the configured tool budget.')
    return Report(incident_id=item.id, exception_type=parsed.exception_type, probable_cause=cause, status=status, evidence=evidence, proposed_fix=fix, validation_steps=['Add a regression test for the failing pathway.', 'Run the relevant .NET test project.', 'Reproduce the incident and verify the exception is handled.'], tool_trace=trace, warnings=warnings)
