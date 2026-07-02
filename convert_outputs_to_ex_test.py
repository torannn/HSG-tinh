import html
import json
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / 'pdf_to_tex_outputs'
EXAMPLE_DIR = ROOT / 'ex_test'
OUTPUT_DIR = ROOT / 'generated_ex_test'

QUESTION_START_RE = re.compile(r'^(?:Câu|Cau)\s*(\d+)\s*[:\.]?\s*(.*)$', re.IGNORECASE)
MD_IMAGE_RE = re.compile(r'!\[[^\]]*\]\(([^)]+)\)')
MATH_RE = re.compile(r'(\$\$.*?\$\$|\$.*?\$|\\\[.*?\\\]|\\\(.*?\\\))', re.DOTALL)
CHOICE_RE = re.compile(r'(?<![\w\\])([A-D])\s*[\.]\s*')
HTML_TABLE_RE = re.compile(r'<table.*?</table>', re.IGNORECASE | re.DOTALL)

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.current_row = None
        self.current_cell = None

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'tr':
            self.current_row = []
        elif tag.lower() in {'td', 'th'} and self.current_row is not None:
            self.current_cell = []

    def handle_endtag(self, tag):
        if tag.lower() in {'td', 'th'} and self.current_cell is not None:
            self.current_row.append(html.unescape(''.join(self.current_cell)).strip())
            self.current_cell = None
        elif tag.lower() == 'tr' and self.current_row is not None:
            self.rows.append(self.current_row)
            self.current_row = None

    def handle_data(self, data):
        if self.current_cell is not None:
            self.current_cell.append(data)

def escape_tex_text(s):
    repl = {
        '&': r'\&',
        '%': r'\%',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '−': '-',
        '–': '-',
        '—': '-',
        '': '<',
        '': r"'",
        '': r'$^\circ$',
        '°': r'$^\circ$',
    }
    return ''.join(repl.get(ch, ch) for ch in s)

def inline_md_to_tex(line):
    line = line.replace('**', '')
    parts = MATH_RE.split(line)
    out = []
    for part in parts:
        if not part:
            continue
        out.append(part if MATH_RE.fullmatch(part) else escape_tex_text(part))
    return ''.join(out)

def html_table_to_tex(match):
    parser = TableParser()
    parser.feed(match.group(0))
    rows = [row for row in parser.rows if row]
    if not rows:
        return ''
    width = max(len(row) for row in rows)
    spec = '|' + '|'.join(['c'] * width) + '|'
    tex_rows = [r'\begin{center}', r'\begin{tabular}{' + spec + '}', r'\hline']
    for row in rows:
        padded = row + [''] * (width - len(row))
        tex_rows.append(' & '.join(inline_md_to_tex(cell) for cell in padded) + r' \\')
        tex_rows.append(r'\hline')
    tex_rows += [r'\end{tabular}', r'\end{center}']
    return '\n'.join(tex_rows)

def replace_tables(text):
    return HTML_TABLE_RE.sub(html_table_to_tex, text)

def normalize_image_path(src):
    name = Path(src).name
    return 'Images/' + name

def convert_images(line):
    def repl(match):
        return '\n'.join([
            r'\begin{center}',
            r'\includegraphics[width=0.82\linewidth]{' + normalize_image_path(match.group(1)) + '}',
            r'\end{center}',
        ])
    return MD_IMAGE_RE.sub(repl, line)

def split_questions(markdown):
    preface = []
    questions = []
    current = None
    text = replace_tables(markdown)
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            if current is not None:
                current['lines'].append('')
            continue
        match = QUESTION_START_RE.match(line)
        if match:
            if current is not None:
                questions.append(current)
            current = {'number': match.group(1), 'lines': [match.group(2).strip()] if match.group(2).strip() else []}
        elif current is not None:
            current['lines'].append(line)
        else:
            preface.append(line)
    if current is not None:
        questions.append(current)
    return preface, questions

def md_heading_to_tex(line):
    if line.startswith('###'):
        return r'\subsubsection*{' + inline_md_to_tex(line.lstrip('#').strip()) + '}'
    if line.startswith('##'):
        return r'\subsection*{' + inline_md_to_tex(line.lstrip('#').strip()) + '}'
    if line.startswith('#'):
        return r'\section*{' + inline_md_to_tex(line.lstrip('#').strip()) + '}'
    return inline_md_to_tex(line) + r'\par'

def is_raw_tex_line(line):
    stripped = line.strip()
    if stripped.startswith((r'\begin{', r'\end{', r'\hline')):
        return True
    if ' & ' in stripped and stripped.endswith(r'\\'):
        return True
    return False

def split_choices_from_line(line):
    matches = list(CHOICE_RE.finditer(line))
    labels = [m.group(1) for m in matches]
    if labels != ['A', 'B', 'C', 'D']:
        return None
    stem = line[:matches[0].start()].strip()
    choices = []
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(line)
        choices.append(line[start:end].strip())
    if not all(choices):
        return None
    return stem, choices

def question_to_tex(question):
    body = []
    first_text_done = False
    for raw in question['lines']:
        line = convert_images(raw.strip())
        if not line:
            body.append('')
            continue
        if is_raw_tex_line(line):
            body.append(line)
            continue
        parsed = split_choices_from_line(line)
        if parsed:
            stem, choices = parsed
            if stem:
                body.append(inline_md_to_tex(stem) + r'\\')
            body.append(r'\choice')
            for choice in choices:
                body.append('{' + inline_md_to_tex(choice) + '}')
            first_text_done = True
            continue
        if line.startswith('#'):
            body.append(md_heading_to_tex(line))
            continue
        suffix = r'\\' if not first_text_done else r'\par'
        body.append(inline_md_to_tex(line) + suffix)
        first_text_done = True
    return '\n'.join([r'\begin{ex}'] + body + [r'\loigiai{}', r'\end{ex}'])

def document_title(preface, slug):
    for line in preface:
        if line.startswith('#'):
            return line.lstrip('#').strip()
    return slug.replace('-', ' ').title()

def render_document(slug, markdown):
    preface, questions = split_questions(markdown)
    title = document_title(preface, slug)
    lines = [
        r'\documentclass[12pt,a4paper,oneside]{article}',
        r'\usepackage[top=2cm, bottom=2cm, left=1.5cm, right=1.5cm]{geometry}',
        r'\usepackage{amsmath, amssymb, fancyhdr}',
        r'\usepackage{tkz-euclide,tikz-3dplot,tikz,tkz-tab}',
        r'\usepackage{fontawesome5}',
        r'\usepackage[dethi]{ex_test}',
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
        r'\begin{document}',
        r'\OPTN{kindTF=t, kindSA=}',
        r'\def\SSS{}',
        r'\Opensolutionfile{ansbook}[ans/ansbook]',
        r'\Opensolutionfile{ans}[ans/ans]',
        r'\OPTN{kindDrag=1}',
        r'\begin{center}\bf\Large',
        inline_md_to_tex(title),
        r'\end{center}',
    ]
    for line in preface:
        if line.startswith('#'):
            continue
        if line:
            lines.append(md_heading_to_tex(line))
    for question in questions:
        lines.append(question_to_tex(question))
    lines += [
        r'\Closesolutionfile{ans}',
        r'\Closesolutionfile{ansbook}',
        r'\begin{center}\bf\Large',
        r'BẢNG ĐÁP ÁN',
        r'\end{center}',
        r'\inputansbox[0]{7}{ans/ans.tex}',
        r'\end{document}',
    ]
    return '\n'.join(lines) + '\n'

def copy_images_for_slug(slug, target_images):
    source_images = SOURCE_DIR / 'images'
    if not source_images.exists():
        return 0
    count = 0
    for image in source_images.iterdir():
        if image.is_file() and image.name.startswith(slug + '_'):
            shutil.copy2(image, target_images / image.name)
            count += 1
    return count

def convert_all():
    markdown_dir = SOURCE_DIR / 'markdown'
    if not markdown_dir.exists():
        raise FileNotFoundError(markdown_dir)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = []
    for md_path in sorted(markdown_dir.glob('*.md')):
        slug = md_path.stem
        target_dir = OUTPUT_DIR / slug
        target_images = target_dir / 'Images'
        target_ans = target_dir / 'ans'
        target_images.mkdir(parents=True, exist_ok=True)
        target_ans.mkdir(parents=True, exist_ok=True)
        sty_src = EXAMPLE_DIR / 'ex_test.sty'
        if sty_src.exists():
            shutil.copy2(sty_src, target_dir / 'ex_test.sty')
        markdown = md_path.read_text(encoding='utf-8', errors='ignore')
        tex = render_document(slug, markdown)
        tex_path = target_dir / (slug + '.tex')
        tex_path.write_text(tex, encoding='utf-8')
        (target_ans / 'ans.tex').write_text('', encoding='utf-8')
        (target_ans / 'ansbook.tex').write_text('', encoding='utf-8')
        image_count = copy_images_for_slug(slug, target_images)
        question_count = len(split_questions(markdown)[1])
        summary.append({'slug': slug, 'tex': str(tex_path), 'questions': question_count, 'images': image_count})
    (OUTPUT_DIR / 'conversion_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    return summary

if __name__ == '__main__':
    for row in convert_all():
        print(f"{row['slug']}: {row['questions']} questions, {row['images']} images -> {row['tex']}")
