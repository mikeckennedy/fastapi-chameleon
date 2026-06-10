#!/usr/bin/env python3
"""Serve the committed docs/ under the production subpath for a faithful local preview.

This mirrors how nginx serves the site (``alias`` at ``/docs/fastapi-chameleon/``), so the
relative asset/nav paths resolve exactly as they will in production. Run
``scripts/build_docs.py`` first to populate ``docs/``.
"""

from __future__ import annotations

import functools
import http.server
import socketserver
from pathlib import Path

PREFIX = "/docs/fastapi-chameleon"
PORT = 8099
ROOT = Path(__file__).resolve().parent.parent / "docs"  # repo-root/docs (package is at git root)


class H(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        c = path.split("?", 1)[0].split("#", 1)[0]
        if c.startswith(PREFIX):
            path = c[len(PREFIX):] or "/"
        return super().translate_path(path)

    def send_head(self):
        if self.path in ("/", PREFIX):
            self.send_response(302)
            self.send_header("Location", PREFIX + "/")
            self.end_headers()
            return None
        return super().send_head()


class S(socketserver.TCPServer):
    allow_reuse_address = True


def main():
    if not ROOT.is_dir():
        raise SystemExit(f"Run build_docs.py first; {ROOT} missing")
    with S(("127.0.0.1", PORT), functools.partial(H, directory=str(ROOT))) as httpd:
        print(f"-> http://127.0.0.1:{PORT}{PREFIX}/  (Ctrl+C to stop)")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
