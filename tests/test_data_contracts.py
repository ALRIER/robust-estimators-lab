from pathlib import Path
import pandas as pd
from src.constants import ESTIMATOR_NAMES

ROOT = Path(__file__).resolve().parents[1]


def test_required_raw_files_exist():
    required = [
        "data/raw/discovery/combined_final_regime_results_all_rows.csv",
        "data/raw/discovery/ga_winner_candidates_for_q1.csv",
        "data/raw/validation/final_decision_table.csv",
        "data/raw/validation/bootstrap_ci.csv",
        "data/raw/validation/seed_level_expanded_gate.csv",
        "data/raw/evidence/evidence_taxonomy_all_candidates.csv",
        "data/raw/evidence/validated_specialists.csv",
        "data/raw/dirichlet/abstain_audit_results.csv",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_processed_winners_have_26_weights():
    p = ROOT / "data/processed/winners_all.csv"
    if not p.exists():
        return
    df = pd.read_csv(p)
    expected = {f"w_{n}" for n in ESTIMATOR_NAMES}
    assert expected.issubset(df.columns)


def test_winner_weights_sum_to_one():
    p = ROOT / "data/processed/winners_all.csv"
    if not p.exists():
        return
    df = pd.read_csv(p)
    cols = [f"w_{n}" for n in ESTIMATOR_NAMES]
    sums = df[cols].fillna(0).sum(axis=1)
    assert ((sums - 1.0).abs() < 1e-5).all()
