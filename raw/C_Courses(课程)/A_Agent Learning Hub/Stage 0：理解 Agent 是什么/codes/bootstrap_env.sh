#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_VENV_DIR="$SCRIPT_DIR/.venv"
VENV_DIR="${VENV_DIR:-$DEFAULT_VENV_DIR}"
REQ_FILE="$SCRIPT_DIR/requirements.txt"

python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/python" -m pip install --upgrade pip
"$VENV_DIR/bin/python" -m pip install -r "$REQ_FILE"

cat <<EOF
Environment ready.

Virtual env:
$VENV_DIR

Activate it with:
source "$VENV_DIR/bin/activate"

Then run, for example:
python "$SCRIPT_DIR/01_chatbot_deepseek.py"
EOF
