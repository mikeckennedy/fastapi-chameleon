#!/usr/bin/env python3
"""Build the docs and mirror the static site into the committed repo-root docs/ folder.

Great Docs writes its site into an ephemeral ``great-docs/_site/`` directory (gitignored
and regenerated each build). This script runs the build, then mirrors that output into the
repo-root ``docs/`` folder that is committed and served by nginx. For this project the
package lives at the git root, so PKG_DIR == REPO_ROOT.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
PKG_DIR = _SCRIPTS.parent  # dir with pyproject.toml + great-docs.yml (also the git root here)
REPO_ROOT = PKG_DIR  # package is at the git root -> docs/ is committed beside pyproject.toml
SITE = PKG_DIR / "great-docs" / "_site"
DEST = REPO_ROOT / "docs"


def main() -> int:
    # Prefer the great-docs installed in the same venv as this interpreter.
    great_docs = Path(sys.executable).with_name("great-docs")
    cmd = [str(great_docs) if great_docs.exists() else "great-docs", "build"]
    if subprocess.run(cmd, cwd=PKG_DIR).returncode != 0:
        return 1
    if not SITE.is_dir():
        print(f"build output missing: {SITE}", file=sys.stderr)
        return 1
    if DEST.exists():
        shutil.rmtree(DEST)
    shutil.copytree(SITE, DEST)
    print(f"Mirrored -> {DEST} ({sum(1 for p in DEST.rglob('*') if p.is_file())} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
