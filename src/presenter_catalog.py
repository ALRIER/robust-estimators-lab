"""Shared catalog for the defense Presenter Companion.

The companion must not become a second source of truth. Current modular note
files override the historical notes embedded in ``streamlit_app.py``. Legacy
entries are read from the source file so Simulation Lab and GA Search remain
available until they are migrated to dedicated note modules.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

from src.cover_presenter_notes import COVER_PRESENTER_NOTES
from src.research_presenter_notes import RESEARCH_PRESENTER_NOTES
from src.data_world_presenter_notes import DATA_WORLD_PRESENTER_NOTES
from src.monte_carlo_presenter_notes import MONTE_CARLO_PRESENTER_NOTES
from src.final_presenter_notes import FINAL_PRESENTER_NOTES
from src.thesis_ga_presenter_notes import THESIS_GA_PRESENTER_NOTES
from src.results_presenter_notes import RESULTS_PRESENTER_NOTES


ROOT = Path(__file__).resolve().parents[1]


PRESENTER_SEQUENCE = (
    (
        "01 · Research logic",
        (
            ("research_problem", "Why a problem?"),
            ("research_objective", "What are we asking?"),
            ("research_hypotheses", "What should happen?"),
            ("research_target", "What can the GA change?"),
            ("research_why_win", "When can a mixture win?"),
        ),
    ),
    (
        "02 · Data-generating world",
        (
            ("data_world_why_simulation", "Why simulation?"),
            ("data_world_regime", "Build a regime"),
            ("data_world_validity", "Trust the simulator"),
        ),
    ),
    ("03 · Simulation lab", (("simulation_lab", "Simulation lab"),)),
    (
        "04 · Monte Carlo engine",
        (
            ("monte_carlo_measurement", "Measure repeated risk"),
            ("monte_carlo_why_validate", "Why validate first?"),
            ("monte_carlo_validation_stages", "Validation stages"),
            ("monte_carlo_fairness", "Fairness & order of trust"),
        ),
    ),
    ("05 · GA search", (("ga_search", "GA search"),)),
    (
        "06 · Experiment pipeline",
        (
            ("pipeline_architecture", "Thesis GA Architecture"),
            ("pipeline_stage_0", "Initial discovery"),
            ("pipeline_stage_1", "Frozen confirmation I"),
            ("pipeline_stage_2", "Expanded rediscovery"),
            ("pipeline_stage_3", "Frozen validation II"),
            ("pipeline_stage_4", "External evidence + audit"),
        ),
    ),
    (
        "07 · Results journey",
        (
            ("results_stage_0", "Discovery + Frozen I"),
            ("results_stage_1", "Expanded rediscovery"),
            ("results_stage_2", "Strict validation"),
            ("results_stage_3", "Real-world battery"),
            ("results_stage_4", "Dirichlet audit"),
        ),
    ),
    (
        "08 · Conclusions",
        (
            ("conclusions_claims", "Claims H1–H4"),
            ("conclusions_contrib", "Contributions & Limits"),
        ),
    ),
    (
        "09 · Technical drill-down",
        (
            ("appendix_A", "GA mechanics"),
            ("appendix_B", "Metrics & gate"),
            ("appendix_C", "Technical results"),
            ("appendix_D", "Committee Q&A"),
        ),
    ),
)


def _legacy_presenter_notes() -> dict:
    """Read literal legacy note entries without importing the Streamlit app."""
    source = (ROOT / "streamlit_app.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(t, ast.Name) and t.id == "PRESENTER_NOTES" for t in node.targets):
            continue
        if not isinstance(node.value, ast.Dict):
            return {}

        notes = {}
        for key_node, value_node in zip(node.value.keys, node.value.values):
            try:
                key = ast.literal_eval(key_node)
                value = ast.literal_eval(value_node)
            except Exception:
                # One unusual historical entry should never break the whole
                # Presenter Companion. Modular notes can still override it.
                continue
            if isinstance(key, str):
                notes[key] = value
        return notes
    return {}


def all_presenter_notes() -> dict:
    """Return one merged note dictionary; modular notes are authoritative."""
    notes = _legacy_presenter_notes()
    notes.update(FINAL_PRESENTER_NOTES)
    notes.update(COVER_PRESENTER_NOTES)
    notes.update(RESEARCH_PRESENTER_NOTES)
    notes.update(DATA_WORLD_PRESENTER_NOTES)
    notes.update(MONTE_CARLO_PRESENTER_NOTES)
    notes.update(THESIS_GA_PRESENTER_NOTES)
    notes.update(RESULTS_PRESENTER_NOTES)
    return notes


def flat_sequence():
    """Return ordered (layer, key, label) rows for Previous/Next navigation."""
    return tuple(
        (layer, key, label)
        for layer, items in PRESENTER_SEQUENCE
        for key, label in items
    )


def speaking_cues(note) -> list[str]:
    """Extract the HELP/speaking content while omitting formula and Q&A blocks."""
    if not note:
        return ["No cue card is available for this view yet."]
    _title, _source, points, _transition = note

    if isinstance(points, (list, tuple)) and points and all(
        isinstance(item, (list, tuple)) and len(item) == 2 for item in points
    ):
        for label, copy in points:
            if str(label).upper() == "HELP":
                if isinstance(copy, (list, tuple)):
                    return [str(item).strip() for item in copy if str(item).strip()]
                text = str(copy).strip()
                return [
                    part.strip()
                    for part in re.split(r"(?<=[.!?])\s+", text)
                    if part.strip()
                ]

    if isinstance(points, (list, tuple)):
        return [str(item).strip() for item in points if str(item).strip()]
    return [str(points).strip()] if str(points).strip() else []
