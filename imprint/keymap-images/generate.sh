#!/usr/bin/env bash
# Regenerate per-layer images of the Cyboard Imprint keymap from ../../imprint_vial_latest.vil
# Needs: pip install keymap-drawer pyyaml; rsvg-convert (apt install librsvg2-bin)
set -euo pipefail
KEYMAP=${KEYMAP:-keymap}
cd "$(dirname "$0")"
LAYOUT=LAYOUT_fun   # imprint_function_row_2key_bottom_row (physical_layout.json is the Vial fork info.json with the function row moved up and the bottom-row and thumb keys moved down so nothing overlaps)
python3 vil_to_qmk.py ../../imprint_vial_latest.vil physical_layout.json $LAYOUT > keymap.json
$KEYMAP -c config.yaml parse -q keymap.json > keymap.yaml
for l in $(python3 -c 'import yaml;print(*yaml.safe_load(open("keymap.yaml"))["layers"])'); do
  $KEYMAP -c config.yaml draw keymap.yaml -j physical_layout.json -l $LAYOUT -s "$l" > "$l.svg"
  rsvg-convert -w 1400 -b white "$l.svg" -o "$l.png"
done
