"""Compatibility entry point for Streamlit Cloud.

This is intentionally the deployment entrypoint.  Always reload the real
application module so Streamlit Cloud cannot keep serving a stale imported
copy after repository updates.
"""

import importlib
import streamlit_app

importlib.reload(streamlit_app)

# Deployment revision: Stage 5 external evidence + abstention audit unified.
# 2026-09-28
