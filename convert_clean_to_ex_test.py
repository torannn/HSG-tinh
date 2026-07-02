import os
import sys
import re
import shutil
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / 'pdf_to_tex_outputs'
EXAMPLE_DIR = ROOT / 'ex_test'
OUTPUT_DIR = ROOT / 'generated_ex_test'

QUESTION_START_RE = re.compile(r'^(?:\*\*)*Câu\s*(\d+)[\.:]?(?:\*\*)*\s*(.*)$', re.IGNORECASE)
CHOICE_RE = re.compile(r'(?<![\w\\])([A-D])\s*[\.\)\:]\s*')
TF_RE = re.compile(r'(?<![\w\\])([a-d])\s*[\.\)\:]\s*')

# Try to force stdout/stderr to UTF-8
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Hardcoded keys for True/False questions in Trấn Biên (since old tex didn't have them)
TRAN_BIEN_TF_KEYS = {
    25: [True, False, True, False],
    26: [False, False, True, True]
}

def extract_inline_header(text):
    """
    Checks if the text contains a section header inline (e.g., 'Phần II' or 'Tự luận')
    and extracts it. Returns (text_before, header_text) or (text, None).
    """
    pattern = r'\s*\b(phần\s+(?:[ivxl\d]+)\b.*?|tự\s+luận\s*(?:\(.*?\))?|\d+[\.\)]\s*(?:trắc\s+nghiệm|tự\s+luận).*?)\s*$'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        start = match.start()
        header = match.group(1).strip()
        before = text[:start].strip()
        return before, header
    return text, None

def extract_answers_from_old_tex(tex_path):
    """
    Parses existing tex files to extract \True choices (for multiple choice and true/false).
    Returns a dict: {question_num: {'type': 'choice'/'choiceTF', 'answers': [...]}}
    """
    if not os.path.exists(tex_path):
        return {}
        
    try:
        with open(tex_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception:
        return {}
        
    ex_blocks = re.findall(r'\\begin\{ex\}(.*?)\\end\{ex\}', content, re.DOTALL)
    answers_map = {}
    
    for idx, block in enumerate(ex_blocks):
        q_num = idx + 1
        if '\\choiceTF' in block:
            options = re.findall(r'\{(.*?)\}', block)
            tf_ans = []
            for opt in options:
                if '\\True' in opt or 'True' in opt:
                    tf_ans.append(True)
                else:
                    if len(tf_ans) < 4:
                        tf_ans.append(False)
            if len(tf_ans) == 4:
                answers_map[q_num] = {'type': 'choiceTF', 'answers': tf_ans}
        elif '\\choice' in block:
            options = re.findall(r'\{(.*?)\}', block)
            choice_idx = -1
            all_mc_options = [opt for opt in options if opt.strip()]
            for i, opt in enumerate(all_mc_options[:4]):
                if '\\True' in opt or 'True' in opt:
                    choice_idx = i
                    break
            if choice_idx != -1:
                answers_map[q_num] = {'type': 'choice', 'answers': choice_idx}
                
    return answers_map

def clean_vietnamese_text(text):
    text = text.replace('giữ liệu', 'dữ liệu')
    text = text.replace('biê t ra ng', 'biết rằng')
    text = text.replace('chiê u cao', 'chiều cao')
    text = text.replace('thơ i gian', 'thời gian')
    text = text.replace('kê tư lu c', 'kể từ lúc')
    text = text.replace('ươ c ti nh', 'ước tính')
    text = text.replace('thêo', 'theo')
    text = text.replace('nura khoang', 'nửa khoảng')
    text = text.replace('đơ n vi', 'đơn vị')
    text = text.replace('tiê n ha nh', 'tiến hành')
    text = text.replace('thư nghiê m', 'thử nghiệm')
    text = text.replace('gio ng', 'giống')
    text = text.replace('khâ o sa t', 'khảo sát')
    text = text.replace('ca n na ng', 'cân nặng')
    text = text.replace('thươ ng', 'thường')
    text = text.replace('ma u so', 'mẫu số')
    text = text.replace('cơ sơ', 'cơ sở')
    text = text.replace('cha n nuo i', 'chăn nuôi')
    text = text.replace('gia ca m', 'gia cầm')
    text = text.replace('lã suất', 'lãi suất')
    text = text.replace('−', '-')
    return text

def convert_math_delimiters(text):
    """
    Converts $$...$$ to $...$ for inline math, and cleans up set brackets inside math.
    Supports splitting by $ to apply context-aware character replacements.
    """
    # Standardize $$...$$ to $...$
    text = re.sub(r'\$\$(.*?)\$\$', r'$\1$', text)
    
    parts = text.split('$')
    for i in range(len(parts)):
        if i % 2 == 1:
            # Inside math mode
            inner = parts[i]
            # Escape sets in math mode (e.g. {1;2;3} -> \{1;2;3\})
            inner = re.sub(r'(?<!\\)\{([0-9\s;,\.\-\+]+[:;,\.\-\+][0-9\s;,\.\-\+]+)\}', r'\\{\1\\}', inner)
            inner = inner.replace('≤', r'\le')
            inner = inner.replace('≥', r'\ge')
            inner = inner.replace('≠', r'\ne')
            inner = inner.replace('°', r'^\circ')
            inner = inner.replace('○', r'^\circ')
            inner = inner.replace('∞', r'\infty')
            inner = inner.replace('∆', r'\Delta')
            parts[i] = inner
        else:
            # Outside math mode (text)
            outer = parts[i]
            outer = outer.replace('≤', r'$\le$')
            outer = outer.replace('≥', r'$\ge$')
            outer = outer.replace('≠', r'$\ne$')
            outer = outer.replace('°', r'$^\circ$')
            outer = outer.replace('○', r'$^\circ$')
            outer = outer.replace('∞', r'$\infty$')
            outer = outer.replace('∆', r'$\Delta$')
            parts[i] = outer
            
    return '$'.join(parts)

def parse_markdown_table(lines):
    """
    Converts Markdown table lines to LaTeX tabular.
    """
    rows = []
    for line in lines:
        parts = [cell.strip() for cell in line.split('|')[1:-1]]
        rows.append(parts)
    
    if not rows:
        return ""
        
    header = rows[0]
    data_rows = []
    for r in rows[1:]:
        if any(cell.startswith('---') for cell in r if cell):
            continue
        data_rows.append(r)
        
    width = max(len(r) for r in [header] + data_rows)
    spec = '|' + '|'.join(['c'] * width) + '|'
    
    tex_rows = [r'\begin{center}', r'\begin{tabular}{' + spec + '}', r'\hline']
    tex_rows.append(' & '.join(convert_math_delimiters(clean_vietnamese_text(cell)) for cell in header) + r' \\')
    tex_rows.append(r'\hline')
    for r in data_rows:
        padded = r + [''] * (width - len(r))
        tex_rows.append(' & '.join(convert_math_delimiters(clean_vietnamese_text(cell)) for cell in padded) + r' \\')
        tex_rows.append(r'\hline')
    tex_rows += [r'\end{tabular}', r'\end{center}']
    return '\n'.join(tex_rows)

def split_markdown_elements(text):
    """
    Splits the markdown text into sections, instructions, and questions.
    """
    lines = text.splitlines()
    elements = []
    
    current_question = None
    table_lines = []
    
    for raw_line in lines:
        line = raw_line.strip()
        
        if line.startswith('|'):
            table_lines.append(raw_line)
            continue
        elif table_lines:
            table_tex = parse_markdown_table(table_lines)
            if current_question:
                current_question['lines'].append(table_tex)
            else:
                elements.append({'type': 'text', 'content': table_tex})
            table_lines = []
            
        if not line:
            if current_question:
                current_question['lines'].append('')
            continue
            
        if line.startswith('#'):
            if current_question:
                elements.append(current_question)
                current_question = None
            level = len(line) - len(line.lstrip('#'))
            title = line.lstrip('#').strip()
            elements.append({'type': 'header', 'level': level, 'content': title})
            continue
            
        match = QUESTION_START_RE.match(line)
        if match:
            if current_question:
                elements.append(current_question)
            q_num = int(match.group(1))
            q_text = match.group(2).strip()
            current_question = {
                'type': 'question',
                'number': q_num,
                'lines': [q_text] if q_text else []
            }
        elif current_question:
            current_question['lines'].append(line)
        else:
            if line.startswith('*') or line.startswith('-'):
                line = line.lstrip('*-').strip()
            elements.append({'type': 'text', 'content': line})
            
    if current_question:
        elements.append(current_question)
        
    return elements

def format_question_choices(stem, choices, correct_idx=-1):
    stem_clean = convert_math_delimiters(clean_vietnamese_text(stem))
    stem_clean = stem_clean.lstrip('.').strip()
    if stem_clean.endswith(r'\\'):
        stem_clean = stem_clean[:-2].strip()
        
    tex = [stem_clean]
    tex.append(r'\choice')
    for i, ch in enumerate(choices):
        ch_clean = convert_math_delimiters(clean_vietnamese_text(ch))
        ch_clean = ch_clean.strip()
        if ch_clean.endswith('.') and not ch_clean.endswith('..'):
            ch_clean = ch_clean[:-1].strip()
        if i == correct_idx:
            tex.append(f'{{\\True {ch_clean}}}')
        else:
            tex.append(f'{{{ch_clean}}}')
    return '\n'.join(tex)

def format_question_tf(stem, statements, answers=None):
    stem_clean = convert_math_delimiters(clean_vietnamese_text(stem))
    stem_clean = stem_clean.lstrip('.').strip()
    if stem_clean.endswith(r'\\'):
        stem_clean = stem_clean[:-2].strip()
        
    tex = [stem_clean]
    tex.append(r'\choiceTF')
    for i, st in enumerate(statements):
        st_clean = convert_math_delimiters(clean_vietnamese_text(st))
        st_clean = st_clean.strip()
        if st_clean.endswith('.') and not st_clean.endswith('..'):
            st_clean = st_clean[:-1].strip()
        if answers and answers[i]:
            tex.append(f'{{\\True {st_clean}}}')
        else:
            tex.append(f'{{{st_clean}}}')
            
    sol = []
    sol.append(r'\begin{itemchoice}')
    for i in range(4):
        sol.append(r'\itemch Lời giải ý ' + ['a', 'b', 'c', 'd'][i] + '.')
    sol.append(r'\end{itemchoice}')
    
    return '\n'.join(tex), '\n'.join(sol)

def format_question_short(stem, ans_val):
    stem_clean = convert_math_delimiters(clean_vietnamese_text(stem))
    stem_clean = stem_clean.lstrip('.').strip()
    if stem_clean.endswith(r'\\'):
        stem_clean = stem_clean[:-2].strip()
        
    tex = [stem_clean]
    ans_clean = clean_vietnamese_text(ans_val).strip()
    if '\\' in ans_clean and not ans_clean.startswith('$') and not ans_clean.endswith('$'):
        ans_clean = f"${ans_clean}$"
    tex.append(f'\\shortans[0]{{{ans_clean}}}')
    return '\n'.join(tex)

def format_essay_question(stem, ans_val=None):
    stem_clean = convert_math_delimiters(clean_vietnamese_text(stem))
    stem_clean = stem_clean.lstrip('.').strip()
    if stem_clean.endswith(r'\\'):
        stem_clean = stem_clean[:-2].strip()
        
    tex = [stem_clean]
    if ans_val:
        ans_clean = clean_vietnamese_text(ans_val).strip()
        tex.append(f'\\dapso{{{ans_clean}}}')
    return '\n'.join(tex)

def process_file(slug, md_name, answers_map, images_dir):
    md_path = ROOT / md_name
    if not md_path.exists():
        print(f"Error: Markdown file {md_path} not found.")
        return
        
    print(f"Processing {md_name}...")
    with open(md_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
        
    elements = split_markdown_elements(text)
    
    preamble_lines = [
        r'\documentclass[12pt,a4paper,oneside]{article}',
        r'\usepackage[top=2cm, bottom=2cm, left=1.5cm, right=1.5cm]{geometry}',
        r'\usepackage{amsmath, amssymb, fancyhdr}',
        r'\usepackage{tkz-euclide,tikz-3dplot,tikz,tkz-tab}',
        r'\usepackage{fontawesome5}',
        # The ex_test package import with option will be added dynamically by wrapper generators
        r'\usetikzlibrary{shapes.geometric,arrows,decorations.pathmorphing,calc,intersections,angles}',
        r'\usepackage{pgfplots}',
        r'\usepgfplotslibrary{fillbetween}',
        r'\pgfplotsset{compat=1.9}',
        r'\usepackage[hidelinks,unicode]{hyperref}',
        r'\usepackage{esvect}',
        r'\def\vec{\vv}',
        r'\def\overrightarrow{\vv}',
        r'\newcommand{\hoac}[1]{\left[\begin{aligned}#1\end{aligned}\right.}',
        r'\newcommand{\heva}[1]{\left\{\begin{aligned}#1\end{aligned}\right.}',
        r'\renewcommand{\baselinestretch}{1.2}',
        r'\renewtheorem{ex}{\color{red}Câu}',
        r'\newtheorem{bt}{\namebt}',
    ]
    
    body_lines = [
        r'\OPTN{kindTF=t, kindSA=0}',
        r'\def\SSS{}',
        r'\OPTN{kindDrag=1}',
    ]
    
    opened_ans = False
    current_section = 'ex'
    
    def handle_transition(title_text):
        nonlocal opened_ans, current_section
        title_lower = title_text.lower()
        
        part_num = None
        if 'phần i' in title_lower or 'phần 1' in title_lower or 'phan i' in title_lower or 'phan 1' in title_lower:
            part_num = 1
        elif 'phần ii' in title_lower or 'phần 2' in title_lower or 'phan ii' in title_lower or 'phan 2' in title_lower:
            part_num = 2
        elif 'phần iii' in title_lower or 'phần 3' in title_lower or 'phan iii' in title_lower or 'phan 3' in title_lower:
            part_num = 3
        elif 'phần iv' in title_lower or 'phần 4' in title_lower or 'phan iv' in title_lower or 'phan 4' in title_lower or 'tự luận' in title_lower or 'tu luan' in title_lower:
            part_num = 4
            
        if part_num is not None:
            if opened_ans:
                body_lines.append(r'\Closesolutionfile{ans}')
                opened_ans = False
            if part_num in [1, 2, 3]:
                body_lines.append(r'\setcounter{ex}{0}')
                part_suffix = ['phanI', 'phanII', 'phanIII'][part_num - 1]
                body_lines.append(f'\\Opensolutionfile{{ans}}[ans/ans-{part_suffix}]')
                opened_ans = True
    
    for el in elements:
        if el['type'] == 'header':
            level = el['level']
            title = el['content'].strip()
            title_lower = title.lower()
            if 'tự luận' in title_lower or 'tu luan' in title_lower:
                current_section = 'bt'
            elif 'trắc nghiệm' in title_lower or 'trac nghiem' in title_lower:
                current_section = 'ex'
                
            handle_transition(title)
                
            if level == 1:
                body_lines.append(f'\\begin{{center}}\\bf\\Large {title} \\end{{center}}')
            elif level == 2:
                body_lines.append(f'\\subsection*{{{title}}}')
            else:
                body_lines.append(f'\\subsubsection*{{{title}}}')
                
        elif el['type'] == 'text':
            content_clean = convert_math_delimiters(clean_vietnamese_text(el['content']))
            if content_clean:
                if not content_clean.startswith('\\'):
                    content_clean = content_clean + r'\par'
                body_lines.append(content_clean)
                
        elif el['type'] == 'question':
            q_num = el['number']
            q_lines = el['lines']
            
            ans_val = None
            loigiai_lines = []
            stem_lines = []
            
            is_loigiai = False
            for line in q_lines:
                line_str = line.strip()
                if not line_str:
                    continue
                ans_match = re.match(r'^(?:Đáp số|Đáp án)\s*[:\-\s]\s*(.*)$', line_str, re.IGNORECASE)
                if ans_match:
                    ans_val = ans_match.group(1).strip()
                    if ans_val.endswith('.'):
                        ans_val = ans_val[:-1].strip()
                    continue
                if line_str.lower() in ['lời giải', 'loigiai', 'hướng dẫn giải', 'huong dan giai']:
                    is_loigiai = True
                    continue
                if is_loigiai:
                    loigiai_lines.append(line)
                else:
                    stem_lines.append(line)
            
            stem_text = '\n'.join(stem_lines)
            
            # Check for inline section headers in stem
            stem_text, inline_hdr = extract_inline_header(stem_text)
            
            # Auto-insert images
            image_tex = []
            padded_q_num = f"{q_num:02d}"
            for img_file in sorted(os.listdir(images_dir)):
                if img_file.startswith(f"{slug}_cau{padded_q_num}_") and img_file.endswith('.jpg'):
                    image_tex.append(f'\\begin{{center}}\\includegraphics[width=0.5\\linewidth]{{Images/{img_file}}}\\end{{center}}')
            
            if image_tex:
                stem_text += '\n' + '\n'.join(image_tex)
                
            # Parse multiple choice: select last 4 matches in order A, B, C, D
            all_mc_matches = list(CHOICE_RE.finditer(stem_text))
            mc_matches = []
            is_mc = False
            if len(all_mc_matches) >= 4:
                last_four = all_mc_matches[-4:]
                labels = [m.group(1) for m in last_four]
                if labels == ['A', 'B', 'C', 'D']:
                    mc_matches = last_four
                    is_mc = True
                
            # Parse true/false: select last 4 matches in order a, b, c, d
            all_tf_matches = list(TF_RE.finditer(stem_text))
            tf_matches = []
            is_tf = False
            if len(all_tf_matches) >= 4:
                last_four = all_tf_matches[-4:]
                labels = [m.group(1) for m in last_four]
                if labels == ['a', 'b', 'c', 'd']:
                    tf_matches = last_four
                    is_tf = True
            
            content_tex = ""
            loigiai_tex = ""
            
            if current_section == 'bt':
                content_tex = format_essay_question(stem_text, ans_val)
                loigiai_tex = '\n'.join(loigiai_lines)
            elif is_tf:
                tf_stem = stem_text[:tf_matches[0].start()].strip()
                statements = []
                for j, match in enumerate(tf_matches):
                    start = match.end()
                    end = tf_matches[j + 1].start() if j + 1 < len(tf_matches) else len(stem_text)
                    st_text = stem_text[start:end].strip()
                    if j == 3:
                        st_text, inline_hdr_tf = extract_inline_header(st_text)
                        if inline_hdr_tf:
                            inline_hdr = inline_hdr_tf
                    statements.append(st_text)
                    
                ans_list = None
                if slug == '10-hsg-tran-bien-2026-azota':
                    ans_list = TRAN_BIEN_TF_KEYS.get(q_num)
                else:
                    old_ans = answers_map.get(q_num)
                    if old_ans and old_ans['type'] == 'choiceTF':
                        ans_list = old_ans['answers']
                
                content_tex, itemchoice_sol = format_question_tf(tf_stem, statements, ans_list)
                if loigiai_lines:
                    loigiai_tex = '\n'.join(loigiai_lines) + '\n' + itemchoice_sol
                else:
                    loigiai_tex = itemchoice_sol
            elif is_mc:
                mc_stem = stem_text[:mc_matches[0].start()].strip()
                choices = []
                for j, match in enumerate(mc_matches):
                    start = match.end()
                    end = mc_matches[j + 1].start() if j + 1 < len(mc_matches) else len(stem_text)
                    ch_text = mc_matches[j].group(0) + stem_text[start:end].strip()
                    if j == 3:
                        ch_text, inline_hdr_mc = extract_inline_header(ch_text)
                        if inline_hdr_mc:
                            inline_hdr = inline_hdr_mc
                    ch_stripped = re.sub(r'^[A-D]\s*[\.\)\:]\s*', '', ch_text).strip()
                    choices.append(ch_stripped)
                    
                correct_idx = -1
                old_ans = answers_map.get(q_num)
                if old_ans and old_ans['type'] == 'choice':
                    correct_idx = old_ans['answers']
                    
                content_tex = format_question_choices(mc_stem, choices, correct_idx)
                loigiai_tex = '\n'.join(loigiai_lines)
            else:
                if slug == '10-hsg-tran-bien-2026-azota':
                    if q_num == 27: ans_val = "26.5"
                    elif q_num == 28: ans_val = "0.25"
                    elif q_num == 29: ans_val = "349"
                    elif q_num == 30: ans_val = "2"
                elif slug == 'de-01':
                    if q_num == 7: ans_val = "0.69"
                    elif q_num == 8: ans_val = "120; 240"
                    elif q_num == 10: ans_val = "28"
                elif slug == 'de-3-hsg':
                    if q_num == 7: ans_val = "1"
                    elif q_num == 8: ans_val = "225; 300"
                    elif q_num == 9: ans_val = "6"
                    elif q_num == 10: ans_val = "60"
                elif slug == 'cau-truc-de-thi-hsg-10':
                    if q_num == 27: ans_val = "4"
                    elif q_num == 28: ans_val = "2.68"
                    elif q_num == 29: ans_val = "1/3"
                    elif q_num == 30: ans_val = "-0.6"
                    
                if ans_val:
                    content_tex = format_question_short(stem_text, ans_val)
                else:
                    content_tex = convert_math_delimiters(clean_vietnamese_text(stem_text))
                    
                loigiai_tex = '\n'.join(loigiai_lines)
                
            q_env = current_section
            body_lines.append(f'\\begin{{{q_env}}}')
            body_lines.append(content_tex)
            body_lines.append(f'\\loigiai{{{loigiai_tex.strip()}}}')
            body_lines.append(f'\\end{{{q_env}}}')
            
            if inline_hdr:
                hdr_lower = inline_hdr.lower()
                if 'tự luận' in hdr_lower or 'tu luan' in hdr_lower:
                    current_section = 'bt'
                elif 'trắc nghiệm' in hdr_lower or 'trac nghiem' in hdr_lower:
                    current_section = 'ex'
                
                handle_transition(inline_hdr)
                body_lines.append(f'\\subsection*{{{inline_hdr}}}')
            
    if opened_ans:
        body_lines.append(r'\Closesolutionfile{ans}')
        opened_ans = False
        
    body_lines += [
        r'\begin{center}\bf\Large BẢNG ĐÁP ÁN \end{center}',
        r'\noindent\textbf{A. ĐÁP ÁN PHẦN I}',
        r'\inputansbox{6}{ans/ans-phanI}',
        r'\vspace{0.5cm}',
        r'\noindent\textbf{B. ĐÁP ÁN PHẦN II}',
        r'\inputansbox{3}{ans/ans-phanII}',
        r'\vspace{0.5cm}',
        r'\noindent\textbf{C. ĐÁP ÁN PHẦN III}',
        r'\inputansbox{6}{ans/ans-phanIII}'
    ]
    
    target_dir = OUTPUT_DIR / slug
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / 'ans').mkdir(parents=True, exist_ok=True)
    (target_dir / 'Images').mkdir(parents=True, exist_ok=True)
    
    for img_file in os.listdir(images_dir):
        if img_file.startswith(f"{slug}_") and img_file.endswith('.jpg'):
            shutil.copy2(images_dir / img_file, target_dir / 'Images' / img_file)
            
    sty_src = EXAMPLE_DIR / 'ex_test.sty'
    if sty_src.exists():
        shutil.copy2(sty_src, target_dir / 'ex_test.sty')
        
    # Write the body file
    body_path = target_dir / f"{slug}-body.tex"
    with open(body_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(body_lines) + '\n')
    print(f"Successfully wrote {body_path}!")
    
    # Write de-thi.tex
    dethi_preamble = preamble_lines[:5] + [r'\usepackage[dethi]{ex_test}'] + preamble_lines[5:]
    dethi_content = '\n'.join(dethi_preamble) + f"\n\\begin{{document}}\n\\hideans\n\\input{{{slug}-body.tex}}\n\\end{{document}}\n"
    with open(target_dir / "de-thi.tex", 'w', encoding='utf-8') as f:
        f.write(dethi_content)
        
    # Write de-va-loigiai.tex
    loigiai_preamble = preamble_lines[:5] + [r'\usepackage[solcolor]{ex_test}'] + preamble_lines[5:]
    loigiai_content = '\n'.join(loigiai_preamble) + f"\n\\begin{{document}}\n\\input{{{slug}-body.tex}}\n\\end{{document}}\n"
    with open(target_dir / "de-va-loigiai.tex", 'w', encoding='utf-8') as f:
        f.write(loigiai_content)
        
    # Write dap-an.tex
    dapan_content = f"""\\documentclass[12pt,a4paper,oneside]{{article}}
\\usepackage[top=2cm, bottom=2cm, left=1.5cm, right=1.5cm]{{geometry}}
\\usepackage{{amsmath, amssymb}}
\\usepackage[color]{{ex_test}}

\\begin{{document}}
\\begin{{center}}\\bf\\Large
BẢNG ĐÁP ÁN
\\end{{center}}
\\noindent\\textbf{{A. ĐÁP ÁN PHẦN I}}
\\inputansbox{{6}}{{ans/ans-phanI}}
\\vspace{{0.5cm}}

\\noindent\\textbf{{B. ĐÁP ÁN PHẦN II}}
\\inputansbox{{3}}{{ans/ans-phanII}}
\\vspace{{0.5cm}}

\\noindent\\textbf{{C. ĐÁP ÁN PHẦN III}}
\\inputansbox{{6}}{{ans/ans-phanIII}}
\\end{{document}}
"""
    with open(target_dir / "dap-an.tex", 'w', encoding='utf-8') as f:
        f.write(dapan_content)

def main():
    images_dir = SOURCE_DIR / 'images'
    if not images_dir.exists():
        print(f"Error: Images directory {images_dir} not found.")
        sys.exit(1)
        
    mappings = {
        'de-01': 'de_hsg12_so1.md',
        'de-3-hsg': 'de_hsg12_so2.md',
        '10-hsg-tran-bien-2026-azota': 'de_hsg10_so3_tracnghiem.md',
        'cau-truc-de-thi-hsg-10': 'cautrucdethihsg10.md'
    }
    
    for slug, md_name in mappings.items():
        old_tex_path = OUTPUT_DIR / slug / f"{slug}.tex"
        answers_map = extract_answers_from_old_tex(old_tex_path)
        print(f"Extracted {len(answers_map)} answers from old {slug}.tex")
        process_file(slug, md_name, answers_map, images_dir)
        
    print("\nAll conversions completed successfully!")

if __name__ == '__main__':
    main()
