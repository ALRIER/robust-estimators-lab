# Robust Estimators Lab — portable launch

## Local source mode
- Linux/macOS: `./run_linux_mac.sh` then open http://127.0.0.1:8050
- Windows: run `run_windows.ps1` then open http://127.0.0.1:8050

## Container / hosted mode
With Docker available, run `docker compose up --build` and open http://127.0.0.1:8050. For a server, expose port 8050 behind a reverse proxy and use its HTTPS URL.

The app is offline at runtime: it has no external APIs, fonts, telemetry, or network data calls. A first native dependency install or Docker build requires packages to be available locally; to make a target machine fully air-gapped, build/load the container image for that target platform in advance.
