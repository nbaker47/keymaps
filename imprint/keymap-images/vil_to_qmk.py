#!/usr/bin/env python3
"""Convert a Vial .vil file into a QMK keymap.json that keymap-drawer can parse.

usage: vil_to_qmk.py <file.vil> <physical_layout.json> <LAYOUT_name> > keymap.json
Keys are placed using each key's matrix [row, col] from the keyboard's info.json.
"""
import json, re, sys

ALIASES = {"BSPACE": "BSPC", "SCOLON": "SCLN", "LBRACKET": "LBRC", "RBRACKET": "RBRC",
           "BSLASH": "BSLS", "QUOTE": "QUOT", "PGDOWN": "PGDN", "LCTRL": "LCTL", "RCTRL": "RCTL",
           "ESCAPE": "ESC", "DELETE": "DEL", "EQUAL": "EQL", "MINUS": "MINS", "GRAVE": "GRV"}

def fix(code):
    code = str(code)
    code = re.sub(r"^LT(\d+)\((.*)\)$", r"LT(\1,\2)", code)
    return re.sub(r"KC_([A-Z0-9_]+)", lambda m: "KC_" + ALIASES.get(m.group(1), m.group(1)), code)

vil = json.load(open(sys.argv[1]))
info = json.load(open(sys.argv[2]))
name = sys.argv[3]
order = [tuple(k["matrix"]) for k in info["layouts"][name]["layout"]]
layers = [[fix(layer[r][c]) for r, c in order] for layer in vil["layout"]]
print(json.dumps({"layout": name, "layers": layers}))
