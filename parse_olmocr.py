import os
import re
import sys
import shutil
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / 'generated_ex_test' / 'hsg-12-khao-sat-ham-so'
INPUT_FILE = ROOT / 'olmocr.md'

# Danh sách các theme và cấu hình chi tiết có thể tự do tùy biến (customizable)
# Nếu có file styles_config.json của ứng dụng GUI, chương trình sẽ tự động ưu tiên nạp từ đó.
STYLES = {
    'blue-pink': {
        'primary': '0, 102, 204',       # Xanh biển đậm
        'accent': '204, 0, 102',        # Hồng tím
        'use_custom_shapes': True,
        'correct_choice_shape': 'rectangle',
        'incorrect_choice_shape': 'circle',
        'question_symbol': r'\faPen',
        'book_symbol': r'\faBook',
        'solution_title_symbol': r'\faLightbulb',
        'hand_pointing_symbol': r'\faHandPointRight',
        'math_font': 'default',
        'color_formulas': 'none',
        'main_font': 'default',
        'page_header_style': 'none',
        'page_footer_style': 'none',
        'question_label_style': 'standard',
        'header_banner_text': 'LỚP TOÁN THẦY HOÀNG',
        'footer_copyright_text': '© 2026 Bản quyền thuộc về tác giả. All rights reserved.',
        'watermark_text': '',
        'watermark_opacity': '0.06',
        'hide_id': False,
    },
    'hoang-decor': {
        'primary': '30, 58, 138',       # Xanh navy đậm
        'accent': '219, 39, 119',       # Hồng đậm cá tính
        'use_custom_shapes': True,
        'correct_choice_shape': 'yellow-circle', # Đáp án Đúng: tròn vàng như ảnh
        'incorrect_choice_shape': 'yellow-circle', # Các đáp án trắc nghiệm: tròn vàng
        'question_symbol': 'none',
        'book_symbol': 'none',
        'solution_title_symbol': r'\faLightbulb',
        'hand_pointing_symbol': r'\faHandPointRight',
        'math_font': 'default',
        'color_formulas': 'none',
        'main_font': 'opensans',        # Open Sans tiếng Việt cực đẹp
        'page_header_style': 'hoang-decor',
        'page_footer_style': 'hoang-decor',
        'question_label_style': 'boxed', # Hộp câu hỏi bo tròn
        'header_banner_text': 'Lớp Toán thầy Hoàng - ĐỀ KIỂM TRA ĐỊNH KỲ',
        'footer_copyright_text': '© 2026 Bản quyền thuộc về tác giả. All rights reserved.',
        'watermark_text': '',
        'watermark_opacity': '0.06',
        'hide_id': False,
    },
    'elegant-book': {
        'primary': '21, 128, 61',       # Xanh lá cây thông
        'accent': '180, 83, 9',         # Hổ phách/Vàng đồng cổ điển
        'use_custom_shapes': True,
        'correct_choice_shape': 'rectangle',
        'incorrect_choice_shape': 'none',
        'question_symbol': r'\faCheck',
        'book_symbol': r'\faBook',
        'solution_title_symbol': r'\faLightbulb',
        'hand_pointing_symbol': r'\faHandPointRight',
        'math_font': 'mathpazo',        # Font toán Palatino
        'color_formulas': 'myprimary',
        'main_font': 'tgpagella',       # TeX Gyre Pagella tiếng Việt rất đẹp
        'page_header_style': 'minimal',  # Khung header mỏng
        'page_footer_style': 'minimal',  # Khung footer mỏng
        'question_label_style': 'standard',
        'header_banner_text': 'Lớp Toán thầy Hoàng - ĐỀ KHẢO SÁT CHẤT LƯỢNG MÔN TOÁN',
        'footer_copyright_text': 'Tài liệu lưu hành nội bộ - THPT Chuyên Quốc Học',
        'watermark_text': '',
        'watermark_opacity': '0.06',
        'hide_id': False,
    },
    'cyberpunk': {
        'primary': '6, 182, 212',       # Cyan sáng công nghệ
        'accent': '168, 85, 247',       # Tím sáng Neon
        'use_custom_shapes': True,
        'correct_choice_shape': 'rectangle',
        'incorrect_choice_shape': 'circle',
        'question_symbol': r'\faTerminal',
        'book_symbol': r'\faCode',
        'solution_title_symbol': r'\faKey',
        'hand_pointing_symbol': r'\faAngleRight',
        'math_font': 'arev',            # Font toán không chân Sans-serif Arev
        'color_formulas': 'myprimary',
        'main_font': 'tgheros',         # Helvetica tiếng Việt không chân cực hiện đại
        'page_header_style': 'minimal',
        'page_footer_style': 'minimal',
        'question_label_style': 'boxed',
        'header_banner_text': 'LỚP TOÁN THẦY HOÀNG - MOCK ONLINE TEST',
        'footer_copyright_text': 'Designed with LaTeX & TikZ Cyber Theme',
        'watermark_text': '',
        'watermark_opacity': '0.06',
        'hide_id': False,
    },
    'teal-orange': {
        'primary': '0, 128, 128',
        'accent': '230, 115, 0',
        'use_custom_shapes': True,
        'correct_choice_shape': 'circle',
        'incorrect_choice_shape': 'circle',
        'question_symbol': r'\faEdit',
        'book_symbol': r'\faGraduationCap',
        'solution_title_symbol': r'\faKey',
        'hand_pointing_symbol': r'\faCheck',
        'math_font': 'default',
        'color_formulas': 'none',
        'main_font': 'default',
        'page_header_style': 'none',
        'page_footer_style': 'none',
        'question_label_style': 'standard',
        'header_banner_text': 'LỚP TOÁN THẦY HOÀNG - KIỂM TRA ĐỊNH KỲ',
        'footer_copyright_text': '© 2026 Bản quyền thuộc về tác giả. All rights reserved.',
        'watermark_text': '',
        'watermark_opacity': '0.06',
        'hide_id': False,
    },
    'violet-emerald': {
        'primary': '102, 0, 204',
        'accent': '0, 153, 76',
        'use_custom_shapes': True,
        'correct_choice_shape': 'rectangle',
        'incorrect_choice_shape': 'none',
        'question_symbol': r'\faQuestionCircle',
        'book_symbol': r'\faBook',
        'solution_title_symbol': r'\faCommentDots',
        'hand_pointing_symbol': r'\faArrowRight',
        'math_font': 'eulervm',
        'color_formulas': 'myprimary',
        'main_font': 'default',
        'page_header_style': 'none',
        'page_footer_style': 'none',
        'question_label_style': 'standard',
        'header_banner_text': 'LỚP TOÁN THẦY HOÀNG - KIỂM TRA GIỮA HỌC KỲ I',
        'footer_copyright_text': '© 2026 Bản quyền thuộc về tác giả. All rights reserved.',
        'watermark_text': '',
        'watermark_opacity': '0.06',
        'hide_id': False,
    },
    'classic': {
        'primary': '0, 0, 0',
        'accent': '204, 0, 0',
        'use_custom_shapes': False,
        'correct_choice_shape': 'none',
        'incorrect_choice_shape': 'none',
        'question_symbol': '',
        'book_symbol': '',
        'solution_title_symbol': '',
        'hand_pointing_symbol': '',
        'math_font': 'default',
        'color_formulas': 'none',
        'main_font': 'default',
        'page_header_style': 'none',
        'page_footer_style': 'none',
        'question_label_style': 'standard',
        'header_banner_text': 'LỚP TOÁN THẦY HOÀNG - KIỂM TRA GIỮA HỌC KỲ I',
        'footer_copyright_text': '© 2026 Bản quyền thuộc về tác giả. All rights reserved.',
        'watermark_text': '',
        'watermark_opacity': '0.06',
        'hide_id': False,
    }
}

# Nạp cấu hình styles từ tệp JSON ngoài nếu có để tương tác với GUI
STYLE_CONFIG_PATH = ROOT / 'styles_config.json'
if STYLE_CONFIG_PATH.exists():
    try:
        with open(STYLE_CONFIG_PATH, 'r', encoding='utf-8') as f:
            STYLES.update(json.load(f))
    except Exception as e:
        print(f"Warning: Không thể tải styles_config.json ({e})")

# Theme mặc định (có thể đổi tên theme tại đây hoặc truyền qua đối số dòng lệnh)
DEFAULT_STYLE = 'blue-pink'

# Regular expressions
QUESTION_START_RE = re.compile(r'^Câu\s*(\d+)[\.:]?\s*(.*)$', re.IGNORECASE)
CHOICE_LABEL_RE = re.compile(r'(?<![\w\\\(\[\{])([A-D])\s*[\.\)\:]\s*')
TF_LABEL_RE = re.compile(r'(?<![\w\\\(\[\{])([a-d])\s*[\.\)\:]\s*')
ORIGIN_PREFIX_RE = re.compile(r'^(\s*(?:\([^)]+\)|\[[^\]]+\])\s*)')

def generate_preamble(style_name, doc_type):
    config = STYLES.get(style_name, STYLES[DEFAULT_STYLE])
    primary_rgb = config['primary']
    accent_rgb = config['accent']
    use_shapes = config['use_custom_shapes']
    
    # Custom parameters
    correct_shape = config.get('correct_choice_shape', 'rectangle')
    incorrect_shape = config.get('incorrect_choice_shape', 'circle')
    correct_tf_shape = config.get('correct_tf_shape', 'rectangle')
    correct_sa_shape = config.get('correct_sa_shape', 'rectangle')
    auto_wrap_anstab = config.get('auto_wrap_anstab', True)
    prevent_overflow_ansbox = config.get('prevent_overflow_ansbox', True)
    sa_height = config.get('sa_height', 0.9)
    q_symbol = config.get('question_symbol', r'\faPen')
    b_symbol = config.get('book_symbol', r'\faBook')
    sol_symbol = config.get('solution_title_symbol', r'\faLightbulb')
    hand_symbol = config.get('hand_pointing_symbol', r'\faHandPointRight')
    math_font = config.get('math_font', 'default')
    color_formulas = config.get('color_formulas', 'none')

    # New custom parameters from HuongDanExTest
    question_text = config.get('question_text', 'Câu').replace('&', r'\&')
    book_text = config.get('book_text', 'Bài tự luận').replace('&', r'\&')
    
    parskip_choice = str(config.get('parskip_choice', '2'))
    if not parskip_choice.endswith(('mm', 'cm', 'pt', 'in', 'ex', 'em')):
        parskip_choice += 'mm'

    # Font & Style Customizations
    main_font = config.get('main_font', 'default')
    page_header_style = config.get('page_header_style', 'none')
    page_footer_style = config.get('page_footer_style', 'none')
    question_label_style = config.get('question_label_style', 'standard')
    header_banner_text = config.get('header_banner_text', 'KIỂM TRA GIỮA HỌC KỲ I - THPT 2026').replace('&', r'\&')
    footer_copyright_text = config.get('footer_copyright_text', '© 2026 Bản quyền thuộc về tác giả. All rights reserved.').replace('&', r'\&')
    watermark_text = config.get('watermark_text', '').replace('&', r'\&')
    watermark_opacity = config.get('watermark_opacity', '0.06')

    # Tránh ký tự double backslash từ JSON
    if q_symbol: q_symbol = q_symbol.replace('\\\\', '\\')
    if b_symbol: b_symbol = b_symbol.replace('\\\\', '\\')
    if sol_symbol: sol_symbol = sol_symbol.replace('\\\\', '\\')
    if hand_symbol: hand_symbol = hand_symbol.replace('\\\\', '\\')

    # Format symbols
    q_prefix = f"{q_symbol}\\ " if q_symbol and q_symbol != 'none' else ""
    b_prefix = f"{b_symbol}\\ " if b_symbol and b_symbol != 'none' else ""
    sol_prefix = f"{sol_symbol}\\ " if sol_symbol and sol_symbol != 'none' else ""
    hand_prefix = f"{hand_symbol}\\ " if hand_symbol and hand_symbol != 'none' else ""

    font_package = ""
    # Main document font
    if main_font != 'default':
        font_package += r"\usepackage[T5]{fontenc}" + "\n"
        if main_font == 'tgschola':
            font_package += r"\IfFileExists{tgschola.sty}{\usepackage{tgschola}}{}" + "\n"
        elif main_font == 'tgtermes':
            font_package += r"\IfFileExists{tgtermes.sty}{\usepackage{tgtermes}}{}" + "\n"
        elif main_font == 'tgpagella':
            font_package += r"\IfFileExists{tgpagella.sty}{\usepackage{tgpagella}}{}" + "\n"
        elif main_font == 'tgheros':
            font_package += r"\IfFileExists{tgheros.sty}{\usepackage[scale=0.9]{tgheros}\renewcommand{\familydefault}{\sfdefault}}{\usepackage{helvet}\renewcommand{\familydefault}{\sfdefault}}" + "\n"
        elif main_font == 'opensans':
            font_package += r"\IfFileExists{opensans.sty}{\usepackage[default]{opensans}}{\usepackage{helvet}\renewcommand{\familydefault}{\sfdefault}}" + "\n"
        elif main_font == 'notosans':
            font_package += r"\IfFileExists{noto.sty}{\usepackage[sfdefault]{noto}}{\usepackage{helvet}\renewcommand{\familydefault}{\sfdefault}}" + "\n"
        elif main_font == 'arev':
            font_package += r"\IfFileExists{arevtext.sty}{\usepackage{arev}}{\usepackage{helvet}\renewcommand{\familydefault}{\sfdefault}}" + "\n"
        elif main_font == 'fourier':
            font_package += r"\IfFileExists{fourier.sty}{\usepackage{fourier}}{}" + "\n"

    # Math font package
    if math_font == 'mathptmx':
        font_package += r"\IfFileExists{mathptmx.sty}{\usepackage{mathptmx}}{}" + "\n"
    elif math_font == 'mathpazo':
        font_package += r"\IfFileExists{mathpazo.sty}{\usepackage{mathpazo}}{}" + "\n"
    elif math_font == 'fourier' and main_font != 'fourier':
        font_package += r"\IfFileExists{fourier.sty}{\usepackage{fourier}}{}" + "\n"
    elif math_font == 'eulervm':
        font_package += r"\IfFileExists{eulervm.sty}{\usepackage[euler-digits,euler-hat-accent]{eulervm}}{}" + "\n"
    elif math_font == 'arev' and main_font != 'arev':
        font_package += r"\IfFileExists{arevtext.sty}{\usepackage{arev}}{}" + "\n"
    elif math_font == 'charter':
        font_package += r"\IfFileExists{mathdesign.sty}{\usepackage[charter]{mathdesign}}{}" + "\n"

    # Margin settings depending on header/footer style
    if page_header_style == 'hoang-decor' or page_footer_style == 'hoang-decor':
        geom_opts = "top=3.2cm, bottom=2.8cm, left=1.5cm, right=1.5cm, headheight=2.5cm, headsep=0.3cm, footskip=1.5cm"
    elif page_header_style in ['minimal', 'accent-bar', 'double-line'] or page_footer_style in ['minimal', 'accent-bar', 'double-line']:
        geom_opts = "top=2.8cm, bottom=2.5cm, left=1.5cm, right=1.5cm, headheight=1.5cm, headsep=0.4cm, footskip=1.2cm"
    else:
        geom_opts = "top=2cm, bottom=2cm, left=1.5cm, right=1.5cm"


    # Font size customization
    global_font_size = config.get('global_font_size', '12pt')
    if global_font_size not in ['10pt', '11pt', '12pt']:
        global_font_size = '12pt'
        
    two_columns = config.get('two_columns', False)
    if two_columns and doc_type == 'de-thi':
        if global_font_size == '12pt':
            global_font_size = '11pt'

    common_start = f"""\\documentclass[{global_font_size},a4paper,oneside]{{article}}
\\usepackage[{geom_opts}]{{geometry}}
\\usepackage{{amsmath, amssymb}}
"""
    if font_package:
        common_start += font_package + "\n"

    common_start += r"""\usepackage{ifthen}
\usepackage{tkz-euclide,tikz-3dplot,tikz,tkz-tab}
\usepackage{fontawesome5}
"""
    
    if doc_type == 'de-thi':
        common_start += r"\usepackage[dethi]{ex_test}" + "\n"
    else:
        common_start += r"\usepackage[solcolor]{ex_test}" + "\n"

    common_end = r"""\usetikzlibrary{shapes.geometric,arrows,decorations.pathmorphing,calc,intersections,angles}
\usepackage{pgfplots}
\usepgfplotslibrary{fillbetween}
\pgfplotsset{compat=1.9}
\usepackage[hidelinks,unicode]{hyperref}
\usepackage{esvect}
\usepackage{multicol}

\def\vec{\vv}
\def\overrightarrow{\vv}
\newcommand{\hoac}[1]{\left[\begin{aligned}#1\end{aligned}\right.}
\newcommand{\heva}[1]{\left\{\begin{aligned}#1\end{aligned}\right.}
\renewcommand{\baselinestretch}{1.2}

% Định nghĩa màu sắc theo theme
\definecolor{myprimary}{RGB}{__PRIMARY_RGB__}
\definecolor{myaccent}{RGB}{__ACCENT_RGB__}
\definecolor{blue}{RGB}{__PRIMARY_RGB__}
\definecolor{red}{RGB}{__ACCENT_RGB__}
"""

    # Formula coloring definition
    color_formula_def = ""
    if color_formulas != 'none':
        if color_formulas == 'myprimary':
            color_formula_def = r"""
\everymath{\color{myprimary}}
\everydisplay{\color{myprimary}}
"""
        elif color_formulas == 'myaccent':
            color_formula_def = r"""
\everymath{\color{myaccent}}
\everydisplay{\color{myaccent}}
"""
        else:
            # Custom RGB color like '0, 102, 204'
            color_formula_def = f"""
\\definecolor{{mathcolor}}{{RGB}}{{{color_formulas}}}
\\everymath{{\\color{{mathcolor}}}}
\\everydisplay{{\\color{{mathcolor}}}}
"""
    if color_formula_def:
        common_end += color_formula_def + "\n"

    # Header and Footer layout snippet
    header_footer_defs = ""
    has_fancy = page_header_style in ['hoang-decor', 'minimal', 'accent-bar', 'double-line'] or \
                 page_footer_style in ['hoang-decor', 'minimal', 'accent-bar', 'double-line']
                 
    if has_fancy:
        header_footer_defs += r"""
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
"""
        # Header configurations
        if page_header_style == 'hoang-decor':
            header_footer_defs += r"\renewcommand{\headrulewidth}{0pt}" + "\n"
            header_footer_defs += f"""
\\newcommand{{\\drawheader}}{{%
  \\begin{{tikzpicture}}[remember picture, overlay]
    \\fill[color=myprimary] (current page.north west) rectangle ([yshift=-2.2cm]current page.north east);
    \\fill[color=myaccent] ([yshift=-2.2cm]current page.north west) rectangle ([yshift=-2.3cm]current page.north east);
    \\fill[color=myaccent!45, opacity=0.7] ([xshift=-1.5cm, yshift=-1.1cm]current page.north east) circle (0.8cm);
    \\fill[color=yellow!60, opacity=0.5] ([xshift=-0.5cm, yshift=-1.5cm]current page.north east) circle (0.6cm);
    \\fill[color=myprimary!30, opacity=0.4] ([xshift=2cm, yshift=-1.5cm]current page.north west) circle (1.2cm);
    \\node[anchor=center, fill=white, draw=myprimary, line width=1.5pt, rounded corners=12pt, inner sep=8pt, minimum width=14cm] at ([yshift=-1.1cm]current page.north) {{
      \\bfseries\\sffamily\\color{{myprimary}}\\Large {header_banner_text}
    }};
    \\node[anchor=west, fill=myprimary, rounded corners=3pt, inner sep=4pt] at ([xshift=1.5cm, yshift=-1.8cm]current page.north west) {{\\bfseries\\sffamily\\color{{white}}\\scriptsize TOÁN HỌC}};
    \\node[anchor=east, fill=myaccent, rounded corners=3pt, inner sep=4pt] at ([xshift=-1.5cm, yshift=-1.8cm]current page.north east) {{\\bfseries\\sffamily\\color{{white}}\\scriptsize TOÁN}};
  \\end{{tikzpicture}}%
}}
\\fancyhead[C]{{\\drawheader}}
"""
        elif page_header_style == 'minimal':
            header_footer_defs += f"""
\\renewcommand{{\\headrulewidth}}{{0.5pt}}
\\fancyhead[L]{{\\sffamily\\color{{myprimary}}\\bfseries {header_banner_text}}}
\\fancyhead[R]{{\\sffamily\\color{{myprimary}}\\bfseries TOÁN HỌC}}
"""
        elif page_header_style == 'accent-bar':
            header_footer_defs += f"""
\\renewcommand{{\\headrule}}{{%
  \\color{{myaccent}}\\hrule width\\headwidth height 3.0pt
}}
\\fancyhead[L]{{\\sffamily\\color{{myprimary}}\\bfseries {header_banner_text}}}
\\fancyhead[R]{{\\sffamily\\color{{myprimary}}\\bfseries TOÁN HỌC}}
"""
        elif page_header_style == 'double-line':
            header_footer_defs += f"""
\\renewcommand{{\\headrule}}{{%
  \\color{{myprimary}}\\hrule width\\headwidth height 1.5pt \\vskip 1.5pt
  \\color{{myaccent}}\\hrule width\\headwidth height 0.5pt
}}
\\fancyhead[L]{{\\sffamily\\color{{myprimary}}\\bfseries {header_banner_text}}}
\\fancyhead[R]{{\\sffamily\\color{{myaccent}}\\bfseries TOÁN HỌC}}
"""
        else:
            header_footer_defs += r"\renewcommand{\headrulewidth}{0pt}" + "\n"

        # Footer configurations
        if page_footer_style == 'hoang-decor':
            header_footer_defs += f"""
\\newcommand{{\\drawfooter}}{{%
  \\begin{{tikzpicture}}[remember picture, overlay]
    \\fill[color=myprimary] ([yshift=1.2cm]current page.south west) rectangle (current page.south east);
    \\fill[color=myaccent] ([yshift=1.2cm]current page.south west) rectangle ([yshift=1.25cm]current page.south east);
    \\node[anchor=west, text=white] at ([xshift=1.5cm, yshift=0.6cm]current page.south west) {{\\sffamily\\scriptsize {footer_copyright_text}}};
    \\node[anchor=east, text=white] at ([xshift=-1.5cm, yshift=0.6cm]current page.south east) {{\\bfseries\\sffamily\\scriptsize THPT}};
    \\node[shape=circle, fill=white, draw=myaccent, line width=1.5pt, inner sep=5pt] at ([yshift=1.2cm]current page.south) {{\\bfseries\\color{{myprimary}}\\small\\thepage}};
  \\end{{tikzpicture}}%
}}
\\fancyfoot[C]{{\\drawfooter}}
"""
        elif page_footer_style == 'minimal':
            header_footer_defs += f"""
\\renewcommand{{\\footrulewidth}}{{0.5pt}}
\\fancyfoot[L]{{\\sffamily\\color{{gray}}\\scriptsize {footer_copyright_text}}}
\\fancyfoot[C]{{\\sffamily\\color{{myprimary}}\\bfseries\\thepage}}
"""
        elif page_footer_style == 'accent-bar':
            header_footer_defs += f"""
\\renewcommand{{\\footrule}}{{%
  \\color{{myaccent}}\\hrule width\\headwidth height 2.0pt
}}
\\fancyfoot[L]{{\\sffamily\\color{{myprimary}}\\bfseries\\scriptsize {footer_copyright_text}}}
\\fancyfoot[R]{{\\tikz[baseline=(char.base)]{{\\node[shape=rectangle,rounded corners=3pt,fill=myprimary,inner sep=4pt] (char) {{\\color{{white}}\\bfseries\\sffamily\\thepage}};}}}}
"""
        elif page_footer_style == 'double-line':
            header_footer_defs += f"""
\\renewcommand{{\\footrule}}{{%
  \\color{{myaccent}}\\hrule width\\headwidth height 0.5pt \\vskip 1.5pt
  \\color{{myprimary}}\\hrule width\\headwidth height 1.5pt
}}
\\fancyfoot[L]{{\\sffamily\\color{{gray}}\\scriptsize {footer_copyright_text}}}
\\fancyfoot[R]{{\\sffamily\\color{{myprimary}}\\bfseries\\thepage}}
"""
        else:
            header_footer_defs += r"\renewcommand{\footrulewidth}{0pt}" + "\n"
    else:
        header_footer_defs += r"\pagestyle{plain}" + "\n"


    common_end += header_footer_defs

    # Question and Book Label style snippet
    label_style_defs = ""
    if question_label_style == 'boxed':
        label_style_defs += r"""
\newcommand{\mycaubox}[1]{%
  \tikz[baseline=(char.base)]{\node[shape=rectangle,rounded corners=4pt,fill=myprimary,inner sep=4pt] (char) {\color{white}\bfseries\sffamily #1};}%
}
\newtheoremstyle{myboxstyle}%
  {\item[\hskip\labelsep \mycaubox{##1\ ##2}\theorem@separator]}%
  {\item[\hskip\labelsep \mycaubox{##1\ ##2}\ \textbf{(##3)}\theorem@separator]}
\theoremstyle{myboxstyle}
\theoremseparator{.}
\theorembodyfont{\rm}
"""
    else:
        label_style_defs += r"""
\theoremstyle{immini}
\theoremseparator{.}
\theorembodyfont{\rm}
"""
    
    label_style_defs += f"""
\\renewcommand{{\\nameex}}{{{q_prefix}{question_text}}}
\\newcommand{{\\namebook}}{{{b_prefix}{book_text}}}
\\renewtheorem{{ex}}{{\\nameex}}
\\makeatletter
\\@ifundefined{{bt}}{{\\newtheorem{{bt}}{{\\namebook}}}}{{\\renewtheorem{{bt}}{{\\namebook}}}}
\\makeatother
"""
    common_end += label_style_defs
    common_end = common_end.replace('__PRIMARY_RGB__', primary_rgb).replace('__ACCENT_RGB__', accent_rgb)

    if watermark_text:
        watermark_def = f"""
\\usepackage{{eso-pic}}
\\AddToShipoutPictureBG{{
  \\AtPageCenter{{
    \\makebox[0pt]{{\\rotatebox{{45}}{{\\tikz[remember picture,overlay] \\node[opacity={watermark_opacity},color=myprimary] {{\\fontsize{{60}}{{70}}\\selectfont\\bfseries\\sffamily {watermark_text}}};}}}}
  }}
}}
"""
        common_end += watermark_def

    # 2-column layout definition
    two_columns = config.get('two_columns', False)
    if two_columns and doc_type == 'de-thi':
        column_defs = r"""
\newcommand{\starttwocolumns}{\begin{multicols}{2}}
\newcommand{\stoptwocolumns}{\end{multicols}}
"""
    else:
        column_defs = r"""
\newcommand{\starttwocolumns}{}
\newcommand{\stoptwocolumns}{}
"""
    common_end += column_defs


    if doc_type == 'de-thi':
        if use_shapes:
            shape_defs = ""
            if incorrect_shape == 'circle':
                shape_defs += r"""
% Lệnh vẽ vòng tròn cho các phương án lựa chọn (viền trơn)
\newcommand*\mykhoanhtron[1]{\tikz[baseline=(char.base)]{\node[shape=circle,draw=myprimary,inner sep=1.2pt,minimum size=0.55cm] (char) {\color{myprimary}\textbf{#1}};}}
\renewcommand{\FalseEX}{\stepcounter{dapan}\mykhoanhtron{\textbf{\Alph{dapan}}}}
\renewcommand{\TrueEX}{\stepcounter{dapan}\mykhoanhtron{\textbf{\Alph{dapan}}}}
\settowidth{\widthalpha}{\mykhoanhtron{A}}
\addtolength{\widthalpha}{0.18cm}
"""
            elif incorrect_shape == 'yellow-circle':
                shape_defs += r"""
% Lệnh vẽ vòng tròn màu vàng cho các phương án lựa chọn
\newcommand*\mykhoanhtron[1]{\tikz[baseline=(char.base)]{\node[shape=circle,draw=yellow!80,fill=yellow!80,inner sep=1.5pt,minimum size=0.55cm] (char) {\color{black}\textbf{#1}};}}
\renewcommand{\FalseEX}{\stepcounter{dapan}\mykhoanhtron{\textbf{\Alph{dapan}}}}
\renewcommand{\TrueEX}{\stepcounter{dapan}\mykhoanhtron{\textbf{\Alph{dapan}}}}
\settowidth{\widthalpha}{\mykhoanhtron{A}}
\addtolength{\widthalpha}{0.18cm}
"""
            elif incorrect_shape == 'circle-white':
                shape_defs += r"""
% Lệnh vẽ vòng tròn nền trắng viền màu chủ đạo
\newcommand*\mykhoanhtron[1]{\tikz[baseline=(char.base)]{\node[shape=circle,draw=myprimary,fill=white,inner sep=1.2pt,minimum size=0.55cm] (char) {\color{myprimary}\textbf{#1}};}}
\renewcommand{\FalseEX}{\stepcounter{dapan}\mykhoanhtron{\textbf{\Alph{dapan}}}}
\renewcommand{\TrueEX}{\stepcounter{dapan}\mykhoanhtron{\textbf{\Alph{dapan}}}}
\settowidth{\widthalpha}{\mykhoanhtron{A}}
\addtolength{\widthalpha}{0.18cm}
"""
            elif incorrect_shape == 'boxed-white':
                shape_defs += r"""
% Lệnh vẽ hình vuông nền trắng viền màu chủ đạo
\newcommand*\mykhoanhtron[1]{\tikz[baseline=(char.base)]{\node[shape=rectangle,draw=myprimary,fill=white,inner sep=1.8pt,minimum size=0.55cm] (char) {\color{myprimary}\textbf{#1}};}}
\renewcommand{\FalseEX}{\stepcounter{dapan}\mykhoanhtron{\textbf{\Alph{dapan}}}}
\renewcommand{\TrueEX}{\stepcounter{dapan}\mykhoanhtron{\textbf{\Alph{dapan}}}}
\settowidth{\widthalpha}{\mykhoanhtron{A}}
\addtolength{\widthalpha}{0.18cm}
"""
            elif incorrect_shape == 'underlined':
                shape_defs += r"""
% Lệnh gạch chân màu chủ đạo
\newcommand*\mykhoanhtron[1]{\tikz[baseline=(char.base)]{\node[inner sep=1.5pt] (char) {\textbf{#1}}; \draw[line width=1.2pt, color=myprimary] (char.south west) -- (char.south east);}}
\renewcommand{\FalseEX}{\stepcounter{dapan}\mykhoanhtron{\textbf{\Alph{dapan}}}}
\renewcommand{\TrueEX}{\stepcounter{dapan}\mykhoanhtron{\textbf{\Alph{dapan}}}}
\settowidth{\widthalpha}{\textbf{A}}
\addtolength{\widthalpha}{0.18cm}
"""
            else:
                shape_defs += r"""
\renewcommand{\FalseEX}{\stepcounter{dapan}\textbf{\Alph{dapan}}.}
\renewcommand{\TrueEX}{\stepcounter{dapan}\textbf{\Alph{dapan}}.}
\settowidth{\widthalpha}{\textbf{A}.}
\addtolength{\widthalpha}{0.18cm}
"""
            shape_defs += r"""
\def\dotEX{\hspace{0.15cm}}
"""
        else:
            shape_defs = r"\def\dotEX{\hspace{0.15cm}}" + "\n"
        res = common_start + common_end + shape_defs

    elif doc_type in ['de-va-loigiai', 'dap-an']:
        if use_shapes:
            if correct_shape == 'rectangle':
                circled_def = r"\renewcommand*\circled[1]{\tikz[baseline=(char.base)]{\node[shape=rectangle,draw=myaccent,fill=myaccent!10,inner sep=1.8pt,minimum size=0.55cm] (char) {\color{myaccent}\textbf{#1}};}}"
            elif correct_shape == 'circle':
                circled_def = r"\renewcommand*\circled[1]{\tikz[baseline=(char.base)]{\node[shape=circle,draw=myaccent,fill=myaccent!10,inner sep=1.2pt,minimum size=0.55cm] (char) {\color{myaccent}\textbf{#1}};}}"
            elif correct_shape == 'yellow-circle':
                circled_def = r"\renewcommand*\circled[1]{\tikz[baseline=(char.base)]{\node[shape=circle,draw=yellow!90,fill=yellow!80,inner sep=1.5pt,minimum size=0.55cm] (char) {\color{black}\textbf{#1}};}}"
            elif correct_shape == 'circle-white':
                circled_def = r"\renewcommand*\circled[1]{\tikz[baseline=(char.base)]{\node[shape=circle,draw=myaccent,fill=white,inner sep=1.2pt,minimum size=0.55cm] (char) {\color{myaccent}\textbf{#1}};}}"
            elif correct_shape == 'boxed-white':
                circled_def = r"\renewcommand*\circled[1]{\tikz[baseline=(char.base)]{\node[shape=rectangle,draw=myaccent,fill=white,inner sep=1.8pt,minimum size=0.55cm] (char) {\color{myaccent}\textbf{#1}};}}"
            elif correct_shape == 'accent-box':
                circled_def = r"\renewcommand*\circled[1]{\tikz[baseline=(char.base)]{\node[shape=rectangle,draw=myaccent,fill=myaccent,inner sep=1.8pt,minimum size=0.55cm] (char) {\color{white}\textbf{#1}};}}"
            elif correct_shape == 'accent-circle':
                circled_def = r"\renewcommand*\circled[1]{\tikz[baseline=(char.base)]{\node[shape=circle,draw=myaccent,fill=myaccent,inner sep=1.2pt,minimum size=0.55cm] (char) {\color{white}\textbf{#1}};}}"
            elif correct_shape == 'underlined':
                circled_def = r"\renewcommand*\circled[1]{\tikz[baseline=(char.base)]{\node[inner sep=1.5pt] (char) {\textbf{#1}}; \draw[line width=1.5pt, color=myaccent] (char.south west) -- (char.south east);}}"
            else:
                circled_def = r"\renewcommand*\circled[1]{\textbf{\color{myaccent}#1}}"

            # True/False shape definition for \squareTF
            if correct_tf_shape == 'rectangle':
                tf_shape_def = r"\renewcommand{\squareTF}[2][fill=myaccent!5,draw=myaccent]{\tikz[baseline=(char.base)]{\node[shape=rectangle,inner sep=0.5pt,#1] (char) {{~\color{myaccent}#2\phantom{~}}};}}"
            elif correct_tf_shape == 'circle':
                tf_shape_def = r"\renewcommand{\squareTF}[2][fill=myaccent!5,draw=myaccent]{\tikz[baseline=(char.base)]{\node[shape=circle,inner sep=1pt,#1](char){\phantom{Đ}};\node[inner sep=1pt](char){\color{myaccent}#2};}}"
            elif correct_tf_shape == 'yellow-circle':
                tf_shape_def = r"\renewcommand{\squareTF}[2][fill=yellow!80,draw=yellow!90]{\tikz[baseline=(char.base)]{\node[shape=circle,inner sep=1pt,#1](char){\phantom{Đ}};\node[inner sep=1pt](char){\color{black}#2};}}"
            elif correct_tf_shape == 'circle-white':
                tf_shape_def = r"\renewcommand{\squareTF}[2][fill=white,draw=myaccent]{\tikz[baseline=(char.base)]{\node[shape=circle,inner sep=1pt,#1](char){\phantom{Đ}};\node[inner sep=1pt](char){\color{myaccent}#2};}}"
            elif correct_tf_shape == 'boxed-white':
                tf_shape_def = r"\renewcommand{\squareTF}[2][fill=white,draw=myaccent]{\tikz[baseline=(char.base)]{\node[shape=rectangle,inner sep=0.5pt,#1] (char) {{~\color{myaccent}#2\phantom{~}}};}}"
            elif correct_tf_shape == 'accent-box':
                tf_shape_def = r"\renewcommand{\squareTF}[2][fill=myaccent,draw=myaccent]{\tikz[baseline=(char.base)]{\node[shape=rectangle,inner sep=0.5pt,#1] (char) {{~\color{white}#2\phantom{~}}};}}"
            elif correct_tf_shape == 'accent-circle':
                tf_shape_def = r"\renewcommand{\squareTF}[2][fill=myaccent,draw=myaccent]{\tikz[baseline=(char.base)]{\node[shape=circle,inner sep=1pt,#1](char){\phantom{Đ}};\node[inner sep=1pt](char){\color{white}#2};}}"
            elif correct_tf_shape == 'underlined':
                tf_shape_def = r"\renewcommand{\squareTF}[2][]{\tikz[baseline=(char.base)]{\node[inner sep=2.5pt] (char) {#2}; \draw[line width=1.5pt, color=myaccent] (char.south west) -- (char.south east);}}"
            else:
                tf_shape_def = r"\renewcommand{\squareTF}[2][]{\textbf{\color{myaccent}#2}}"

            # Short Answer shape definition for \squareEX
            if correct_sa_shape == 'rectangle':
                sa_shape_def = r"\renewcommand{\squareEX}[2][fill=myaccent!10,draw=myaccent]{\tikz[baseline=(char.base)]{\node[shape=rectangle,inner sep=2.5pt,rounded corners=1pt,#1] (char) {{\color{myaccent}#2}};}}"
            elif correct_sa_shape == 'circle':
                sa_shape_def = r"\renewcommand{\squareEX}[2][fill=myaccent!10,draw=myaccent]{\tikz[baseline=(char.base)]{\node[shape=circle,inner sep=2pt,#1] (char) {{\color{myaccent}#2}};}}"
            elif correct_sa_shape == 'yellow-circle':
                sa_shape_def = r"\renewcommand{\squareEX}[2][fill=yellow!80,draw=yellow!90]{\tikz[baseline=(char.base)]{\node[shape=circle,inner sep=2pt,#1] (char) {{\color{black}#2}};}}"
            elif correct_sa_shape == 'circle-white':
                sa_shape_def = r"\renewcommand{\squareEX}[2][fill=white,draw=myaccent]{\tikz[baseline=(char.base)]{\node[shape=circle,inner sep=2pt,#1] (char) {{\color{myaccent}#2}};}}"
            elif correct_sa_shape == 'boxed-white':
                sa_shape_def = r"\renewcommand{\squareEX}[2][fill=white,draw=myaccent]{\tikz[baseline=(char.base)]{\node[shape=rectangle,inner sep=2.5pt,rounded corners=1pt,#1] (char) {{\color{myaccent}#2}};}}"
            elif correct_sa_shape == 'accent-box':
                sa_shape_def = r"\renewcommand{\squareEX}[2][fill=myaccent,draw=myaccent]{\tikz[baseline=(char.base)]{\node[shape=rectangle,inner sep=2.5pt,rounded corners=1pt,#1] (char) {{\color{white}#2}};}}"
            elif correct_sa_shape == 'accent-circle':
                sa_shape_def = r"\renewcommand{\squareEX}[2][fill=myaccent,draw=myaccent]{\tikz[baseline=(char.base)]{\node[shape=circle,inner sep=2pt,#1] (char) {{\color{white}#2}};}}"
            elif correct_sa_shape == 'underlined':
                sa_shape_def = r"\renewcommand{\squareEX}[2][]{\tikz[baseline=(char.base)]{\node[inner sep=2.5pt] (char) {#2}; \draw[line width=1.5pt, color=myaccent] (char.south west) -- (char.south east);}}"
            else:
                sa_shape_def = r"\renewcommand{\squareEX}[2][]{\textbf{\color{myaccent}#2}}"

            if incorrect_shape == 'circle':
                mc_list_def = r"""
\newcommand*\mykhoanhtron[1]{\tikz[baseline=(char.base)]{\node[shape=circle,draw=myprimary,inner sep=1.2pt,minimum size=0.55cm] (char) {\color{myprimary}\textbf{#1}};}}
\renewcommand{\FalseEX}{\stepcounter{dapan}\mykhoanhtron{\textbf{\Alph{dapan}}}}
\settowidth{\widthalpha}{\mykhoanhtron{A}}
"""
            elif incorrect_shape == 'yellow-circle':
                mc_list_def = r"""
\newcommand*\mykhoanhtron[1]{\tikz[baseline=(char.base)]{\node[shape=circle,draw=yellow!80,fill=yellow!80,inner sep=1.5pt,minimum size=0.55cm] (char) {\color{black}\textbf{#1}};}}
\renewcommand{\FalseEX}{\stepcounter{dapan}\mykhoanhtron{\textbf{\Alph{dapan}}}}
\settowidth{\widthalpha}{\mykhoanhtron{A}}
"""
            elif incorrect_shape == 'circle-white':
                mc_list_def = r"""
\newcommand*\mykhoanhtron[1]{\tikz[baseline=(char.base)]{\node[shape=circle,draw=myprimary,fill=white,inner sep=1.2pt,minimum size=0.55cm] (char) {\color{myprimary}\textbf{#1}};}}
\renewcommand{\FalseEX}{\stepcounter{dapan}\mykhoanhtron{\textbf{\Alph{dapan}}}}
\settowidth{\widthalpha}{\mykhoanhtron{A}}
"""
            elif incorrect_shape == 'boxed-white':
                mc_list_def = r"""
\newcommand*\mykhoanhtron[1]{\tikz[baseline=(char.base)]{\node[shape=rectangle,draw=myprimary,fill=white,inner sep=1.8pt,minimum size=0.55cm] (char) {\color{myprimary}\textbf{#1}};}}
\renewcommand{\FalseEX}{\stepcounter{dapan}\mykhoanhtron{\textbf{\Alph{dapan}}}}
\settowidth{\widthalpha}{\mykhoanhtron{A}}
"""
            elif incorrect_shape == 'underlined':
                mc_list_def = r"""
\newcommand*\mykhoanhtron[1]{\tikz[baseline=(char.base)]{\node[inner sep=1.5pt] (char) {\textbf{#1}}; \draw[line width=1.2pt, color=myprimary] (char.south west) -- (char.south east);}}
\renewcommand{\FalseEX}{\stepcounter{dapan}\mykhoanhtron{\textbf{\Alph{dapan}}}}
\settowidth{\widthalpha}{\textbf{A}}
"""
            else:
                mc_list_def = r"""
\renewcommand{\FalseEX}{\stepcounter{dapan}\textbf{\Alph{dapan}}.}
\settowidth{\widthalpha}{\textbf{A}.}
"""

            shape_defs = f"""
% ==========================================
% TÙY CHỈNH STYLE CÁ NHÂN (PREAMBLE)
% ==========================================
{mc_list_def}
{circled_def}

% Tùy chỉnh hiển thị Lời giải và Chốt đáp án
\\def\\loigiaiEX{{\\color{{myaccent}}{sol_prefix}\\textbf{{Hướng dẫn giải chi tiết:}}}}
\\def\\selectchoice{{\\color{{myprimary}}\\textbf{{{hand_prefix}Chốt đáp án:}}}}
\\def\\selectchoiceTF{{\\color{{myprimary}}\\textbf{{{hand_prefix}Chốt đáp án:}}}}
\\def\\selectshortans{{\\color{{myprimary}}\\textbf{{{hand_prefix}Chốt đáp án:}}}}

% Đồng bộ tông màu myaccent cho các khung hệ thống
\\renewcommand{{\\circEX}}[2][fill=myaccent!10,draw=myaccent]{{%
	\\tikz[baseline=(char.base)]{{\\node[shape=circle,inner sep=1pt,#1] (char) {{\\color{{myaccent}}#2}};}}%
}}
{sa_shape_def}
{tf_shape_def}
\\renewcommand{{\\circTF}}[2][fill=myaccent!10,draw=myaccent]{{%
	\\tikz[baseline=(char.base)]{{\\node[shape=circle,inner sep=0.5pt,#1](char){{\\phantom{{Đ}}}};\\node[inner sep=0.5pt](char){{\\color{{myaccent}}\\textbf{{#2}}}};}}%
}}
\\renewcommand{{\\circT}}[2][draw=myaccent,fill=myaccent!10]{{%
	\\tikz[baseline=(char.base)]{{\\draw[#1,scale=\\f@size/11.5] (0,0) circle(7pt);\\node (char)[above=-1.4ex]{{\\color{{myaccent}}#2}};\\node (char)[right=6pt,scale=0.95]{{\\color{{myaccent}}\\parbox[t]{{2.6mm}}{{\\centering Đ}}}};}}\\vspace{{0.1mm}}%
}}
\\renewcommand{{\\circF}}[2][draw=myaccent,fill=myaccent!10]{{%
	\\tikz[baseline=(char.base)]{{\\draw[#1,scale=\\f@size/11.5] (0,0) circle(7pt);\\node (char)[above=-1.4ex]{{\\color{{myaccent}}#2}};\\node (char)[right=6pt,scale=0.95]{{\\color{{myaccent}}\\parbox[t]{{2.6mm}}{{\\centering S}}}};}}\\vspace{{0.1mm}}%
}}

% Đồng nhất màu sắc ô chốt đáp án với tông màu chủ đạo (myaccent) - ô vuông đồng bộ
\\def\\keyCh{{\\circled{{\\keyEX}}}}
\\def\\keyTF{{\\squareTF{{\\textbf{{\\keyEX}}}}}}
\\def\\keySA{{\\squareEX{{\\textbf{{\\keyEX}}}}}}

\\renewcommand{{\\qedsymbol}}{{}} % Xóa ô vuông ở cuối dòng lời giải

% Tùy chỉnh phương án A, B, C, D đồng nhất
\\def\\colorEX{{\\color{{myaccent}}}}

% Sử dụng luôn lệnh \\circled đã được làm đẹp ở trên cho đáp án Đúng
\\renewcommand{{\\TrueEX}}{{\\stepcounter{{dapan}}\\circled{{\\Alph{{dapan}}}}}}

\\addtolength{{\\widthalpha}}{{0.18cm}}

% Thêm khoảng trắng (0.15cm) để đẩy chữ cách xa ô vuông/vòng tròn
\\def\\dotEX{{\\hspace{{0.15cm}}}} 
\\def\\parskipchoice{{{parskip_choice}}}

% Định nghĩa lại lệnh \\Split để hỗ trợ tách ô cho cả số thập phân (dùng dấu chấm) và phân số
\\makeatletter
\\renewcommand{{\\Split}}[1]{{%
	\\def\\str{{\\detokenize{{#1}}}}%
	\\StrSubstitute{{\\str}}{{\\detokenize{{ }}}}{{}}[\\cleaned]%
	\\StrSubstitute{{\\cleaned}}{{\\detokenize{{$}}}}{{}}[\\cleaned]%
	\\StrSubstitute{{\\cleaned}}{{\\detokenize{{\\,}}}}{{}}[\\cleaned]%
	\\StrSubstitute{{\\cleaned}}{{\\detokenize{{\\;}}}}{{}}[\\cleaned]%
	\\StrSubstitute{{\\cleaned}}{{\\detokenize{{~}}}}{{}}[\\cleaned]%
	\\StrSubstitute{{\\cleaned}}{{\\detokenize{{{{,}}}}}}{{,}}[\\cleaned]%
	\\StrSubstitute{{\\cleaned}}{{\\detokenize{{-}}}}{{}}[\\nstr]%
	\\StrSubstitute{{\\nstr}}{{\\detokenize{{,}}}}{{}}[\\nstr]%
	\\StrSubstitute{{\\nstr}}{{\\detokenize{{.}}}}{{}}[\\nstr]%
	\\StrSubstitute{{\\nstr}}{{\\detokenize{{/}}}}{{}}[\\nstr]%
	\\StrSubstitute{{\\nstr}}{{\\detokenize{{0}}}}{{}}[\\nstr]%
	\\StrSubstitute{{\\nstr}}{{\\detokenize{{1}}}}{{}}[\\nstr]%
	\\StrSubstitute{{\\nstr}}{{\\detokenize{{2}}}}{{}}[\\nstr]%
	\\StrSubstitute{{\\nstr}}{{\\detokenize{{3}}}}{{}}[\\nstr]%
	\\StrSubstitute{{\\nstr}}{{\\detokenize{{4}}}}{{}}[\\nstr]%
	\\StrSubstitute{{\\nstr}}{{\\detokenize{{5}}}}{{}}[\\nstr]%
	\\StrSubstitute{{\\nstr}}{{\\detokenize{{6}}}}{{}}[\\nstr]%
	\\StrSubstitute{{\\nstr}}{{\\detokenize{{7}}}}{{}}[\\nstr]%
	\\StrSubstitute{{\\nstr}}{{\\detokenize{{8}}}}{{}}[\\nstr]%
	\\StrSubstitute{{\\nstr}}{{\\detokenize{{9}}}}{{}}[\\nstr]%
	\\IfStrEq{{\\nstr}}{{}}%
	{{\\StrLen{{\\cleaned}}[\\lengthKQ]%
		\\ifnum\\lengthKQ<5\\relax%
			{{\\renewcommand{{\\tabcolsep}}{{1.8mm}}%
			\\begin{{tabular}}{{|m{{2.5mm}}|m{{2.5mm}}|m{{2.5mm}}|m{{2.5mm}}|}}
				\\hline%
				\\ifnum\\lengthKQ>0\\relax\\StrChar{{\\cleaned}}{{1}}[\\firstchar]\\centering$\\firstchar$\\fi&%
				\\ifnum\\lengthKQ>1\\relax\\StrChar{{\\cleaned}}{{2}}[\\secondchar]\\centering$\\secondchar$\\fi&%
				\\ifnum\\lengthKQ>2\\relax\\StrChar{{\\cleaned}}{{3}}[\\thirdchar]\\centering$\\thirdchar$\\fi&%
				\\ifnum\\lengthKQ>3\\relax\\StrChar{{\\cleaned}}{{4}}[\\fourthchar]\\centering$\\fourthchar$\\fi\\tabularnewline%
				\\hline%
			\\end{{tabular}}}}%
		\\else #1 \\fi%
	}}{{#1}}%
}}

% Định nghĩa lại lệnh \\shortans để dùng thống nhất màu myaccent
\\renewcommand{{\\shortans}}[2][]{{%
	\\gdef\\chType{{-1}}%
	\\savekinditch\\def\\typekindSA{{#1}}%
	\\IfInteger{{#1}}{{\\def\\RM{{1}}}}{{%
		\\ifthenelse{{\\equal{{#1}}{{}}\\OR\\equal{{#1}}{{oly}}\\OR\\equal{{#1}}{{...}}}}{{\\def\\RM{{1}}}}{{\\def\\RM{{0}}}}}}%
	\\ifthenelse{{\\equal{{\\kindSA}}{{}}}}
	{{\\shortansfix[#1]{{\\Split{{#2}}}}}}
	{{\\ifthenelse{{\\equal{{\\kindSA}}{{ShowSAKeyColor}}}}
		{{\\ifthenelse{{\\equal{{#1}}{{}}\\OR\\equal{{#1}}{{oly}}\\OR\\equal{{#1}}{{...}}}}
			{{\\Hfill\\raisebox{{0pt}}{{\\tikz[baseline=(char.base)]{{%
				\\node (char)[rectangle,inner sep=2pt,fill=myaccent!10,draw=myaccent]{{\\color{{myaccent}}~\\selectshortans\\ \\Split{{#2}}\\phantom{{~}}}};}}}}\\ifInList{{\\hspace{{-1mm}}}}{{\\par}}}}%
			{{\\raisebox{{0pt}}{{\\tikz[baseline=(char.base)]{{%
				\\node (char)[rectangle,inner sep=2pt,fill=myaccent!10,draw=myaccent]{{\\color{{myaccent}}\\Split{{#2}}}};}}}}}}}}%
		{{\\ifthenelse{{\\equal{{\\kindSA}}{{ShowSAKeyLG}}}}
			{{\\ifthenelse{{\\equal{{#1}}{{}}\\OR\\equal{{#1}}{{oly}}\\OR\\equal{{#1}}{{...}}}}
				{{\\Hfill\\raisebox{{0pt}}{{\\tikz[baseline=(char.base)]{{%
					\\node (char)[rectangle,inner sep=2pt]{{\\color{{myaccent}}~\\selectshortans\\ \\Split{{#2}}\\phantom{{~}}}};}}}}\\ifInList{{\\hspace{{-1mm}}}}{{\\par}}}}%
				{{\\raisebox{{0pt}}{{\\tikz[baseline=(char.base)]{{%
					\\node (char)[rectangle,inner sep=2pt]{{\\color{{myaccent}}\\Split{{#2}}}};}}}}}}}}%
			{{\\shortansfix[\\kindSA]{{\\Split{{#2}}}}}}%
		}}%
	}}%
	\\xdef\\saveKQ{{\\detokenize{{#2}}}}\\gdef\\keyEX{{#2}}%
	\\ifInList
	{{\\stepcounter{{dapan}}%
		\\xdef\\saveFileAns{{\\saveFileAns\\ifnum\\thedapan>1\\relax\\@percentchar^^J\\fi\\string\\dapsoSA[\\DapAnSA]\\detokenize{{{{#2}}}}}}}}
}}

% Định nghĩa lại lệnh \\addclause để bỏ các vòng tròn Đ, S ở giải chi tiết
\\renewcommand{{\\addclause}}{{%
	\\ifnum\\addquestions=1\\gdef\\lienket{{\\;>>>>\\;}}\\gdef\\brlk{{\\par\\noindent}}%
	\\else\\gdef\\lienket{{}}\\gdef\\brlk{{}}\\fi%
		 \\ifnum\\the\\value{{numitem}}=1\\relax {{\\deA}}{{\\Large\\color{{myaccent}}\\lienket}}%
	\\else\\ifnum\\the\\value{{numitem}}=2\\relax {{\\deB}}{{\\Large\\color{{myaccent}}\\lienket}}%
	\\else\\ifnum\\the\\value{{numitem}}=3\\relax {{\\deC}}{{\\Large\\color{{myaccent}}\\lienket}}%
	\\else\\ifnum\\the\\value{{numitem}}=4\\relax {{\\deD}}{{\\Large\\color{{myaccent}}\\lienket}}%
	\\else\\ifnum\\the\\value{{numitem}}=5\\relax {{\\deE}}{{\\Large\\color{{myaccent}}\\lienket}}%
	\\else\\ifnum\\the\\value{{numitem}}=6\\relax {{\\deF}}{{\\Large\\color{{myaccent}}\\lienket}}%
	\\else\\ifnum\\the\\value{{numitem}}=7\\relax {{\\deG}}{{\\Large\\color{{myaccent}}\\lienket}}%
	\\else\\ifnum\\the\\value{{numitem}}=8\\relax {{\\deH}}{{\\Large\\color{{myaccent}}\\lienket}}%
	\\else\\ifnum\\the\\value{{numitem}}=9\\relax {{\\deI}}{{\\Large\\color{{myaccent}}\\lienket}}%
	\\else\\ifnum\\the\\value{{numitem}}=10\\relax{{\\deJ}}{{\\Large\\color{{myaccent}}\\lienket}}%
	\\fi\\fi\\fi\\fi\\fi\\fi\\fi\\fi\\fi\\fi%
}}
\\makeatother
"""
        else:
            shape_defs = r"\def\dotEX{\hspace{0.15cm}}" + "\n"
        res = common_start + common_end + shape_defs

    if doc_type == 'dap-an':
        if auto_wrap_anstab:
            res += r"""
% ==========================================
% GHI ĐÈ \inputanstab ĐỂ TỰ ĐỘNG NGẮT DÒNG
% PHẦN II (ĐÚNG SAI) VÀ PHẦN III (TRẢ LỜI NGẮN)
% ==========================================
\makeatletter
\renewcommand{\inputanstab}[3][1]{\IfInteger{#1}{\ifnum#1>0\relax%
	\renewcommand{\dapsoSA}[2][]{##2}%
	\renewcommand{\circT}[2][]{\refstepcounter{dapan}%
		\pgfmathsetmacro{\xpos}{2*(\SttANS-#1-\sttTAB*#2)}%
		\draw (\xpos,0.7-0.7*\thedapan) rectangle (\xpos+2,-0.7*\thedapan);
		\node at (\xpos+1,0.35-0.7*\thedapan){##2) Đ};
	}%
	\renewcommand{\circF}[2][]{\refstepcounter{dapan}%
		\pgfmathsetmacro{\xpos}{2*(\SttANS-#1-\sttTAB*#2)}%
		\draw (\xpos,0.7-0.7*\thedapan) rectangle (\xpos+2,-0.7*\thedapan);
		\node at (\xpos+1,0.35-0.7*\thedapan){##2) S};
	}%
	\RenewEnviron{Solution}[2][]{%
		\findkindans{\BODY}%xác định loại ans
		\gdef\SttANS{##2}%
		\pgfmathsetmacro{\sttTAB}{ceil((##2-#1+1)/#2)-1}%
		\setcounter{dapan}{0}%
		\ifnum\kindans=0%
			\begin{scope}[shift={(0,-2*\sttTAB)}]
				\draw[xstep=2,ystep=0.7] (-2,-0.7) grid (0,0.7);
				\node at (-1,0.4)[fill=white,inner sep=0.3pt]{\bfseries Câu};
				\node at (-1,-0.35)[fill=white,inner sep=0.3pt]{\bfseries Chọn};
				\draw[ystep=0.7] (0,0.7) grid (#2,-0.7);
				\node at (##2-#1+0.5-\sttTAB*#2,0.35){##2};
				\node at (##2-#1+0.5-\sttTAB*#2,-0.35){\BODY};
			\end{scope}%
		\fi%
		\ifnum\kindans=-1%
			\begin{scope}[shift={(0,-2*\sttTAB)}]
				\draw[xstep=2,ystep=0.7] (-2,-0.7) grid (0,0.7);
				\node at (-1,0.4)[fill=white,inner sep=0.3pt]{\bfseries Câu};
				\node at (-1,-0.35)[fill=white,inner sep=0.3pt]{\bfseries Chọn};
				\pgfmathsetmacro{\xpos}{1.4*(##2-#1-\sttTAB*#2)}%
				\draw (\xpos,0.7) rectangle (\xpos+1.4,-0.7);
				\draw (\xpos,0)--(\xpos+1.4,0);
				\node at (\xpos+0.7,0.35){##2};
				\node at (\xpos+0.7,-0.35){\BODY};
			\end{scope}%
		\fi%
		\ifnum\kindans=1%
			\begin{scope}[shift={(0,-3.5*\sttTAB)}]
				\pgfmathsetmacro{\xpos}{2*(##2-#1-\sttTAB*#2)}%
				\draw (\xpos,0.7) rectangle (\xpos+2,-0.7);
				\node at (\xpos+1,0.4){\bfseries Câu ##2.};
				\BODY
			\end{scope}%
		\fi%
	}
	\begin{center}
		\begin{tikzpicture}[xscale=0.9]
			\input{#3}
		\end{tikzpicture}
	\end{center}
\fi}{}}
\makeatother
"""
    else:
        if prevent_overflow_ansbox:
            res += r"""
% ==========================================
% GHI ĐÈ \inputansbox ĐỂ TRÁNH TRÀN TRANG ĐỐI VỚI ĐÚNG SAI
% ==========================================
\makeatletter
\renewcommand{\inputansbox}[3][]{%
	\ifthenelse{\equal{#1}{0}}{\Nocirc\gdef\runTachO{0}\def\wCau{4mm}}
	{\gdef\runTachO{1}\def\wCau{10mm}%
	\ifthenelse{\equal{#1}{1}}{\Fullcirc}{\Onlycirc}}%
	\IfSubStr{#2}{,}
	{\def\numABCD{\expandafter\firstofthreeaux#2\relax}%
		\def\numTF{\expandafter\secondofthreeaux#2\relax}%
		\def\numSA{\expandafter\thirdofthreeaux#2\relax}%
		\Onlycirc\def\numMW{3}}%
	{\def\numABCD{#2}\def\numTF{#2}\def\numSA{#2}\def\numMW{#2}}%
	{\fontfamily{qcs}\small\selectfont%
	\RenewEnviron{Solution}[2][]{%
		\findkindans{\BODY}%xác định loại ans
		\def\SttANS{##2}\def\nobox{0}%
		\ifthenelse{\equal{##1}{}}{}{\ifthenelse{\equal{#1}{0}}{\def\nameans{}}{\def\nameans{##1~}}}%
		\ifnum\kindans=10%
			\setlength{\dorongANS}{\dimexpr\linewidth/#2-4.2\fboxsep\relax}%
			\BODY%
		\else\ifnum\kindans=-1\ifnum\numexpr\numSA\relax>0%
				\ifthenelse{\equal{\numCellsAnsBox}{}}
					{\setlength{\dorongANS}{\dimexpr\linewidth/\numSA-4.2\fboxsep\relax}}
					{\setlength{\dorongANS}{\dimexpr\numCellsAnsBox\linewidth/\numSA-4.2\fboxsep\relax}}%%
				\BODY\gdef\numCellsAnsBox{}\fi%
			\else\ifnum\kindans=-2%
					\ifnum##2=1\vspace{0.3\baselineskip}\par\fi%
					\begin{lrbox}{\myboxans}
						\ifthenelse{\equal{\numCellsAnsBox}{}}
							{\begin{minipage}{\dimexpr\linewidth/\numMW-4.2\fboxsep\relax}
								\parbox[b]{\wCau}{\color{blue}\nameans##2.}
								\hfill\color{black}\mbox{\BODY}%
							\end{minipage}}
							{\begin{minipage}{\dimexpr\numCellsAnsBox\linewidth/\numMW-4.2\fboxsep\relax}
								\parbox[b]{\wCau}{\color{blue}\nameans##2.}
								\hfill\color{black}\mbox{\BODY}%
							\end{minipage}\gdef\numCellsAnsBox{}}%
					\end{lrbox}\noindent\fbox{\usebox{\myboxans}}\;
				\else\ifnum\kindans=1\ifnum\numexpr\numTF\relax>0%Câu đúng/sai
						\ifnum##2=1\vspace{0.3\baselineskip}\par\fi%
						\begin{lrbox}{\myboxans}%
							\renewcommand{\circT}[2][]{\textbf{####2}\textsuperscript{Đ}\ignorespaces}%
							\renewcommand{\circF}[2][]{\textbf{####2}\textsuperscript{S}\ignorespaces}%
							\ifthenelse{\equal{\numCellsAnsBox}{}}
								{\begin{minipage}{\dimexpr\linewidth/\numTF-4.2\fboxsep\relax}
									\parbox[b]{\wCau}{\color{blue}\nameans##2.}
									\hfill\color{black}\BODY%
								\end{minipage}}
								{\begin{minipage}{\dimexpr\numCellsAnsBox\linewidth/\numTF-4.2\fboxsep\relax}
									\parbox[b]{\wCau}{\color{blue}\nameans##2.}
									\hfill\color{black}\BODY%
								\end{minipage}\gdef\numCellsAnsBox{}}%
						\end{lrbox}\noindent\fbox{\usebox{\myboxans}}\;
					\fi%
					\else\ifnum\numexpr\numABCD\relax>0%
						\begin{lrbox}{\myboxans}%
						\ifthenelse{\equal{\numCellsAnsBox}{}}
							{\begin{minipage}{\dimexpr\linewidth/\numABCD-4.2\fboxsep\relax}
								\color{blue}##2.
								\hfill\color{black}\BODY%
							\end{minipage}}
							{\begin{minipage}{\dimexpr\numCellsAnsBox\linewidth/\numABCD-4.2\fboxsep\relax}
								\color{blue}##2.
								\hfill\color{black}\BODY%
							\end{minipage}\gdef\numCellsAnsBox{}}%
						\end{lrbox}\noindent\fbox{\usebox{\myboxans}}\;
						\fi%
					\fi%
				\fi%
			\fi%
		\fi%
	}%
	\begin{flushleft}%
		\foreach \file in {#3}{% Nếu muốn giữa 2 file được nhập có xuống dòng thì gõ file1 ,, file 2
			\IfStrEq{\file}{}{\vspace{0.3mm}\par}{\IfFileExists{\file}{\input{\file}}{\par File tex: \file\ không tồn tại!}}%
    }
	\end{flushleft}
}}
\makeatother
"""
    return res

def convert_ocr_math(text):
    text = re.sub(r'\\\(\s*([Hh]ình\s*\d+)\s*\\\)', r'\1', text)
    text = text.replace(r'\(', '$').replace(r'\)', '$')
    text = text.replace(r'\[', '$$').replace(r'\]', '$$')
    text = re.sub(r'\$\s*([Hh]ình\s*\d+)\s*\$', r'\1', text)
    return text

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

def convert_math_symbols(text):
    text = re.sub(r'\$\$(.*?)\$\$', r'$\1$', text)
    parts = text.split('$')
    for i in range(len(parts)):
        if i % 2 == 1:
            inner = parts[i]
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
    tex_rows.append(' & '.join(convert_math_symbols(convert_ocr_math(clean_vietnamese_text(cell))) for cell in header) + r' \\')
    tex_rows.append(r'\hline')
    for r in data_rows:
        padded = r + [''] * (width - len(r))
        tex_rows.append(' & '.join(convert_math_symbols(convert_ocr_math(clean_vietnamese_text(cell))) for cell in padded) + r' \\')
        tex_rows.append(r'\hline')
    tex_rows += [r'\end{tabular}', r'\end{center}']
    return '\n'.join(tex_rows)

def normalize_labels(text):
    text = re.sub(r'(?<![\w\\\(\[\{])(a\s*[\.\)]|A\s*\))\s*', '\na) ', text)
    text = re.sub(r'(?<![\w\\\(\[\{])(b\s*[\.\)]|B\s*\))\s*', '\nb) ', text)
    text = re.sub(r'(?<![\w\\\(\[\{])(c\s*[\.\)]|C\s*\))\s*', '\nc) ', text)
    text = re.sub(r'(?<![\w\\\(\[\{])(d\s*[\.\)]|D\s*\))\s*', '\nd) ', text)
    
    text = re.sub(r'(?<![\w\\\(\[\{])A\s*[\.\:]\s*', '\nA. ', text)
    text = re.sub(r'(?<![\w\\\(\[\{])B\s*[\.\:]\s*', '\nB. ', text)
    text = re.sub(r'(?<![\w\\\(\[\{])C\s*[\.\:]\s*', '\nC. ', text)
    text = re.sub(r'(?<![\w\\\(\[\{])D\s*[\.\:]\s*', '\nD. ', text)
    return text

def copy_input_to_output(input_dir, output_dir):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)
    
    # Copy ex_test.sty from root master package
    sty_src = ROOT / 'ex_test' / 'ex_test.sty'
    if not sty_src.exists():
        sty_src = input_path / 'ex_test.sty'
    if sty_src.exists():
        shutil.copy2(sty_src, output_path / 'ex_test.sty')
        print(f"Copied ex_test.sty to {output_path}")

    # Copy all files and directories except .tex files and output directory
    for item in input_path.iterdir():
        if item.is_dir():
            if item.name.lower() in ['.git', '__pycache__', '.windsurf', '.gemini']:
                continue
            # Avoid infinite recursion if output_dir is nested inside input_dir
            try:
                if output_path.resolve() == item.resolve() or output_path.resolve().is_relative_to(item.resolve()):
                    continue
            except Exception:
                pass
            dest_dir = output_path / item.name
            if dest_dir.exists():
                try:
                    shutil.rmtree(dest_dir)
                except Exception:
                    pass
            try:
                shutil.copytree(item, dest_dir)
            except Exception as e:
                print(f"Warning: could not copy folder {item.name}: {e}")
        else:
            if item.name == 'ex_test.sty':
                continue
            if item.suffix.lower() == '.tex':
                try:
                    with open(item, 'r', encoding='utf-8', errors='ignore') as f:
                        text = f.read()
                    if r'\begin{document}' not in text:
                        shutil.copy2(item, output_path / item.name)
                except Exception as e:
                    print(f"Warning: could not read {item.name}: {e}")
                continue
            shutil.copy2(item, output_path / item.name)

def inject_style_to_file(input_file_path, output_file_path, style_name):
    input_file_path = Path(input_file_path)
    output_file_path = Path(output_file_path)
    
    with open(input_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    filename = input_file_path.name.lower()
    if 'loigiai' in filename or 'loi-giai' in filename or 'sol' in filename:
        doc_type = 'de-va-loigiai'
    elif 'dap-an' in filename or 'dapan' in filename or 'ans' in filename:
        doc_type = 'dap-an'
    else:
        doc_type = 'de-thi'
        
    match = re.search(r'\\begin\s*\{\s*document\s*\}', content)
    if not match:
        output_file_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(input_file_path, output_file_path)
        return
        
    preamble_end = match.start()
    body_start = match.end()
    
    new_preamble = generate_preamble(style_name, doc_type)
    body = content[body_start:]
    
    config = STYLES.get(style_name, STYLES[DEFAULT_STYLE])
    tf_layout = config.get('tf_layout', 't')
    tf_bold = '1' if config.get('tf_bold_header', True) else '0'
    tf_abbr = '1' if config.get('tf_abbreviation', False) else '0'
    tf_header = config.get('tf_header_text', 'Phát biểu').replace('&', r'\&')
    tf_dapan = config.get('tf_dapan', 'a')
    tf_sep = config.get('tf_sep', ')')
    tf_addanswers = '1' if config.get('tf_addanswers', True) else '0'
    tf_addquestions = '1' if config.get('tf_addquestions', False) else '0'
    
    sa_layout = config.get('sa_layout', 'oly')
    sa_prefix = config.get('sa_prefix', 'Đáp số:').replace('&', r'\&')
    sa_width = config.get('sa_width', 4)
    sa_dapan = config.get('sa_dapan', 'a')
    sa_height = config.get('sa_height', 0.9)
    
    optn_str = f"\\OPTN{{kindTF={tf_layout}, boldTF={tf_bold}, viettat={tf_abbr}, phatbieu={tf_header}, dapanTF={tf_dapan}, sepTF={tf_sep}, addanswers={tf_addanswers}, addquestions={tf_addquestions}, kindSA={sa_layout}, ketquaSA={sa_prefix}, widthSA={sa_width}, heightSA={sa_height}, dapanSA={sa_dapan}}}"
    
    if doc_type in ['de-thi', 'de-va-loigiai']:
        optn_match = re.search(r'\\OPTN\s*\{[^}]*\}', body)
        if optn_match:
            body = body[:optn_match.start()] + optn_str + body[optn_match.end():]
        else:
            hideans_match = re.search(r'\\hideans', body)
            if hideans_match:
                insert_pos = hideans_match.end()
                body = body[:insert_pos] + "\n" + optn_str + body[insert_pos:]
            else:
                body = "\n" + optn_str + body
                
    new_content = new_preamble + "\n\\begin{document}" + body
    
    output_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="OCR parser and Style Injection for LaTeX")
    parser.add_argument("style_name", nargs="?", default=None, help="Theme style name")
    parser.add_argument("--action", choices=["ocr", "inject_single", "inject_all"], default="ocr", help="Action to perform")
    parser.add_argument("--input_dir", help="Input directory")
    parser.add_argument("--output_dir", help="Output directory")
    parser.add_argument("--file", help="TeX file name for inject_single")
    
    args = parser.parse_args()
    
    style_name = DEFAULT_STYLE
    if args.style_name:
        arg_style = args.style_name.strip().lower()
        if arg_style in STYLES:
            style_name = arg_style
            print(f"Using requested style: {style_name}")
        else:
            print(f"Warning: Style '{arg_style}' not found. Using default '{style_name}'. Available: {list(STYLES.keys())}")
    else:
        print(f"Using default style: {style_name}")
        
    global OUTPUT_DIR
    if args.output_dir:
        OUTPUT_DIR = Path(args.output_dir)
        
    if args.action == "inject_single":
        if not args.input_dir or not args.output_dir or not args.file:
            print("Error: Missing --input_dir, --output_dir, or --file for action inject_single.")
            sys.exit(1)
        print(f"Injecting style '{style_name}' into {args.file} from {args.input_dir} to {args.output_dir}...")
        copy_input_to_output(args.input_dir, args.output_dir)
        inject_style_to_file(Path(args.input_dir) / args.file, Path(args.output_dir) / args.file, style_name)
        (Path(args.output_dir) / 'ans').mkdir(parents=True, exist_ok=True)
        print("Done styling single file.")
        return
        
    elif args.action == "inject_all":
        if not args.input_dir or not args.output_dir:
            print("Error: Missing --input_dir or --output_dir for action inject_all.")
            sys.exit(1)
        print(f"Injecting style '{style_name}' into all TeX files in {args.input_dir} to {args.output_dir}...")
        copy_input_to_output(args.input_dir, args.output_dir)
        
        input_path = Path(args.input_dir)
        tex_files = [f.name for f in input_path.glob("*.tex")]
        if not tex_files:
            print("No .tex files found in input directory.")
            return
            
        for f_name in tex_files:
            print(f"Styling {f_name}...")
            inject_style_to_file(input_path / f_name, Path(args.output_dir) / f_name, style_name)
        (Path(args.output_dir) / 'ans').mkdir(parents=True, exist_ok=True)
        print(f"Done styling all {len(tex_files)} files.")
        return

    if not INPUT_FILE.exists():
        print(f"Error: Input file {INPUT_FILE} not found.")
        return

    print(f"Reading {INPUT_FILE}...")
    with open(INPUT_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    questions = []
    current_q = None
    table_lines = []

    for idx, raw_line in enumerate(lines):
        line = raw_line.strip()
        if not line or line.startswith('https://') or line.startswith('<!--'):
            continue
        if line.startswith('CHỦ ĐỀ') or 'TRẮC NGHIỆM' in line or 'TRẢ LỜI NGẮN' in line:
            continue

        if line.startswith('|'):
            table_lines.append(raw_line)
            continue
        elif table_lines:
            table_tex = parse_markdown_table(table_lines)
            if current_q:
                current_q['lines'].append(table_tex)
            table_lines = []

        match = QUESTION_START_RE.match(line)
        if match:
            if current_q:
                questions.append(current_q)
            q_num = int(match.group(1))
            q_text = match.group(2).strip()
            current_q = {
                'number': q_num,
                'lines': [q_text] if q_text else []
            }
        elif current_q:
            current_q['lines'].append(line)

    if current_q:
        questions.append(current_q)

    print(f"Parsed {len(questions)} total questions sequentially.")

    # Now classify and format each question
    part1_questions = []
    part2_questions = []
    part3_questions = []

    for q in questions:
        full_text = '\n'.join(q['lines'])
        full_text = convert_ocr_math(full_text)
        full_text = clean_vietnamese_text(full_text)
        full_text = convert_math_symbols(full_text)
        full_text = normalize_labels(full_text)

        mc_matches = list(CHOICE_LABEL_RE.finditer(full_text))
        tf_matches = list(TF_LABEL_RE.finditer(full_text))

        if len(mc_matches) >= 4:
            stem = full_text[:mc_matches[0].start()].strip()
            choices = []
            for j in range(4):
                start = mc_matches[j].end()
                end = mc_matches[j+1].start() if j+1 < len(mc_matches) else len(full_text)
                choice_text = full_text[start:end].strip()
                if choice_text.endswith('.') and not choice_text.endswith('..'):
                    choice_text = choice_text[:-1].strip()
                choices.append(choice_text)
            
            part1_questions.append({
                'stem': stem,
                'choices': choices,
                'correct_idx': 0
            })
        elif len(tf_matches) >= 2:
            stem = full_text[:tf_matches[0].start()].strip()
            statements = []
            for j in range(len(tf_matches)):
                start = tf_matches[j].end()
                end = tf_matches[j+1].start() if j+1 < len(tf_matches) else len(full_text)
                statement_text = full_text[start:end].strip()
                if statement_text.endswith('.') and not statement_text.endswith('..'):
                    statement_text = statement_text[:-1].strip()
                statements.append(statement_text)
            
            while len(statements) < 4:
                lbl = chr(97 + len(statements))
                statements.append(f"Mệnh đề {lbl} (đang được cập nhật).")
            
            part2_questions.append({
                'stem': stem,
                'statements': statements[:4],
                'answers': [True, False, True, False]
            })
        else:
            part3_questions.append({
                'stem': full_text.strip(),
                'answer': "1"
            })

    print(f"Grouped questions:")
    print(f"  Part 1 (Multiple Choice): {len(part1_questions)} questions (Expected: 30)")
    print(f"  Part 2 (True/False): {len(part2_questions)} questions (Expected: 13)")
    print(f"  Part 3 (Short Answer): {len(part3_questions)} questions (Expected: 24)")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / 'ans').mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / 'Images').mkdir(parents=True, exist_ok=True)

    sty_src = ROOT / 'ex_test' / 'ex_test.sty'
    if sty_src.exists():
        shutil.copy2(sty_src, OUTPUT_DIR / 'ex_test.sty')
        print(f"Copied ex_test.sty to {OUTPUT_DIR}")

    # Build body.tex
    config = STYLES.get(style_name, STYLES[DEFAULT_STYLE])
    hide_id = config.get('hide_id', False)

    body_lines = [
        r'\def\SSS{}',
        r'\OPTN{kindDrag=1}',
        r'',
        r'\begin{center}\bf\Large CHỦ ĐỀ 1 – KHẢO SÁT HÀM SỐ \end{center}',
        r'',
        r'\starttwocolumns',
        r'',
        r'\subsection*{PHẦN 1. TRẮC NGHIỆM NHIỀU PHƯƠNG ÁN LỰA CHỌN (6 điểm)}',
        r'\setcounter{ex}{0}',
        r'\Opensolutionfile{ans}[ans/\jobname-phanI]',
    ]

    for idx, q in enumerate(part1_questions):
        body_lines.append(r'\begin{ex}')
        stem_text = q['stem']
        if hide_id:
            stem_text = ORIGIN_PREFIX_RE.sub('', stem_text).strip()
        body_lines.append(stem_text)
        body_lines.append(r'\choice')
        for c_idx, choice in enumerate(q['choices']):
            if c_idx == q['correct_idx']:
                body_lines.append(f'{{\\True {choice}}}')
            else:
                body_lines.append(f'{{{choice}}}')
        body_lines.append(r'\loigiai{Lời giải chi tiết cho Câu ' + str(idx+1) + r'.}')
        body_lines.append(r'\end{ex}')
        body_lines.append('')

    body_lines += [
        r'\Closesolutionfile{ans}',
        r'\stoptwocolumns',
        r'',
        r'\subsection*{PHẦN 2. TRẮC NGHIỆM ĐÚNG SAI (2 điểm)}',
        r'\setcounter{ex}{0}',
        r'\Opensolutionfile{ans}[ans/\jobname-phanII]',
    ]

    for idx, q in enumerate(part2_questions):
        body_lines.append(r'\begin{ex}')
        stem_text = q['stem']
        if hide_id:
            stem_text = ORIGIN_PREFIX_RE.sub('', stem_text).strip()
        body_lines.append(stem_text)
        body_lines.append(r'\choiceTF')
        for s_idx, stmt in enumerate(q['statements']):
            if q['answers'][s_idx]:
                body_lines.append(f'{{\\True {stmt}}}')
            else:
                body_lines.append(f'{{{stmt}}}')
        
        body_lines.append(r'\loigiai{')
        body_lines.append(r'\begin{itemchoice}')
        for letter in ['a', 'b', 'c', 'd']:
            body_lines.append(f'\\itemch Lời giải chi tiết ý {letter}.')
        body_lines.append(r'\end{itemchoice}')
        body_lines.append(r'}')
        body_lines.append(r'\end{ex}')
        body_lines.append('')

    body_lines += [
        r'\Closesolutionfile{ans}',
        r'',
        r'\subsection*{PHẦN 3. TRẮC NGHIỆM TRẢ LỜI NGẮN (2 điểm)}',
        r'\setcounter{ex}{0}',
        r'\Opensolutionfile{ans}[ans/\jobname-phanIII]',
    ]

    for idx, q in enumerate(part3_questions):
        body_lines.append(r'\begin{ex}')
        stem_text = q['stem']
        if hide_id:
            stem_text = ORIGIN_PREFIX_RE.sub('', stem_text).strip()
        body_lines.append(stem_text)
        body_lines.append(f'\\shortans{{{q["answer"]}}}')
        body_lines.append(r'\loigiai{Lời giải chi tiết cho Câu ' + str(idx+1) + r'.}')
        body_lines.append(r'\end{ex}')
        body_lines.append('')

    body_lines += [
        r'\Closesolutionfile{ans}',
    ]

    body_path = OUTPUT_DIR / 'hsg-12-khao-sat-ham-so-body.tex'
    with open(body_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(body_lines) + '\n')
    print(f"Wrote body file to {body_path}")

    # Lấy cấu hình dynamic
    config = STYLES.get(style_name, STYLES[DEFAULT_STYLE])
    tf_layout = config.get('tf_layout', 't')
    tf_bold = '1' if config.get('tf_bold_header', True) else '0'
    tf_abbr = '1' if config.get('tf_abbreviation', False) else '0'
    tf_header = config.get('tf_header_text', 'Phát biểu').replace('&', r'\&')
    tf_dapan = config.get('tf_dapan', 'a')
    tf_sep = config.get('tf_sep', ')')
    tf_addanswers = '1' if config.get('tf_addanswers', True) else '0'
    tf_addquestions = '1' if config.get('tf_addquestions', False) else '0'
    
    sa_layout = config.get('sa_layout', 'oly')
    sa_prefix = config.get('sa_prefix', 'Đáp số:').replace('&', r'\&')
    sa_width = config.get('sa_width', 4)
    sa_dapan = config.get('sa_dapan', 'a')
    sa_height = config.get('sa_height', 0.9)

    # Khởi tạo \OPTN tương ứng
    dethi_optn = f"\\OPTN{{kindTF={tf_layout}, boldTF={tf_bold}, viettat={tf_abbr}, phatbieu={tf_header}, dapanTF={tf_dapan}, sepTF={tf_sep}, addanswers={tf_addanswers}, addquestions={tf_addquestions}, kindSA={sa_layout}, ketquaSA={sa_prefix}, widthSA={sa_width}, heightSA={sa_height}, dapanSA={sa_dapan}}}"
    loigiai_optn = f"\\OPTN{{kindTF={tf_layout}, boldTF={tf_bold}, viettat={tf_abbr}, phatbieu={tf_header}, dapanTF={tf_dapan}, sepTF={tf_sep}, addanswers={tf_addanswers}, addquestions={tf_addquestions}, kindSA={sa_layout}, ketquaSA={sa_prefix}, widthSA={sa_width}, heightSA={sa_height}, dapanSA={sa_dapan}}}"

    # Generate and write de-thi.tex
    dethi_content = generate_preamble(style_name, 'de-thi') + f"""
\\begin{{document}}
\\hideans
{dethi_optn}
\\input{{hsg-12-khao-sat-ham-so-body.tex}}
\\end{{document}}
"""
    with open(OUTPUT_DIR / "de-thi.tex", 'w', encoding='utf-8') as f:
        f.write(dethi_content)
    print(f"Wrote de-thi.tex")

    # Generate and write de-va-loigiai.tex
    loigiai_content = generate_preamble(style_name, 'de-va-loigiai') + f"""
\\begin{{document}}
% --- Thiết lập đồng bộ ---
{loigiai_optn}

\\input{{hsg-12-khao-sat-ham-so-body.tex}}
\\end{{document}}
"""
    with open(OUTPUT_DIR / "de-va-loigiai.tex", 'w', encoding='utf-8') as f:
        f.write(loigiai_content)
    print(f"Wrote de-va-loigiai.tex")

    # Generate and write dap-an.tex
    ans_cols_p1 = int(config.get('ans_table_cols', 10))
    ans_cols_p3 = max(2, ans_cols_p1 // 2)

    dapan_content = generate_preamble(style_name, 'dap-an') + f"""
% ==========================================
% PHẦN THÂN TÀI LIỆU
% ==========================================
\\begin{{document}}

\\begin{{center}}
  \\bf\\Large\\color{{myprimary}} BẢNG ĐÁP ÁN CHÍNH THỨC \\\\[0.2cm]
  \\makebox[5cm]{{\\hrulefill}}
\\end{{center}}
\\vspace{{0.5cm}}

\\noindent\\textbf{{\\color{{myprimary}}A. ĐÁP ÁN PHẦN I}}
\\vspace{{0.2cm}}

\\inputanstab{{{ans_cols_p1}}}{{ans/de-thi-phanI}}
\\vspace{{0.6cm}}

\\noindent\\textbf{{\\color{{myprimary}}B. ĐÁP ÁN PHẦN II}}
\\vspace{{0.2cm}}

\\inputanstab[1]{{2}}{{ans/de-thi-phanII}}
\\vspace{{0.6cm}}

\\noindent\\textbf{{\\color{{myprimary}}C. ĐÁP ÁN PHẦN III}}
\\vspace{{0.2cm}}

\\inputanstab[1]{{{ans_cols_p3}}}{{ans/de-thi-phanIII}}

\\end{{document}}
"""
    with open(OUTPUT_DIR / "dap-an.tex", 'w', encoding='utf-8') as f:
        f.write(dapan_content)
    print(f"Wrote dap-an.tex")

if __name__ == '__main__':
    main()
