"""Compatibility entry point for Streamlit Cloud.

The deployed app must execute the same Streamlit dashboard whether Cloud is
configured with ``app.py`` or the explicit ``streamlit_app.py`` entry point.
"""

from streamlit_app import *  # noqa: F401,F403 - Streamlit renders module top level.
