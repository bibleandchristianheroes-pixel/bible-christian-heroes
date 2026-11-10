#!/usr/bin/env bash
# One-time setup in a fresh workspace.
set -e
cd "$(dirname "$0")"
python3 -c "import cairo" 2>/dev/null || pip install --break-system-packages -q pycairo
python3 -c "import numpy" 2>/dev/null || pip install --break-system-packages -q numpy
mkdir -p data out prev
[ -s data/CPDV.json ] || curl -sS -L -m 180 -o data/CPDV.json https://raw.githubusercontent.com/scrollmapper/bible_databases/master/formats/json/CPDV.json
fc-list | grep -qi lora || echo "WARNING: Lora font missing (captions fall back to another serif)"
fc-list | grep -qi poppins || echo "WARNING: Poppins font missing"
python3 -c "import sys; sys.path.insert(0,'.'); from engine import verse; print('CPDV ok:', verse('John',3,16)[:40])"
