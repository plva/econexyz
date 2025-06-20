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

# Clean up old SVGs before rendering
rm -f "$OUT_DIR"/*.svg

for md in "$DOC_DIR"/*_workflow.md; do
  base=$(basename "$md" .md)
  out="$OUT_DIR/${base}.svg"
  npx -y @mermaid-js/mermaid-cli -i "$md" -o "$out" >/dev/null
done

# List all SVGs in the output directory
for svg in "$OUT_DIR"/*.svg; do
  echo "file://$svg"
done

echo "Rendered SVGs directory: file://$OUT_DIR"
