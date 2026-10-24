#!/bin/bash
# Run only within this project directory; does not delete any user files.
set -euo pipefail
cd "$(dirname "$0")"
echo "4D-CT project: $(pwd)"
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 not found. Install Python 3 and try again." >&2
  exit 1
fi
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
python generate_datasets.py
python generate_project_docs.py
python validate_project.py
echo "Completed. Check simulation_results.json, manuscript.pdf, README.md and report.html."
