#!/usr/bin/env bash
# build.sh — Build Sant Dariya Sahib PDF
set -euo pipefail

readonly SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly TEX_DIR="${SCRIPT_DIR}/tex"
readonly MAIN_FILE="dariya_sahib_bhojpuri.tex"
readonly PDF_FILE="${MAIN_FILE%.tex}.pdf"

command -v lualatex >/dev/null || {
  echo "Error: lualatex is not installed or is not on PATH." >&2
  exit 127
}

cd "${TEX_DIR}"
echo "Building Sant Dariya Sahib PDF..."

for pass in 1 2 3; do
  echo "LuaLaTeX pass ${pass}/3..."
  lualatex -shell-escape -interaction=nonstopmode -halt-on-error -file-line-error "${MAIN_FILE}"
done

echo "Done: ${TEX_DIR}/${PDF_FILE}"

