"""
Creates Human_Touch_share.zip - a copy of the app that is safe to give to someone else.

  python make_share_zip.py

Leaves out your API key (.env), editor settings, caches, test results and old zips.
"""

import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "Human_Touch_share.zip"
SKIP_NAMES = {".env", "results.json", OUT.name}
SKIP_DIRS = {".claude", "__pycache__", ".git", ".venv"}

count = 0
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for p in sorted(HERE.rglob("*")):
        rel = p.relative_to(HERE)
        secret = p.name.lower().startswith(".env") and p.name != ".env.example"  # .env, .env.local, .env.backup...
        if p.is_dir() or secret or p.name in SKIP_NAMES or p.suffix == ".zip" or SKIP_DIRS & set(rel.parts):
            continue
        z.write(p, Path("Human_Touch") / rel)
        count += 1

with zipfile.ZipFile(OUT) as z:
    names = set(z.namelist())
    assert not any(n.endswith("/.env") for n in names), "API key file slipped in!"
    required = ["server.py", "index.html", "requirements.txt", ".env.example", "GETTING_STARTED.md", "LICENSE",
                "Start Human Touch.bat", "start-mac.sh"]
    missing = [f for f in required if f"Human_Touch/{f}" not in names]
    assert not missing, f"Missing from the zip: {missing}"
print(f"Created {OUT.name} with {count} files (no API key inside).")
