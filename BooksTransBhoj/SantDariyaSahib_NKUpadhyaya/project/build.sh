#!/usr/bin/env bash
# Build the N. K. Upadhyaya edition from any current working directory.
set -euo pipefail

readonly SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly TEX_DIR="${SCRIPT_DIR}/tex"
readonly MAIN_FILE="dariya_nk_upadhyaya.tex"
readonly PDF_FILE="${MAIN_FILE%.tex}.pdf"

command -v lualatex >/dev/null || {
  echo "Error: lualatex is not installed or is not on PATH." >&2
  exit 127
}

cd "${TEX_DIR}"
echo "Building N. K. Upadhyaya Dariya Baba PDF..."

# Two passes resolve the table of contents and cross-references.
for pass in 1 2; do
  echo "LuaLaTeX pass ${pass}/2..."
  lualatex -interaction=nonstopmode -halt-on-error -file-line-error "${MAIN_FILE}"
done

echo "Done: ${TEX_DIR}/${PDF_FILE}"
