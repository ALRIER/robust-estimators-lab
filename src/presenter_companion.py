"""Parallel cue-card interface for the thesis defense.

This view is intentionally independent from the audience presentation state. It
uses the same note sources and the same layer/view names, but presents one large
cue card at a time with direct Previous/Next navigation.
"""

from __future__ import annotations

from base64 import b64encode
from pathlib import Path
import html
import re

import streamlit as st

from src.presenter_catalog import (
    PRESENTER_SEQUENCE,
    all_presenter_notes,
    flat_sequence,
    speaking_cues,
)
from src.presenter_sync import read_current_cue


ROOT = Path(__file__).resolve().parents[1]
_LOGO = "data:image/jpeg;base64," + b64encode(
    (ROOT / "assets" / "university_of_hull_logo.jpeg").read_bytes()
).decode("ascii")


def _set_index(index: int) -> None:
    total = len(flat_sequence())
    st.session_state.companion_index = max(0, min(int(index), total - 1))


def _index_for_key(sequence, cue_key: str | None) -> int | None:
    if not cue_key:
        return None
    for index, (_layer, key, _label) in enumerate(sequence):
        if key == cue_key:
            return index
    return None


def _jump_to_audience() -> None:
    sequence = flat_sequence()
    cue_key, revision, _updated_at = read_current_cue()
    index = _index_for_key(sequence, cue_key)
    if index is not None:
        st.session_state.companion_index = index
        st.session_state.companion_seen_revision = revision


def _cue_parts(raw: str, number: int) -> tuple[str, str]:
    """Keep explicit accessible anchors; derive a short anchor for legacy notes."""
    text = str(raw).strip()
    if "|" in text:
        anchor, copy = text.split("|", 1)
        return anchor.strip(), copy.strip()

    if ":" in text:
        prefix, rest = text.split(":", 1)
        if 1 <= len(prefix.strip()) <= 28:
            return prefix.strip().upper(), rest.strip()

    match = re.match(r"^(H[1-4]|RQ[1-4]|Step\s+\d+|Stage\s+\d+)\b[.\- ]*(.*)$", text, re.I)
    if match and match.group(2).strip():
        return match.group(1).upper(), match.group(2).strip()

    return f"CUE {number}", text


def _cue_html(title: str, cues: list[str], transition: str, layer: str, label: str, position: int, total: int) -> str:
    rows = []
    for number, item in enumerate(cues, start=1):
        anchor, copy = _cue_parts(item, number)
        emphasis = anchor in {
            "MAIN QUESTION", "KEY IDEA", "CONCLUSION", "FINAL GATE",
            "WIN CONDITION", "TAKE-HOME", "IMPORTANT", "MAIN IDEA",
            "SUMMARY", "5 STEPS", "6 STAGES", "ORDER",
        }
        if "•" in copy:
            bullet_parts = [part.strip() for part in copy.split("•") if part.strip()]
            copy_html = (
                '<ul class="copy-bullets">'
                + "".join(f"<li>{html.escape(part)}</li>" for part in bullet_parts)
                + "</ul>"
            )
        else:
            copy_html = html.escape(copy)

        rows.append(
            f'<div class="cue-row{" emphasis" if emphasis else ""}">'
            f'<div class="anchor">{html.escape(anchor)}</div>'
            f'<div class="copy">{copy_html}</div>'
            '</div>'
        )

    next_text = html.escape(transition or "")
    return f"""
    <style>
      .block-container{{max-width:1180px!important;padding:1.25rem 2.6rem 2.5rem!important}}
      [data-testid="stAppViewContainer"]{{background:radial-gradient(circle at 50% -10%,#17385e 0,#071525 38%,#040b13 85%)!important}}
      .companion{{font-family:Arial,sans-serif;color:#f7fbff}}
      .eyebrow{{font-size:.92rem;font-weight:900;letter-spacing:.15em;color:#89a9c4;margin-bottom:.5rem}}
      .title{{font-size:2.7rem;line-height:1.1;font-weight:900;color:#72cfff;margin-bottom:.45rem}}
      .meta{{display:flex;gap:1rem;flex-wrap:wrap;font-size:1.02rem;color:#b8cadb;margin-bottom:1.55rem}}
      .meta b{{color:#f3c743}}
      .cue-row{{display:grid;grid-template-columns:245px minmax(0,1fr);gap:30px;align-items:center;background:#0b2138;border:1px solid #32688f;border-left:7px solid #4ea9e8;border-radius:14px;padding:1.15rem 1.4rem;margin-bottom:1rem}}
      .cue-row.emphasis{{border-left-color:#f3c743;background:#102a43}}
      .anchor{{font-size:1.08rem;font-weight:900;line-height:1.25;letter-spacing:.075em;color:#f3c743;text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:6px}}
      .copy{{font-size:1.83rem;font-weight:750;line-height:1.33;color:#fff}}
      .copy-bullets{{margin:.05rem 0;padding-left:1.35rem}}
      .copy-bullets li{{margin:.42rem 0;line-height:1.34}}
      .copy-bullets li::marker{{color:#72cfff}}
      .transition{{margin-top:1.5rem;padding:1rem 1.2rem;border-top:1px solid #315570;color:#bcd0e2;font-size:1.12rem;line-height:1.4}}
      .transition b{{font-size:.86rem;letter-spacing:.12em;color:#72cfff;margin-right:.65rem}}
      @media(max-width:900px){{
        .block-container{{padding:1rem 1.1rem 2rem!important}}
        .title{{font-size:2.2rem}}
        .cue-row{{grid-template-columns:1fr;gap:.6rem}}
        .copy{{font-size:1.5rem}}
      }}
    </style>
    <div class="companion">
      <div class="eyebrow">PRESENTER COMPANION · {html.escape(layer)}</div>
      <div class="title">{html.escape(label)}</div>
      <div class="meta"><span><b>{position + 1} / {total}</b> cue cards</span><span>{html.escape(title)}</span></div>
      {''.join(rows)}
      <div class="transition"><b>NEXT IDEA</b>{next_text}</div>
    </div>
    """


def render_presenter_companion() -> None:
    sequence = flat_sequence()
    notes = all_presenter_notes()
    total = len(sequence)

    if "companion_follow" not in st.session_state:
        st.session_state.companion_follow = True
    if "companion_index" not in st.session_state:
        st.session_state.companion_index = 0

    # A HELP launcher can pass the exact cue key. Consume a newly arrived key.
    try:
        requested_card = str(st.query_params.get("card", "")).strip()
    except Exception:
        requested_card = ""

    if requested_card and st.session_state.get("companion_url_card") != requested_card:
        index = _index_for_key(sequence, requested_card)
        if index is not None:
            st.session_state.companion_index = index
            st.session_state.companion_url_card = requested_card

    # FOLLOW PRESENTATION is one-way. A new audience cue moves HELP to its
    # matching card. Manual HELP navigation is then free until the audience
    # presentation actually changes again.
    live_cue, live_revision, _updated_at = read_current_cue()
    previous_follow = bool(st.session_state.get("companion_follow_previous", False))
    follow_now = bool(st.session_state.companion_follow)
    force_align = follow_now and not previous_follow
    seen_revision = int(st.session_state.get("companion_seen_revision", -1))
    if follow_now and live_cue and (force_align or live_revision != seen_revision):
        live_index = _index_for_key(sequence, live_cue)
        if live_index is not None:
            st.session_state.companion_index = live_index
        st.session_state.companion_seen_revision = live_revision
    st.session_state.companion_follow_previous = follow_now

    current = max(0, min(int(st.session_state.companion_index), total - 1))
    st.session_state.companion_index = current
    live_index = _index_for_key(sequence, live_cue)
    live_label = sequence[live_index][2] if live_index is not None else "Waiting for audience presentation"

    with st.sidebar:
        st.markdown(
            f'<a href="./" target="_blank" title="Open audience presentation">'
            f'<img src="{_LOGO}" alt="University of Hull" style="width:100%;background:white;border-radius:7px;padding:5px;margin-bottom:.65rem"></a>',
            unsafe_allow_html=True,
        )
        st.markdown("## PRESENTER COMPANION")
        st.caption("Same defense order · one cue card at a time")

        st.toggle(
            "🔗 FOLLOW PRESENTATION",
            key="companion_follow",
            help="When ON, a change in the audience presentation moves HELP to the matching cue. HELP navigation never changes the audience screen.",
        )
        st.caption(f"Audience now: **{html.escape(live_label)}**")
        st.button(
            "↩ Current audience slide",
            key="companion_return_to_audience",
            use_container_width=True,
            on_click=_jump_to_audience,
            disabled=live_index is None,
        )
        if live_index is not None and current != live_index:
            st.caption("You are browsing HELP independently. The audience screen has not moved.")
        else:
            st.caption("HELP is aligned with the audience screen.")

        absolute = 0
        for layer, items in PRESENTER_SEQUENCE:
            with st.expander(layer, expanded=any(absolute + j == current for j in range(len(items)))):
                for key, label in items:
                    index = next(i for i, (_layer, k, _label) in enumerate(sequence) if k == key)
                    st.button(
                        label,
                        key=f"companion_nav_{key}",
                        type="primary" if index == current else "secondary",
                        use_container_width=True,
                        on_click=_set_index,
                        args=(index,),
                    )
                absolute += len(items)

    # Lightweight polling keeps a second browser window synchronized.
    # It performs a full rerun only when the audience cue revision changes.
    if hasattr(st, "fragment"):
        @st.fragment(run_every="1s")
        def _live_follow_tick():
            if not st.session_state.get("companion_follow", True):
                return
            cue_key, revision, _updated = read_current_cue()
            if not cue_key:
                return
            if int(revision) == int(st.session_state.get("companion_seen_revision", -1)):
                return
            target = _index_for_key(sequence, cue_key)
            if target is not None:
                st.session_state.companion_index = target
            st.session_state.companion_seen_revision = int(revision)
            st.rerun()

        _live_follow_tick()

    layer, key, label = sequence[current]
    note = notes.get(key)

    if note:
        title, _source, _points, transition = note
        cues = speaking_cues(note)
    else:
        title, transition = label, ""
        cues = ["This cue card has not been migrated yet."]

    top_prev, top_progress, top_next = st.columns([1, 1.7, 1])
    with top_prev:
        st.button(
            "← Previous",
            key="companion_prev_top",
            use_container_width=True,
            disabled=current == 0,
            on_click=_set_index,
            args=(current - 1,),
        )
    with top_progress:
        next_label = sequence[current + 1][2] if current < total - 1 else "End of defense"
        st.markdown(
            f"<div style='text-align:center;color:#9db7cc;padding:.55rem 0'>"
            f"<b style='color:#f3c743'>{current + 1} / {total}</b> &nbsp;·&nbsp; Next: {html.escape(next_label)}</div>",
            unsafe_allow_html=True,
        )
    with top_next:
        st.button(
            "Next →",
            key="companion_next_top",
            type="primary",
            use_container_width=True,
            disabled=current == total - 1,
            on_click=_set_index,
            args=(current + 1,),
        )

    st.markdown(_cue_html(title, cues, transition, layer, label, current, total), unsafe_allow_html=True)

    bottom_prev, bottom_next = st.columns(2)
    with bottom_prev:
        st.button(
            "← Previous cue",
            key="companion_prev_bottom",
            use_container_width=True,
            disabled=current == 0,
            on_click=_set_index,
            args=(current - 1,),
        )
    with bottom_next:
        st.button(
            "Next cue →",
            key="companion_next_bottom",
            type="primary",
            use_container_width=True,
            disabled=current == total - 1,
            on_click=_set_index,
            args=(current + 1,),
        )
