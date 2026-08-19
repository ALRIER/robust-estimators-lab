"""Safe runtime loader for Layer 8/9 while the source module is being consolidated.

It reads the presentation module as text, escapes the one literal-brace q95 formula
inside an f-string, compiles it, and exposes the Layer 8/9 render functions. No thesis
data or results are modified.
"""

from __future__ import annotations

from pathlib import Path

_SOURCE = Path(__file__).with_name("layer89_pages.py")
_text = _SOURCE.read_text(encoding="utf-8")
_text = _text.replace(
    "q<sub>.95</sub>({(θ̂−θ)²})",
    "q<sub>.95</sub>({{(θ̂−θ)²}})",
)

_namespace = {
    "__name__": "src.layer89_pages_runtime_impl",
    "__file__": str(_SOURCE),
    "__package__": "src",
}
exec(compile(_text, str(_SOURCE), "exec"), _namespace)

install_layer89_pages = _namespace["install_layer89_pages"]
render_layer8 = _namespace["_render_layer8"]
render_layer9 = _namespace["_render_layer9"]
presenter_notes = _namespace["_presenter_notes"]
