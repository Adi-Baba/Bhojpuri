# Bhojpuri Kosh (भोजपुरी कोश) --- Trilingual Lexicon

A comprehensive, modular LaTeX dictionary of the Bhojpuri language, typeset in **Kaithi script**, **Devanagari**, and **English**, compiled with **LuaLaTeX**.

## Goal & Mission

Since Bhojpuri faces severe language endangerment and script extinction, **Bhojpuri Kosh** provides a **Trilingual (Bhojpuri + Hindi + English)** reference lexicon.
- **For Hindi / Devanagari speakers**: Seamless transition to learning Bhojpuri vocabulary and the historical Kaithi script through familiar Devanagari glosses.
- **For International & Non-Hindi Audiences**: Full English translations, grammatical classification, and Latin transliteration enable global access, academic research, and preservation.

## Current State

| Section | Status |
|---|---|
| Title page | Done (Trilingual: Kaithi + Devanagari + English) |
| Abbreviations (Grammatical terms in Hi/En) | Done |
| Varnamala (Phonemic inventory + Matras + Conjuncts) | Done |
| Shabd Kosh (Main Trilingual Dictionary) | Done — `pages/shabd/shabd.tex` |
| Samasya (Word puzzles) | Placeholder — `pages/samasya/` |
| Muhavare (Idioms) | Placeholder — `pages/muhavare/` |
| Lok-katha (Folk tales) | Placeholder — `pages/lok-katha/` |
| Vyakaran (Grammar) | Placeholder — `pages/vyakaran/` |

## Project Structure

```
BhojDic/
├── main.tex                  # Entry point — compile with LuaLaTeX
├── Makefile                  # make build / make clean
├── config/
│   ├── colors.tex            # Blue color theme (bpblue, bpgold, etc.)
│   ├── fonts.tex             # Kaithi macros + LuaLaTeX font fallbacks
│   ├── packages.tex          # Package imports (longtable, tikz, etc.)
│   └── layout.tex            # Page geometry, headers, section styling
├── components/
│   ├── title/title.tex       # Title page
│   ├── abbreviations/        # Grammatical abbreviation tables
│   └── varnamala/            # Complete Kaithi + Devanagari phonemic inventory
├── pages/                    # Content modules
│   ├── shabd/shabd.tex       # Shabd Kosh — Main Trilingual Dictionary
│   ├── samasya/              # Word puzzles
│   ├── muhavare/             # Idioms and proverbs
│   ├── lok-katha/            # Folk tales and stories
│   └── vyakaran/             # Grammar reference
└── fonts/
    └── NotoSansKaithi-Regular.ttf
```

## Building

Requires a TeX Live installation with LuaLaTeX and Noto Sans fonts.

```bash
cd BhojDic
make build        # runs lualatex twice
# or directly:
lualatex -interaction=nonstopmode -halt-on-error main.tex
lualatex -interaction=nonstopmode -halt-on-error main.tex
```

Output: `main.pdf`

## Font & Script Architecture

### Font Fallback System (`luaotfload`)

`config/fonts.tex` uses LuaLaTeX's native font fallback system (`luaotfload.add_fallback`) to merge `Noto Sans Devanagari` and `Noto Sans Kaithi` seamlessly into `Noto Sans`. This guarantees that:
1. Devanagari combining marks (matras, halants, and conjuncts) shape naturally without macro hacks.
2. Kaithi characters display cleanly via `\K{...}` wrapper macros.

### Kaithi Macro System (`\b...`)

All Kaithi characters use standard `\b`-prefixed macros corresponding to Unicode codepoints (U+11080–U+110C1):

```latex
\def\bka{\char"1108D}    % Ka (क)
\def\bkha{\char"1108E}   % Kha (ख)
\def\bvir{\char"110B9}   % Virama (Halant)
\def\bmaa{\char"110B0}   % Matra AA (ा)
```

**Usage in `.tex` files:**

```latex
% Kaithi word
\K{\bka\bmai\btha\bmi \bla\bmi\bpa\bmi}  % renders 𑂍𑂶𑂟𑂱 𑂪𑂱𑂣𑂱 (Kaithi Lipi)

% Kaithi conjunct
\K{\bka\bvir\bka}                        % renders 𑂍𑂹𑂍 (kka)
```

### Font Requirements

| Font | Used For | System Path |
|---|---|---|
| Noto Sans Kaithi | Kaithi script | `/usr/share/fonts/truetype/noto/NotoSansKaithi-Regular.ttf` |
| Noto Sans Devanagari | Devanagari labels | `/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf` |
| Noto Sans | English/Latin text | `/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf` |

## Trilingual Dictionary Entry Format

Each entry in `pages/shabd/shabd.tex` provides:
1. **Kaithi Script** (`\K{...}`)
2. **Devanagari Bhojpuri**
3. **Latin Transliteration**
4. **Grammatical Tag** (e.g. `n. f.`, `v.`, `adj.`)
5. **Hindi Translation** (हिन्दी अर्थ)
6. **English Gloss**
7. **Bilingual Sample Sentences** (Bhojpuri Kaithi, Bhojpuri Devanagari, Hindi, English)

## Credits

- **Kaithi Font**: Noto Sans Kaithi (Google Fonts)
- **Devanagari Font**: Noto Sans Devanagari (Google Fonts)
- Built with LuaLaTeX + fontspec + luaotfload
