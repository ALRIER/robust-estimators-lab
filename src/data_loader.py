from functools import lru_cache
from pathlib import Path
import pandas as pd

# Single presentation bootstrap plus small compatibility hooks for the
# redesigned full-width cover, Layer 6 architecture, and parallel Presenter
# Companion. The companion runtime is installed before the main app calls
# st.set_page_config so ?presenter_companion=1 can render independently.
from src.presenter_companion_runtime import install_presenter_companion_runtime
from src.defense_runtime import install_defense_runtime
from src.cover_runtime import install_cover_runtime
from src.layer6_runtime import install_layer6_runtime
from src.presenter_launcher_runtime import install_presenter_launcher_runtime

install_presenter_companion_runtime()
install_defense_runtime()
install_cover_runtime()
install_layer6_runtime()
install_presenter_launcher_runtime()

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
