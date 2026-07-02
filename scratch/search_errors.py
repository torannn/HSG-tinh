import sys
from pathlib import Path

# Configure stdout to use utf-8
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

log_path = Path(__file__).resolve().parent.parent / "generated_ex_test" / "test-style" / "de-thi.log"
if log_path.exists():
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    lines = content.splitlines()
    print("Total lines in log:", len(lines))
    
    # Let's search for LaTeX errors
    # LaTeX errors typically start with '!'
    found_errors = False
    for idx, line in enumerate(lines):
        if line.startswith('!'):
            found_errors = True
            print(f"\n--- Error at line {idx+1} ---")
            for j in range(max(0, idx-4), min(len(lines), idx+10)):
                marker = "=>" if j == idx else "  "
                print(f"{marker} {j+1}: {lines[j]}")
                
    if not found_errors:
        print("No lines starting with '!' found.")
        
    # Let's search for 'warning' or 'error' case insensitively
    warning_count = 0
    error_count = 0
    for idx, line in enumerate(lines):
        line_lower = line.lower()
        if 'error' in line_lower and 'first aid' not in line_lower:
            error_count += 1
            if error_count <= 10:
                print(f"Error keyword line {idx+1}: {line}")
        if 'warning' in line_lower:
            warning_count += 1
            
    print(f"Total error keyword lines (excluding first aid): {error_count}")
    print(f"Total warning lines: {warning_count}")
else:
    print("Log file does not exist")
