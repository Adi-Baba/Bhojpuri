import os
import re
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(SCRIPT_DIR, "source/translations")
TEX_DIR = os.path.join(SCRIPT_DIR, "tex")
FONTS_DIR = os.path.join(SCRIPT_DIR, "fonts")
TEX_FILE = os.path.join(TEX_DIR, "manifesto_bhojpuri.tex")

def check_dependencies():
    errors = []
    for cmd in [["lualatex", "--version"], ["inkscape", "--version"]]:
        try:
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except FileNotFoundError:
            errors.append(f"{cmd[0]} not found — is it installed?")
    required_fonts = [
        "TiroDevanagariSanskrit-Regular.ttf",
        "TiroDevanagariSanskrit-Italic.ttf",
        "Kurale-Regular.ttf",
    ]
    for f in required_fonts:
        if not os.path.exists(os.path.join(FONTS_DIR, f)):
            errors.append(f"Font not found: fonts/{f}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        sys.exit(1)
    print("All dependencies ok.")

check_dependencies()

section_files = [
    "00_translators_preface.txt",
    "01_biography.txt",
    "02_manifesto_of_the_communist_party.txt",
    "03_i._bourgeois_and_proletarians.txt",
    "04_ii._proletarians_and_communists.txt",
    "05_iii._socialist_and_communist_literature.txt",
    "06_1._reactionary_socialism.txt",
    "07_2._conservative_or_bourgeois_socialism.txt",
    "08_3._critical-utopian_socialism_and_communism.txt",
    "09_iv._position_of_the_communists_in_relation_to_the_various_existing_opposition_parties.txt",
    "10_appendix_glossary.txt"
]

new_page_sections = {
    "00_translators_preface.txt",
    "01_biography.txt",
    "02_manifesto_of_the_communist_party.txt",
    "03_i._bourgeois_and_proletarians.txt",
    "04_ii._proletarians_and_communists.txt",
    "05_iii._socialist_and_communist_literature.txt",
    "09_iv._position_of_the_communists_in_relation_to_the_various_existing_opposition_parties.txt",
    "10_appendix_glossary.txt"
}

def latex_escape(text):
    text = text.replace('\\', '\\textbackslash{}')
    text = text.replace('%', '\\%')
    text = text.replace('$', '\\$')
    text = text.replace('#', '\\#')
    text = text.replace('_', '\\_')
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    text = text.replace('~', '\\textasciitilde{}')
    text = text.replace('^', '\\textasciicircum{}')

    # Standardize quotation marks: convert straight " " into curly “ ”
    text = re.sub(r'"([^"]+)"', r'“\1”', text)

    def wrap_eng_parens(match):
        return f'{{\\engfont ({match.group(1)})}}'
    
    text = re.sub(r'\(([A-Za-z0-9\s/&,.\'\-;:?!]+)\)', wrap_eng_parens, text)

    parts = re.split(r'(\{\\engfont [^}]+\})', text)
    new_parts = []
    for part in parts:
        if part.startswith('{\\engfont'):
            new_parts.append(part.replace('&', '\\&'))
        else:
            new_parts.append(part.replace('&', 'आ'))
    text = "".join(new_parts)

    text = re.sub(r'^I\.\s*', r'भाग {\\engfont I}. ', text)
    text = re.sub(r'^II\.\s*', r'भाग {\\engfont II}. ', text)
    text = re.sub(r'^III\.\s*', r'भाग {\\engfont III}. ', text)
    text = re.sub(r'^IV\.\s*', r'भाग {\\engfont IV}. ', text)
    text = re.sub(r'^A\.\s*', r'{\\engfont A}. ', text)
    text = re.sub(r'^B\.\s*', r'{\\engfont B}. ', text)
    text = re.sub(r'^C\.\s*', r'{\\engfont C}. ', text)
    text = re.sub(r'^1\.\s*', r'{\\engfont 1}. ', text)
    text = re.sub(r'^2\.\s*', r'{\\engfont 2}. ', text)
    text = re.sub(r'^3\.\s*', r'{\\engfont 3}. ', text)
    # Convert [footnote: ...] or [fn: ...] into \footnote{...}
    text = re.sub(r'\[(?:footnote|fn):\s*(.*?)\]', r'\\footnote{\1}', text)

    return text

latex_body = []
in_table = False
table_rows = []

for filename in section_files:
    filepath = os.path.join(SOURCE_DIR, filename)
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} does not exist.")
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.split("\n")]
    
    is_first_line = True
    for line in lines:
        if not line:
            continue
        
        if line.startswith("┌") or line.startswith("│") or line.startswith("├") or line.startswith("└"):
            if line.startswith("┌"):
                in_table = True
                table_rows = []
            elif line.startswith("├"):
                pass
            elif line.startswith("└"):
                if table_rows:
                    latex_table = [
                        r"\begingroup",
                        r"\small",
                        r"\begin{longtable}{|l|l|p{7.5cm}|}",
                        r"\hline"
                    ]
                    header = table_rows[0]
                    latex_table.append(" & ".join([f"\\textbf{{{latex_escape(c)}}}" for c in header]) + r" \\ \hline \endhead")
                    for row in table_rows[1:]:
                        latex_table.append(" & ".join([latex_escape(c) for c in row]) + r" \\ \hline")
                    latex_table.append(r"\end{longtable}")
                    latex_table.append(r"\endgroup")
                    latex_body.append("\n".join(latex_table) + "\n\n")
                in_table = False
                table_rows = []
            elif line.startswith("│"):
                parts = [p.strip() for p in line.split("│")[1:-1]]
                if parts:
                    table_rows.append(parts)
            continue

        escaped_line = latex_escape(line)

        if is_first_line:
            if filename in new_page_sections:
                latex_body.append(f"\\cleardoublepage\n\\chapter*{{{escaped_line}}}\n\\phantomsection\\addcontentsline{{toc}}{{chapter}}{{{escaped_line}}}\n")
            else:
                latex_body.append(f"\n\\section*{{{escaped_line}}}\n\\phantomsection\\addcontentsline{{toc}}{{section}}{{{escaped_line}}}\n")
            is_first_line = False
        elif line.startswith("A.") or line.startswith("B.") or line.startswith("C.") or line.startswith("भूमिका") or re.match(r'^(\([०-९]+\)|\([0-9]+\)|[0-9]+\.|[०-९]+\.)', line):
            latex_body.append(f"\n\\subsection*{{{escaped_line}}}\n")
        else:
            is_first_line = False
            latex_body.append(f"{escaped_line}\n\n")

latex_content = r"""\documentclass[12pt,a4paper,oneside]{book}
\usepackage{fontspec}
\usepackage{geometry}
\usepackage{xcolor}
\usepackage{array}
\usepackage{longtable}
\usepackage{booktabs}
\usepackage{tikz}
\usepackage{graphicx}
\usepackage{svg}
\usepackage{pagecolor}
\usepackage{setspace}
\usepackage{titlesec}
\usepackage{fancyhdr}
\usepackage{microtype}
\usepackage{amssymb}
\usepackage{tocloft}
\usepackage{luacode}
\usepackage[colorlinks=true, linkcolor=bordercolor, citecolor=bordercolor, urlcolor=bordercolor, pdfborder={0 0 0}]{hyperref}

% Devanagari page numerals via Lua
\begin{luacode*}
function devanagari(num)
  local n = tonumber(num)
  if not n then return tostring(num) end
  local digits = {"०","१","२","३","४","५","६","७","८","९"}
  local s = ""
  if n == 0 then return "०" end
  while n > 0 do
    s = digits[n % 10 + 1] .. s
    n = math.floor(n / 10)
  end
  return s
end
\end{luacode*}

% Warn on missing glyphs in log (does not stop build)
\tracinglostchars=2

% Page Geometry
\geometry{
  a4paper,
  left=25mm,
  right=25mm,
  top=28mm,
  bottom=28mm
}

% Colors - Matmaila / Vintage Parchment Theme
\definecolor{matmaila}{HTML}{C5B99D}      % Authentic matmaila earthy beige parchment
\definecolor{matmailadark}{HTML}{2B251F}  % Deep charcoal brown text
\definecolor{bordercolor}{HTML}{3D3428}   % Vintage dark brown frame

% Fonts Configuration
\setmainfont{TiroDevanagariSanskrit}[
  Path=../fonts/,
  Extension=.ttf,
  Renderer=HarfBuzz,
  Script=Devanagari,
  Language=Hindi,
  UprightFont=*-Regular,
  ItalicFont=*-Italic,
  BoldFont=*-Regular,
  AutoFakeBold
]

\newfontfamily\kurale{Kurale-Regular}[
  Path=../fonts/,
  Extension=.ttf,
  Renderer=HarfBuzz,
  Script=Devanagari,
  Language=Hindi
]

\newfontfamily\engfont{Latin Modern Roman}

% Configure itemize bullet to use engfont textbullet
\renewcommand{\labelitemi}{\engfont\textbullet}

\renewcommand{\cftchapfont}{\normalfont}
\renewcommand{\cftchappagefont}{\normalfont}
\renewcommand{\cftsecfont}{\normalfont}
\renewcommand{\cftsecpagefont}{\normalfont}

\renewcommand{\cftchapfillnum}[1]{%
  \cftchapleader
  {\cftchappagefont \directlua{tex.print(devanagari("#1"))}}%
  \cftchapafterpnum\par
}
\renewcommand{\cftsecfillnum}[1]{%
  \cftsecleader
  {\cftsecpagefont \directlua{tex.print(devanagari("#1"))}}%
  \cftsecafterpnum\par
}

% Line Spacing
\setstretch{1.35}

% Paragraph Formatting
\setlength{\parindent}{1.5em}
\setlength{\parskip}{0.5em}

% Section Titles Styling
\titleformat{\chapter}[block]
  {\centering\LARGE\bfseries\color{bordercolor}}
  {}{0pt}{}
  [\vspace{0.4em}{\color{bordercolor}\rule{0.35\textwidth}{0.8pt}}\vspace{0.8em}]

\titleformat{\section}[block]
  {\Large\bfseries\color{bordercolor}}
  {}{0pt}{}

\titleformat{\subsection}[block]
  {\large\bfseries\color{bordercolor}}
  {}{0pt}{}

% Quote Styling
\usepackage{tcolorbox}
\tcbuselibrary{breakable, skins}
\newenvironment{customquote}
  {\begin{tcolorbox}[blanker, breakable, left=12pt, top=4pt, bottom=4pt, borderline left={1.5pt}{0pt}{bordercolor}]
   \small\itshape}
  {\end{tcolorbox}}

% Footnote Styling
\begin{luacode*}
function devanagari_fn()
  local val = tex.count["c@footnote"]
  tex.print(devanagari(val))
end
\end{luacode*}

\renewcommand{\footnoterule}{%
  \kern -3pt
  \color{bordercolor}\hrule width 0.35\textwidth height 0.6pt
  \kern 2.5pt
}
\setlength{\footnotesep}{0.8em}
\makeatletter
\renewcommand{\@makefnmark}{\textsuperscript{\directlua{devanagari_fn()}}}
\renewcommand{\@makefntext}[1]{%
  \parindent 1em\noindent
  \hb@xt@1.5em{\hss\textsuperscript{\directlua{devanagari_fn()}}~}#1}
\makeatother

% Header and Footer - Devanagari Page Numbers
\pagestyle{fancy}
\fancyhf{}
\fancyfoot[C]{\color{bordercolor}\small\directlua{tex.print(devanagari(tex.count[0]))}}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Redefine plain page style for TOC and chapter pages
\fancypagestyle{plain}{%
  \fancyhf{}%
  \fancyfoot[C]{\color{bordercolor}\small\directlua{tex.print(devanagari(tex.count[0]))}}%
  \renewcommand{\headrulewidth}{0pt}%
  \renewcommand{\footrulewidth}{0pt}%
}

\begin{document}
\pagenumbering{arabic}
\pagecolor{matmaila}
\color{matmailadark}

% ================= PAGE I: FRONT COVER =================
\begin{titlepage}
\thispagestyle{empty}

\begin{tikzpicture}[remember picture, overlay]
  % Outer Double Frame Lines
  \draw[line width=1.2pt, color=bordercolor] 
    ([yshift=-10mm, xshift=10mm]current page.north west) rectangle 
    ([yshift=10mm, xshift=-10mm]current page.south east);

  \draw[line width=0.5pt, color=bordercolor] 
    ([yshift=-12mm, xshift=12mm]current page.north west) rectangle 
    ([yshift=12mm, xshift=-12mm]current page.south east);

  % Top Decorative Ornamental Dots Bar
  \draw[line width=1.2pt, color=bordercolor] 
    ([yshift=-20mm, xshift=18mm]current page.north west) -- 
    ([yshift=-20mm, xshift=-18mm]current page.north east);
  
  \foreach \x in {-7.5,-6,-4.5,-3,-1.5,0,1.5,3,4.5,6,7.5} {
    \node[color=bordercolor, font=\engfont] at ([yshift=-17mm, xshift=\x cm]current page.north) {\small $\therefore$};
  }

  % Bottom Decorative Ornamental Dots Bar
  \draw[line width=1.2pt, color=bordercolor] 
    ([yshift=20mm, xshift=18mm]current page.south west) -- 
    ([yshift=20mm, xshift=-18mm]current page.south east);
  
  \foreach \x in {-7.5,-6,-4.5,-3,-1.5,0,1.5,3,4.5,6,7.5} {
    \node[color=bordercolor, font=\engfont] at ([yshift=23mm, xshift=\x cm]current page.south) {\small $\because$};
  }
\end{tikzpicture}

\vspace*{1.2cm}

\begin{center}
  % Main Header / Title Block
  {\Huge \bfseries \color{matmailadark} कम्युनिस्ट पार्टी के घोषणापत्र} \\[0.7em]
  {\large \color{bordercolor} {\engfont (The Communist Manifesto)}} \\[0.4em]
  {\small \color{bordercolor} भोजपुरी अनुवाद} \\[1.8cm]

  % Center Emblem: Direct SVG Integration using \includesvg
  \includesvg[width=6.0cm]{cropped-communist_emblem.svg}

  \vfill

  % Bottom Left Metadata Block
  \begin{flushleft}
  \hspace*{1.0cm}
  \begin{tikzpicture}
    \draw[line width=1.8pt, color=bordercolor] (0,0) -- (0, 2.4);
    \node[anchor=west, text width=12.5cm, color=matmailadark, font=\normalfont] at (0.35, 1.2) {
      \small
      {\bfseries मूल लेखक:} कार्ल मार्क्स आ फ्रेडरिक एंगेल्स \\
      {\bfseries भोजपुरी अनुवाद:} आदित्य कुमार \\
      {\bfseries भाषा शैली:} भोजपुरी \\
      {\bfseries परियोजना:} भोजपुरी रिवाइव प्रोजेक्ट {\engfont (Bhojpuri Revive Project)} \\
      {\bfseries संस्करण:} प्रथम भोजपुरी संस्करण (2026)
    };
  \end{tikzpicture}
  \end{flushleft}
\end{center}

\vspace*{0.8cm}
\end{titlepage}

% ================= PAGE II: DEDICATED COPYRIGHT PAGE =================
\newpage
\thispagestyle{empty}

\begin{center}
  {\Large \bfseries \color{bordercolor} कम्युनिस्ट पार्टी के घोषणापत्र} \\[0.2em]
  {\small \color{bordercolor} {\engfont (The Communist Manifesto --- Bhojpuri Translation)}} \\[0.4em]
  {\color{bordercolor}\rule{0.35\textwidth}{0.8pt}}
\end{center}

\vspace*{0.3cm}

\begin{center}
\begin{minipage}{0.92\textwidth}
  \small
  \setstretch{1.25}
  \setlength{\parskip}{0.3em}

  {\bfseries पुस्तक का नाम:} कम्युनिस्ट पार्टी के घोषणापत्र \\
  {\bfseries मूल रचयिता:} कार्ल मार्क्स आ फ्रेडरिक एंगेल्स (1848) \\
  {\bfseries भोजपुरी अनुवादक:} आदित्य कुमार {\engfont (Aditya Kumar)} \\
  {\bfseries भाषा शैली:} भोजपुरी \\
  {\bfseries सर्वाधिकार:} {\engfont \copyright} 2026 आदित्य कुमार (सर्वहक़ सुरक्षित) \\
  {\bfseries प्रथम संस्करण:} 2026

  \vspace*{0.4em}

  \begin{tcolorbox}[colframe=bordercolor, colback=matmaila!70!white, arc=3pt, boxrule=0.8pt, top=4pt, bottom=4pt, title={\bfseries अनुदित संस्करण विवरण {\engfont (Translated Edition Details)}}]
  \small
  \begin{itemize}\setlength{\itemsep}{0.1em}\setlength{\topsep}{0pt}\setlength{\parsep}{0pt}
    \item {\bfseries मुख्य अनुवाद आधार (Primary Source):} {\engfont The Communist Manifesto (Illustrated Edition), Karl Marx \& Friedrich Engels (2014, ASIN: B00MJJ7YZE)}
    \item {\bfseries मूल जर्मन संस्करण (Original German):} {\engfont Manifest der Kommunistischen Partei (1848)}
    \item {\bfseries संदर्भ आर्काइव (Reference Archives):} {\engfont Marxists Internet Archive (MIA) \& Anna's Archive}
  \end{itemize}
  \end{tcolorbox}

  \vspace*{0.4em}
  {\color{bordercolor}\rule{\textwidth}{0.4pt}}
  \vspace*{0.4em}

  {\bfseries सर्वाधिकार आ लाइसेंस संबंधी शर्त {\engfont (Copyright Notice)}:}

  \begin{itemize}\setlength{\itemsep}{0.2em}\setlength{\topsep}{0pt}\setlength{\parsep}{0pt}
    \item {\bfseries व्यक्तिगत उपयोग {\engfont (Personal Use)}:} ई भोजपुरी अनुवाद केवल व्यक्तिगत पठन, निजी अध्ययन आ गैर-व्यावसायिक पठन खातिर मुफ़्त उपलब्ध बा।
    \item {\bfseries व्यावसायिक आ अकादमिक छपाई {\engfont (Commercial Mass Printing)}:} कवनो प्रकार के व्यावसायिक प्रकाशन, बड़े पैमाने पर छपाई {\engfont (Mass Printing)}, या व्यावसायिक अकादमिक उपयोग खातिर अनुवादक (आदित्य कुमार) से लिखित पूर्वानुमति आ रॉयल्टी {\engfont (Royalty Agreement)} लेहल अनिवार्य बा।
  \end{itemize}

  \vspace*{0.4em}
  {\color{bordercolor}\rule{\textwidth}{0.4pt}}
  \vspace*{0.4em}

  \begin{center}
    {\engfont \copyright{} 2026 Aditya Kumar. All Rights Reserved.} \\
    {\footnotesize {\engfont Free for personal non-commercial study only. Commercial printing requires prior written permission.}} \\
    \vspace*{0.3em}
    {\small स्वतंत्र अनुवाद परियोजना | भोजपुरी रिवाइव प्रोजेक्ट {\engfont (Bhojpuri Revive Project)}}
  \end{center}
\end{minipage}
\end{center}

% ================= PAGE III: TABLE OF CONTENTS (विषय-सूची - SINGLE PAGE) =================
\newpage
\thispagestyle{empty}

\begin{center}
  {\Large \bfseries \color{bordercolor} विषय-सूची} \\[0.4em]
  {\color{bordercolor}\rule{0.3\textwidth}{0.8pt}}
\end{center}

\vspace*{0.6cm}

\renewcommand{\contentsname}{}
\setcounter{tocdepth}{2}
{\makeatletter
\renewcommand{\@dotsep}{4.5}
\makeatother
\tableofcontents}

\vfill
\begin{center}
  {\small \color{bordercolor} भोजपुरी रिवाइव प्रोजेक्ट | प्रथम भोजपुरी संस्करण (2026)}
\end{center}

\newpage

% ================= MAIN BODY CONTENT =================
\cleardoublepage
""" + "".join(latex_body) + r"""
\end{document}
"""

with open(TEX_FILE, "w", encoding="utf-8") as f:
    f.write(latex_content)

print(f"Generated {TEX_FILE} successfully.")

# Run LuaLaTeX with -shell-escape to enable direct LaTeX \includesvg integration
# Three passes are needed to resolve cross-references and TOC.
try:
    cmd = ["lualatex", "-shell-escape", "-interaction=nonstopmode", "manifesto_bhojpuri.tex"]
    for i in range(3):
        res = subprocess.run(cmd, cwd=TEX_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            print(f"LuaLaTeX run {i+1}/3 returned code {res.returncode} (may be non-fatal), continuing...")
    pdf_path = os.path.join(TEX_DIR, "manifesto_bhojpuri.pdf")
    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 50000:
        print(f"PDF compilation SUCCESSFUL: {pdf_path}")
    else:
        print("ERROR: PDF was not generated or is too small.")
        sys.exit(1)
except Exception as e:
    print("Error running LuaLaTeX:", e)
    sys.exit(1)
