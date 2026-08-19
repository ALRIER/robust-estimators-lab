from pathlib import Path

APP = Path("streamlit_app.py")
text = APP.read_text(encoding="utf-8")

# 1) Direct final-page imports. No runtime hooks.
anchor = "from src.constants import ESTIMATOR_NAMES\n"
imports = (
    "from src.results_page import render_results_journey\n"
    "from src.conclusions import render_conclusions\n"
    "from src.technical_appendix import render_technical_appendix\n"
    "from src.final_presenter_notes import FINAL_PRESENTER_NOTES\n"
)
if imports not in text:
    if anchor not in text:
        raise RuntimeError("Could not find import anchor")
    text = text.replace(anchor, anchor + imports, 1)

# 2) Merge only the current Layer 7-9 presenter notes into the existing note bank.
query_marker = "\n_query = st.query_params\n"
notes_update = "\nPRESENTER_NOTES.update(FINAL_PRESENTER_NOTES)\n"
if "PRESENTER_NOTES.update(FINAL_PRESENTER_NOTES)" not in text:
    if query_marker not in text:
        raise RuntimeError("Could not find presenter query marker")
    text = text.replace(query_marker, notes_update + query_marker, 1)

# 3) Replace the note resolver so the presenter link follows the exact current subview.
start = text.index("def _presenter_note_key(active_section: str) -> str:")
end = text.index("\n\ndef _presenter_notes_link", start)
resolver = '''def _presenter_note_key(active_section: str) -> str:
    """Resolve the exact speaking note for the currently visible defense view."""
    if active_section == "01 · Research logic":
        keys = ("research_problem", "research_objective", "research_hypotheses", "research_target", "research_why_win")
        return keys[int(st.session_state.get("research_panel", 0))]
    if active_section == "02 · Data-generating world":
        keys = ("data_world", "data_world_families", "data_world_certification")
        return keys[int(st.session_state.get("data_world_view", 0))]
    if active_section == "04 · Monte Carlo engine":
        if st.session_state.get("monte_carlo_view", "engine") == "validation":
            return f"monte_carlo_validation_{int(st.session_state.get('validation_stage', 0))}"
        return "monte_carlo_engine"
    if active_section == "06 · Experiment pipeline":
        if st.session_state.get("layer6_view", "architecture") == "architecture":
            return "pipeline_architecture"
        return f"pipeline_stage_{int(st.session_state.get('story_stage', 0))}"
    if active_section == "07 · Results journey":
        return f"results_stage_{max(0, min(int(st.session_state.get('results_stage', 0)), 4))}"
    if active_section == "08 · Conclusions":
        return "conclusions_contrib" if st.session_state.get("conclusion_view", "claims") == "contrib" else "conclusions_claims"
    if active_section == "09 · Technical drill-down":
        letter = "ABCDEF"[max(0, min(int(st.session_state.get("appendix_section", 0)), 5))]
        return f"appendix_{letter}"
    fixed = {
        "00 · Cover": "cover",
        "03 · Simulation lab": "simulation_lab",
        "05 · GA search": "ga_search",
    }
    return fixed[active_section]
'''
text = text[:start] + resolver + text[end:]

# 4) Remove all legacy top-level Layer 7 and Layer 9 page blocks.
def remove_active_blocks(source: str, label: str) -> str:
    target = f'if active_section == "{label}":'
    lines = source.splitlines(keepends=True)
    out = []
    i = 0
    removed = 0
    while i < len(lines):
        if lines[i].rstrip("\r\n") == target:
            removed += 1
            i += 1
            while i < len(lines):
                line = lines[i]
                if line and not line[0].isspace() and line.strip():
                    if (
                        line.startswith("if active_section == ")
                        or line.startswith("DEFENSE_SCENE_SECTION = ")
                        or line.startswith("if active_section in DEFENSE_SCENE_SECTION")
                    ):
                        break
                i += 1
            continue
        out.append(lines[i])
        i += 1
    if removed == 0:
        raise RuntimeError(f"No legacy block found for {label}")
    return "".join(out)

text = remove_active_blocks(text, "07 · Results journey")
text = remove_active_blocks(text, "09 · Technical drill-down")

# 5) Remove the old defense-scene mapping for Layer 8. It is the final legacy block.
legacy8 = "\nDEFENSE_SCENE_SECTION = {\n    \"08 · Conclusions\": 6,\n}\n"
pos = text.find(legacy8)
if pos == -1:
    raise RuntimeError("Could not find legacy Layer 8 defense-scene mapping")
text = text[:pos].rstrip() + "\n\n"

# 6) One direct renderer per final page. These are now the only active implementations.
text += '''if active_section == "07 · Results journey":
    render_results_journey()

if active_section == "08 · Conclusions":
    render_conclusions()

if active_section == "09 · Technical drill-down":
    render_technical_appendix()
'''

# Guardrails: stale blocks and old fallback labels must not survive.
assert text.count('if active_section == "07 · Results journey":') == 1
assert text.count('if active_section == "08 · Conclusions":') == 1
assert text.count('if active_section == "09 · Technical drill-down":') == 1
assert "DEFENSE_SCENE_SECTION" not in text
assert "THESIS RESULTS — precomputed research output" not in text
assert "Opportunity → fixed-weight confirmation" not in text

APP.write_text(text, encoding="utf-8")
print("streamlit_app.py consolidated successfully")
