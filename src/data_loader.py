from functools import lru_cache
from pathlib import Path
import pandas as pd

# Layer 7 is presentation-only: install its visual/help hooks as soon as this
# already-imported dashboard module loads. The hooks never recompute evidence.
from src.layer7_runtime import install_layer7_runtime_hooks

install_layer7_runtime_hooks()

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
