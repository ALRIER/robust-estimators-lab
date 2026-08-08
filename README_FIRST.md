# Robust Estimators Lab — Codex starter

Este repositorio está preparado para que Codex empiece a construir el dashboard de la tesis sin tocar el experimento científico original.

## Objetivo
Construir en **7 días máximo** un dashboard local para video/defensa, con cuatro capas:

1. **Build the problem** — distribución, contaminación y comportamiento de estimadores.
2. **GA search** — mini-GA pedagógico + vista geológica 3D de un corte del simplex.
3. **Thesis results** — explorador de resultados reales precomputados.
4. **Validation pipeline** — discovery → held-out/fixed-weight validation → evidence taxonomy.

## Primera ejecución

### Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/build_processed_data.py
python app.py
```

### Linux/macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/build_processed_data.py
python app.py
```

Después abrir: `http://127.0.0.1:8050`

## Qué debe leer Codex primero
1. `AGENTS.md`
2. `CODEX_START_HERE.md`
3. `docs/MASTER_PLAN.md`
4. `docs/SCIENTIFIC_GUARDRAILS.md`
5. `docs/DATA_MANIFEST.md`
6. `docs/ACCEPTANCE_CRITERIA.md`
7. `prompts/01_LAYER1_BUILD_PROBLEM.md`

## Regla central
**Nunca mezclar DEMO MODE con THESIS RESULTS.** El mini-GA es pedagógico. Los resultados de tesis siempre se leen desde CSV precomputados y no se inventa trayectoria histórica que no exista en los archivos.
