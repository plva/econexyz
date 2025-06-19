#!/bin/bash
# Render Mermaid workflow diagrams as SVG and list file URLs.

set -e

DOC_DIR="$(dirname "$0")/../docs/workflows"
DOC_DIR="$(realpath "$DOC_DIR")"
OUT_DIR="$DOC_DIR/rendered"

mkdir -p "$OUT_DIR"

if ! command -v npx >/dev/null 2>&1; then
  echo "npx is required to run mermaid-cli. Install Node.js." >&2
  exit 1
fi

for md in "$DOC_DIR"/*_workflow.md; do
  base=$(basename "$md" .md)
  out="$OUT_DIR/${base}.svg"
  npx -y @mermaid-js/mermaid-cli -i "$md" -o "$out" >/dev/null
  echo "file://$out"
done
