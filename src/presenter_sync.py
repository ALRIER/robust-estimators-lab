"""One-way live synchronization between the audience deck and Presenter Companion.

The audience presentation publishes only the currently visible cue key. The
Presenter Companion may follow that key automatically, but it never writes back
to the audience presentation. A shared cache resource keeps the state available
across Streamlit sessions served by the same app process.
"""

from __future__ import annotations

import threading
import time

import streamlit as st


@st.cache_resource(show_spinner=False)
def _sync_bus():
    return {
        "lock": threading.Lock(),
        "cue_key": None,
        "revision": 0,
        "updated_at": 0.0,
    }


def cue_for_presentation(active_section: str) -> str | None:
    """Resolve the canonical Presenter Companion cue for the visible audience view."""
    if active_section == "00 · Cover":
        return None

    if active_section == "01 · Research logic":
        keys = (
            "research_problem",
            "research_objective",
            "research_hypotheses",
            "research_target",
            "research_why_win",
        )
        index = max(0, min(int(st.session_state.get("research_panel", 0)), len(keys) - 1))
        return keys[index]

    if active_section == "02 · Data-generating world":
        keys = (
            "data_world_why_simulation",
            "data_world_regime",
            "data_world_validity",
        )
        index = max(0, min(int(st.session_state.get("data_world_view", 0)), len(keys) - 1))
        return keys[index]

    if active_section == "03 · Simulation lab":
        return "simulation_lab"

    if active_section == "04 · Monte Carlo engine":
        keys = (
            "monte_carlo_measurement",
            "monte_carlo_why_validate",
            "monte_carlo_validation_stages",
            "monte_carlo_fairness",
        )
        index = max(0, min(int(st.session_state.get("monte_carlo_didactic_view", 0)), len(keys) - 1))
        return keys[index]

    if active_section == "05 · GA search":
        return "ga_search"

    if active_section == "06 · Experiment pipeline":
        if st.session_state.get("layer6_view", "architecture") == "architecture":
            return "pipeline_architecture"
        stage = max(0, min(int(st.session_state.get("story_stage", 0)), 4))
        return f"pipeline_stage_{stage}"

    if active_section == "07 · Results journey":
        stage = max(0, min(int(st.session_state.get("results_stage", 0)), 2))
        return ("results_stage_2", "results_stage_3", "results_stage_4")[stage]

    if active_section == "08 · Conclusions":
        return (
            "conclusions_contrib"
            if st.session_state.get("conclusion_view", "claims") == "contrib"
            else "conclusions_claims"
        )

    if active_section == "09 · Technical drill-down":
        section = max(0, min(int(st.session_state.get("appendix_section", 0)), 5))
        return f"appendix_{'ABCDEF'[section]}"

    return None


def publish_current_cue(active_section: str) -> str | None:
    """Publish the current audience cue, incrementing revision only on real changes."""
    cue_key = cue_for_presentation(active_section)
    if not cue_key:
        return None

    bus = _sync_bus()
    lock = bus["lock"]
    with lock:
        if bus["cue_key"] != cue_key:
            bus["cue_key"] = cue_key
            bus["revision"] = int(bus["revision"]) + 1
            bus["updated_at"] = time.time()
    return cue_key


def read_current_cue() -> tuple[str | None, int, float]:
    """Return cue key, revision and update timestamp for the current audience view."""
    bus = _sync_bus()
    lock = bus["lock"]
    with lock:
        return (
            bus["cue_key"],
            int(bus["revision"]),
            float(bus["updated_at"]),
        )
