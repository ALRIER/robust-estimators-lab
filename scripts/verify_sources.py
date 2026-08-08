from pathlib import Path
import hashlib, csv

ROOT = Path(__file__).resolve().parents[1]
manifest = ROOT / "research_reference/source_hashes.csv"
if not manifest.exists():
    raise SystemExit("source_hashes.csv missing")

bad = []
with manifest.open(newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        p = ROOT / row["path"]
        if not p.exists():
            bad.append((row["path"], "missing")); continue
        h = hashlib.sha256()
        with p.open("rb") as fh:
            for chunk in iter(lambda: fh.read(1024*1024), b""):
                h.update(chunk)
        if h.hexdigest() != row["sha256"]:
            bad.append((row["path"], "hash mismatch"))
if bad:
    print("Source verification FAILED:", bad)
    raise SystemExit(1)
print("Source verification OK")
