from backend.app.tools import Budget, read_file_lines
from pathlib import Path
def test_budget_enforced(tmp_path):
    (tmp_path/'source').mkdir(); (tmp_path/'source'/'a.cs').write_text('one\ntwo')
    b=Budget(1); assert read_file_lines(tmp_path,'a.cs',1,1,b)['lines']; assert 'error' in read_file_lines(tmp_path,'a.cs',1,1,b)
