import sys
import subprocess
from pathlib import Path
import json

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
import parse_olmocr

# Define temporary output path for testing
TEST_OUT = ROOT / 'generated_ex_test' / 'test-style'

def test_compile_style(header_style, footer_style, test_name):
    print(f"\n==========================================")
    print(f"Testing Theme: {test_name}")
    print(f"Header: {header_style} | Footer: {footer_style}")
    print(f"==========================================")
    
    # 1. Update ocean-breeze style configuration in memory
    config = parse_olmocr.STYLES['ocean-breeze'].copy()
    config['page_header_style'] = header_style
    config['page_footer_style'] = footer_style
    
    # Override in global STYLES dict
    parse_olmocr.STYLES['ocean-breeze'] = config
    
    # 2. Run parse_olmocr style injection
    print("Running inject_all with style ocean-breeze...")
    parse_olmocr.copy_input_to_output(str(ROOT / 'generated_ex_test' / 'hsg-12-khao-sat-ham-so'), str(TEST_OUT))
    
    input_path = ROOT / 'generated_ex_test' / 'hsg-12-khao-sat-ham-so'
    for f in ['de-thi.tex', 'de-va-loigiai.tex', 'dap-an.tex']:
        parse_olmocr.inject_style_to_file(input_path / f, TEST_OUT / f, 'ocean-breeze')
        
    print("Injected styles successfully. Now compiling...")
    
    # 3. Compile all files
    for f_name in ['de-thi', 'de-va-loigiai', 'dap-an']:
        print(f"Compiling {f_name}.tex...")
        cmd = ["pdflatex", "-interaction=nonstopmode", f"{f_name}.tex"]
        res = subprocess.run(cmd, capture_output=True, cwd=str(TEST_OUT))
        if res.returncode != 0:
            print(f"[FAIL] COMPILATION FAILED for {f_name}.tex!")
            stdout = res.stdout.decode('utf-8', errors='ignore')
            stderr = res.stderr.decode('utf-8', errors='ignore')
            print("--- STDOUT ---")
            print('\n'.join(stdout.splitlines()[-20:]))
            print("--- STDERR ---")
            print(stderr)
            sys.exit(1)
        else:
            print(f"[PASS] Compile {f_name}.tex succeeded!")
            
    print(f"--- Test '{test_name}' passed successfully! ---")

# Test Scenario 1: Double line header, Accent bar footer
test_compile_style('double-line', 'accent-bar', 'DoubleLineHeader_AccentBarFooter')

# Test Scenario 2: Accent bar header, Double line footer
test_compile_style('accent-bar', 'double-line', 'AccentBarHeader_DoubleLineFooter')
