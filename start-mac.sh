#!/bin/bash
# Human Touch - start script for Mac and Linux.  Run with:  bash start-mac.sh
cd "$(dirname "$0")" || exit 1

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python is not installed. Install it from https://www.python.org/downloads/ and run this again."
  exit 1
fi

if ! python3 -c "import anthropic" >/dev/null 2>&1; then
  echo "First run: installing the Anthropic library..."
  python3 -m pip install --quiet --user -r requirements.txt || { echo "Installing failed - check your internet connection."; exit 1; }
fi

if [ -z "$ANTHROPIC_API_KEY" ] && [ ! -f .env ]; then
  cp .env.example .env
  echo
  echo "A file called .env has been created in this folder."
  echo "Paste your Anthropic API key after ANTHROPIC_API_KEY= and save it."
  echo "(Without a key the app still works, but only the free quick check is available.)"
  (open -e .env 2>/dev/null || xdg-open .env 2>/dev/null) &
  read -r -p "Press Enter once you've saved the file... "
fi

echo "Starting Human Touch... Keep this window open while you use the app. Press Ctrl+C to stop it."
(sleep 3; open http://localhost:8765 2>/dev/null || xdg-open http://localhost:8765 2>/dev/null) &
python3 server.py
