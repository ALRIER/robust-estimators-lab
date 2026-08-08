from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_WINNERS = ROOT / "data/raw/discovery/winner_summaries"
OUT = ROOT / "data/processed"
OUT.mkdir(parents=True, exist_ok=True)

files = sorted(RAW_WINNERS.rglob("*.csv"))
frames = []
for p in files:
    df = pd.read_csv(p)
    # Infer source seed/family from directory names for easier dashboard filtering.
    seed_dir = next((part for part in p.parts if part.startswith("seed")), None)
    df.insert(0, "source_seed_label", seed_dir or "unknown")
    frames.append(df)

winners = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
winners.to_csv(OUT / "winners_all.csv", index=False)

cases = pd.DataFrame()
if not winners.empty:
    selectors = [
        ("exwald", "REG03", "GA discovery-pass teaching example"),
        ("exgaussian", "REG01", "Benchmark-retained teaching example"),
    ]
    rows = []
    for fam, reg, note in selectors:
        sub = winners[(winners["distribution"] == fam) & (winners["specialist_regime_id"] == reg)]
        if not sub.empty:
            row = sub.iloc[0].copy()
            row["dashboard_teaching_note"] = note
            rows.append(row)
    if rows:
        cases = pd.DataFrame(rows)
cases.to_csv(OUT / "dashboard_cases.csv", index=False)

health = {
    "winner_source_files": len(files),
    "winner_rows": int(len(winners)),
    "families": sorted(winners["distribution"].dropna().unique().tolist()) if not winners.empty else [],
    "teaching_cases": int(len(cases)),
}
(OUT / "data_health.json").write_text(json.dumps(health, indent=2), encoding="utf-8")
print(json.dumps(health, indent=2))
