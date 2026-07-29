import os
import re
import subprocess

SOURCE_DIR = "/home/aditya/Documents/BhojPuriRevive/BooksTransBhoj/CommunistManifestoBhojTrans/project/source/translations"
TEX_DIR = "/home/aditya/Documents/BhojPuriRevive/BooksTransBhoj/CommunistManifestoBhojTrans/project/tex"
TEX_FILE = os.path.join(TEX_DIR, "manifesto_bhojpuri.tex")

section_files = [
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

    def wrap_eng_parens(match):
        return f'{{\\engfont ({match.group(1)})}}'
    
    text = re.sub(r'\(([A-Za-z0-9\s/&,.\'-]+)\)', wrap_eng_parens, text)

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
    return text

latex_body = []

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
        
        escaped_line = latex_escape(line)

        if is_first_line:
            if filename in new_page_sections:
                latex_body.append(f"\\cleardoublepage\n\\section*{{{escaped_line}}}\n\\phantomsection\\addcontentsline{{toc}}{{section}}{{{escaped_line}}}\n")
            else:
                latex_body.append(f"\n\\subsection*{{{escaped_line}}}\n\\phantomsection\\addcontentsline{{toc}}{{subsection}}{{{escaped_line}}}\n")
            is_first_line = False
        elif line.startswith("A.") or line.startswith("B.") or line.startswith("C.") or line.startswith("भूमिका") or re.match(r'^[1234567890]+\.', line):
            latex_body.append(f"\n\\subsection*{{{escaped_line}}}\n")
        else:
            is_first_line = False
            latex_body.append(f"{escaped_line}\n\n")

latex_content = r"""\documentclass[12pt,a4paper,oneside]{article}
\usepackage{fontspec}
\usepackage{geometry}
\usepackage{xcolor}
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
\usepackage[colorlinks=true, linkcolor=bordercolor, citecolor=bordercolor, urlcolor=bordercolor, pdfborder={0 0 0}]{hyperref}

% Suppress lost character log warnings globally
\tracinglostchars=0

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
\setmainfont{Noto Serif Devanagari}[
  Renderer=HarfBuzz,
  Script=Devanagari,
  Language=Hindi,
  UprightFont=*-Regular,
  BoldFont=*-Bold
]

\newfontfamily\engfont{Latin Modern Roman}

% Configure itemize bullet to use engfont textbullet
\renewcommand{\labelitemi}{\engfont\textbullet}

% Universal TOC Page Number Box Width (4.5em reserved for Roman numerals like XXVII)
\makeatletter
\renewcommand{\@pnumwidth}{4.5em}
\renewcommand{\@tocrmarg}{5.0em}
\makeatother

\renewcommand{\cftsecpagefont}{\engfont}
\renewcommand{\cftsubsecpagefont}{\engfont}
\renewcommand{\cftsecfont}{\normalfont}
\renewcommand{\cftsubsecfont}{\normalfont}

% Line Spacing
\setstretch{1.35}

% Paragraph Formatting
\setlength{\parindent}{1.5em}
\setlength{\parskip}{0.5em}

% Section Titles Styling
\titleformat{\section}[block]
  {\centering\Large\bfseries\color{bordercolor}}
  {}{0pt}{}
  [\vspace{0.4em}{\color{bordercolor}\rule{0.35\textwidth}{0.8pt}}\vspace{0.8em}]

\titleformat{\subsection}[block]
  {\large\bfseries\color{bordercolor}}
  {}{0pt}{}

% Header and Footer - Roman Page Numbers
\pagestyle{fancy}
\fancyhf{}
\fancyfoot[C]{\color{bordercolor}\small{\engfont \thepage}}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Redefine plain page style for TOC and chapter pages so footer uses engfont
\fancypagestyle{plain}{%
  \fancyhf{}%
  \fancyfoot[C]{\color{bordercolor}\small{\engfont \thepage}}%
  \renewcommand{\headrulewidth}{0pt}%
  \renewcommand{\footrulewidth}{0pt}%
}

\begin{document}
\pagenumbering{Roman}
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
  \includesvg[width=6.0cm]{communist_emblem.svg}

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

\vfill
\begin{center}
  {\Large \bfseries \color{bordercolor} कम्युनिस्ट पार्टी के घोषणापत्र} \\[0.3em]
  {\small \color{bordercolor} {\engfont (The Communist Manifesto --- Bhojpuri Translation)}} \\[1.5em]
  {\color{bordercolor}\rule{0.4\textwidth}{0.8pt}}
\end{center}

\vspace*{1.2cm}

\begin{center}
\begin{minipage}{0.88\textwidth}
  \small
  \setstretch{1.3}
  \setlength{\parskip}{0.7em}

  {\bfseries पुस्तक का नाम:} कम्युनिस्ट पार्टी के घोषणापत्र \\
  {\bfseries मूल रचयिता:} कार्ल मार्क्स आ फ्रेडरिक एंगेल्स (1848) \\
  {\bfseries भोजपुरी अनुवादक:} आदित्य कुमार {\engfont (Aditya Kumar)} \\
  {\bfseries भाषा शैली:} भोजपुरी \\
  {\bfseries सर्वाधिकार:} {\engfont \copyright} 2026 आदित्य कुमार (सर्वहक़ सुरक्षित) \\
  {\bfseries प्रथम संस्करण:} 2026

  \vspace*{1.0em}
  {\color{bordercolor}\rule{\textwidth}{0.4pt}}
  \vspace*{1.0em}

  {\bfseries सर्वाधिकार आ लाइसेंस संबंधी शर्त {\engfont (Copyright Notice)}:}

  \begin{itemize}\setlength{\itemsep}{0.4em}
    \item {\bfseries व्यक्तिगत उपयोग {\engfont (Personal Use)}:} ई भोजपुरी अनुवाद केवल व्यक्तिगत पठन, निजी अध्ययन आ गैर-व्यावसायिक पठन खातिर मुफ़्त उपलब्ध बा।
    \item {\bfseries व्यावसायिक आ अकादमिक छपाई {\engfont (Commercial \& Academic Mass Printing)}:} कवनो प्रकार के व्यावसायिक प्रकाशन, बड़े पैमाने पर छपाई {\engfont (Mass Printing)}, व्यावसायिक संस्थान या अकादमिक संस्थाओं द्वारा बड़े पैमाने पर वितरण या व्यावसायिक उपयोग खातिर अनुवादक (आदित्य कुमार) से लिखित पूर्वानुमति आ रॉयल्टी {\engfont (Royalty Agreement)} लेहल अनिवार्य बा।
  \end{itemize}

  \vspace*{0.8em}
  {\color{bordercolor}\rule{\textwidth}{0.4pt}}
  \vspace*{0.8em}

  \begin{center}
    {\engfont \copyright{} 2026 Aditya Kumar. All Rights Reserved.} \\
    {\small {\engfont Free for personal non-commercial study only. Commercial printing, mass distribution, or commercial academic use requires prior written permission and royalty licensing.}} \\
    \vspace*{0.5em}
    {\small स्वतंत्र अनुवाद परियोजना | भोजपुरी रिवाइव प्रोजेक्ट {\engfont (Bhojpuri Revive Project)}}
  \end{center}
\end{minipage}
\end{center}
\vfill

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
try:
    cmd = ["lualatex", "-shell-escape", "-interaction=nonstopmode", "manifesto_bhojpuri.tex"]
    for i in range(3):
        res = subprocess.run(cmd, cwd=TEX_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        print("PDF compilation SUCCESSFUL with 0 errors!")
    else:
        print("LuaLaTeX finished.")
except Exception as e:
    print("Error running LuaLaTeX:", e)
