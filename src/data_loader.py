from functools import lru_cache
from pathlib import Path
import pandas as pd

# Presentation-only hooks: these never rerun or alter thesis evidence.
from src.layer7_runtime import install_layer7_runtime_hooks
from src.layer7_stage_nav import install_layer7_stage_navigation
from src.layer7_force_visuals import install_layer7_force_visuals
from src.layer7_force_renderer import install_force_layer7_renderer
from src.layer7_readability import install_layer7_readability
from src.layer7_clean_renderer import install_layer7_clean_renderer
from src.layer89_pages import install_layer89_pages

install_layer7_runtime_hooks()
install_layer7_stage_navigation()
install_layer7_force_visuals()
install_force_layer7_renderer()
install_layer7_readability()
# Install this last for Layer 7. It unwraps stale Plotly closures left by hot reload.
install_layer7_clean_renderer()
# Layer 8/9 final defense pages are rendered after the sidebar and stop the legacy blocks.
install_layer89_pages()

ROOT = Path(__file__).resolve().parents[1]


def _read(rel):
    p = ROOT / rel
    return pd.read_csv(p) if p.exists() else pd.DataFrame()

@lru_cache(maxsize=8)
def load_winners():
    return _read("data/processed/winners_all.csv")

@lru_cache(maxsize=8)
def load_final_decisions():
    return _read("data/raw/validation/final_decision_table.csv")

@lru_cache(maxsize=8)
def load_bootstrap_ci():
    return _read("data/raw/validation/bootstrap_ci.csv")

@lru_cache(maxsize=8)
def load_evidence_taxonomy():
    return _read("data/raw/evidence/evidence_taxonomy_all_candidates.csv")

@lru_cache(maxsize=8)
def load_validated_specialists():
    return _read("data/raw/evidence/validated_specialists.csv")

@lru_cache(maxsize=8)
def load_dirichlet_summary():
    return _read("data/raw/dirichlet/abstain_audit_summary_by_regime.csv")

@lru_cache(maxsize=8)
def load_dirichlet_signals():
    return _read("data/raw/dirichlet/dirichlet_signal_regime_modes.csv")
