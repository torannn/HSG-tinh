import os
import sys
from pathlib import Path

# Configure stdout to use utf-8
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

log_path = Path(__file__).resolve().parent.parent / "generated_ex_test" / "test-style" / "de-thi.log"
if log_path.exists():
    print("Log file size:", log_path.stat().st_size)
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    print("\n--- Last 50 lines ---")
    for line in lines[-50:]:
        try:
            print(line.rstrip())
        except Exception:
            print(line.rstrip().encode('ascii', errors='replace').decode('ascii'))
        
    print("\n--- Error lines ---")
    for idx, line in enumerate(lines):
        if '!' in line or 'Error' in line or 'Undefined control sequence' in line:
            # Print context
            start = max(0, idx - 2)
            end = min(len(lines), idx + 3)
            print(f"Context around line {idx + 1}:")
            for j in range(start, end):
                marker = "=>" if j == idx else "  "
                try:
                    print(f"{marker} {j+1}: {lines[j].rstrip()}")
                except Exception:
                    print(f"{marker} {j+1}: {lines[j].rstrip().encode('ascii', errors='replace').decode('ascii')}")
else:
    print("Log file does not exist")
