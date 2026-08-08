if (!(Test-Path .venv)) { python -m venv .venv }
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/build_processed_data.py
python app.py
