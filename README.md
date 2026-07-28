# 🌾 Bhojpuri Lexicon (भोजपुरी शब्दकोश)

> **A scholarly, print-ready trilingual Bhojpuri–Hindi–English dictionary rendered in Devanagari and authentic Kaithi (𑂍𑂶𑂟𑂲) script.**

---

## 📌 Project Overview

**Bhojpuri Lexicon** is a foundational lexicographical effort to document, preserve, and revitalize the vocabulary of the Bhojpuri language. Compiled using TeX/LuaLaTeX, it bridges classical scholarship with modern print typography.

Key features include:
* **Trilingual Format**: Bhojpuri Headword $\rightarrow$ Hindi Meaning $\rightarrow$ English Gloss.
* **Dual Script Representation**: Every headword is rendered in Devanagari alongside its historical **Kaithi script (𑂍𑂶𑂟𑂲)** counterpart using Google Noto Sans Kaithi fonts.
* **⭐ Real-Life Priority Star System**:
  - `★★★` **Core Spoken**: Essential everyday vocabulary with mandatory Bhojpuri usage example sentences.
  - `★★` **Formal / Regional**: Terms used in formal registers, literature, or specific dialects.
  - `★` **Literary / Archaic**: Rare, poetic, agricultural, or historical terms.
* **🏗️ The Nest Visual Hierarchy**:
  - **Root Word**: Prominent bold entry (`\bhojentry`).
  - **Direct Derivatives**: Indented with `↳` (`\bhojsubentry`).
  - **Compounds**: Double-indented with `$\rightarrow$` (`\bhojcompound`).
* **🗺️ Regional Dialect Tagging**:
  - `[पूर्वी]` Eastern (Saran, Champaran, Ballia)
  - `[पच्छिमी]` Western (Gorakhpur, Deoria, Basti)
  - `[दक्षिणी]` Southern (Bhojpur, Buxar, Rohtas)
  - `[ठेठ]` Universal spoken Bhojpuri

---

## 🗂️ Repository Structure

```
BhojPuriRevive/
├── BhojDic/
│   ├── main.tex                    # Master LaTeX file
│   ├── main.pdf                    # Compiled print-ready PDF
│   ├── config/                     # Layout, font & color configurations
│   │   ├── colors.tex              # Color palette definitions
│   │   ├── fonts.tex               # Noto Sans & Kaithi font setups
│   │   ├── layout.tex              # Lexicon macros (\bhojentry, \starsThree, etc.)
│   │   └── packages.tex            # LaTeX packages
│   ├── components/                 # Front matter components
│   │   ├── title/title.tex         # Title page
│   │   ├── how_to_use/how_to_use.tex# How to use this dictionary guide page
│   │   ├── abbreviations/          # Origin tags & abbreviation legend
│   │   └── varnamala/              # Devanagari & Kaithi alphabet chart
│   └── pages/shabd/                # Modular dictionary entry files
│       ├── shabd.tex               # Master index file
│       ├── a.tex                   # Initial vowel 'अ' (225 words)
│       ├── an_anusvara.tex         # Anusvara vowel 'अं' (45+ words)
│       ├── am_chandrabindu.tex     # Chandrabindu vowel 'अँ' (45+ words)
│       └── aa.tex                  # Initial vowel 'आ' (In progress)
├── KaithiFont/                     # OpenSource Noto Sans Kaithi fonts
└── RefHindiDict/                   # Reference lexicographical materials
```

---

## 🛠️ Build Instructions

To compile the dictionary locally, ensure you have **LuaLaTeX** and **TeX Live** installed.

```bash
cd BhojDic
lualatex -interaction=nonstopmode -halt-on-error main.tex
```

---

## 📄 License & Attribution

* **Text & Lexicon**: Open Access for educational, scholarly, and cultural preservation purposes.
* **Fonts**: Google Noto Sans Kaithi (SIL Open Font License).
