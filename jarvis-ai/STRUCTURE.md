# Project Structure

This repository is now organized for clarity and ease of use. Core Python sources remain in place to avoid breaking imports, while config, scripts, tests, and web assets are grouped logically.

```
jarvis-ai/
├─ api_server.py            # Flask API entry
├─ jarvis_main.py           # Voice assistant entry
├─ jarvis_simple.py         # Lightweight CLI version
├─ modules/                 # Core modules (unchanged)
│  ├─ action_executor.py
│  ├─ ai_brain.py
│  ├─ browser_control.py
│  ├─ intent_parser.py
│  ├─ system_control.py
│  └─ voice_engine.py
├─ config/
│  ├─ .env.example          # Copy to .env and edit
│  ├─ requirements-api.txt
│  └─ requirements-python.txt
├─ scripts/
│  ├─ start-api-server.bat
│  ├─ start-jarvis-python.bat
│  ├─ setup-python-autostart.bat
│  └─ jarvis-python-silent.vbs
├─ tests/
│  ├─ test_api.py
│  ├─ test_chatbot.py
│  └─ test_jarvis.py
├─ web/
│  └─ react_integration.js
├─ Dockerfile               # Uses config/ requirements
├─ docker-compose.yml
└─ STRUCTURE.md             # This file
```

Notes:
- Root scripts with the same names are now deprecated. Use files under `scripts/`.
- Dockerfile now reads requirements from `config/`.
- Tests were updated to import from `modules/` regardless of location.

## Quick Start

Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r config\requirements-python.txt
pip install -r config\requirements-api.txt
```

Run the voice assistant:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-jarvis-python.bat
```

Run the API server:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-api-server.bat
```

Run tests:

```powershell
python .\tests\test_api.py
python .\tests\test_chatbot.py
python .\tests\test_jarvis.py
```

Docker build (from repo root):

```powershell
docker build -t jarvis-ai .
docker run -p 5000:5000 --env-file config\.env.example jarvis-ai
```

Optional Windows autostart:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup-python-autostart.bat
```
