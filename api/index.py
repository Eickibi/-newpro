"""Root Vercel entrypoint for the inventory app.

The actual application lives in something-main/propy-main.
This wrapper lets the repository deploy correctly even when Vercel's
Root Directory is the repository root.
"""
import os
import sys

APP_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "something-main", "propy-main")
)
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

import index as root_index

handler = root_index.handler
