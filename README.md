# AgroGuard AI

**AI-Powered Crop Disease Detection & Smart Farming Assistant**

AgroGuard AI is a software-only Flask web application for crop scouting, educational disease detection, soil notes, fertilizer guidance, weather planning, and printable reports. It runs in Demo AI and Demo Weather modes without sensors, hardware, trained model files, or external API keys.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white) ![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)

## Features

- Secure registration, login, password hashing, sessions, and protected workspace routes
- Responsive agricultural SaaS dashboard with live SQLite statistics
- Demo crop disease predictor with modular AI integration boundary
- Image validation, preview, safe filenames, 8 MB upload limit, and persisted analysis history
- Structured farm assistant API with informational recommendations
- Demo weather service ready for an external provider later
- Soil analysis and fertilizer recommendation services with stored records
- Chart.js analytics, searchable history, delete actions, and print-ready reports
- Light/dark theme persistence and English/Marathi/Hindi translation dictionary foundation

## Screenshots

Run the app locally and capture dashboard, disease detection, and reports views for this section.

## Technology

HTML5, CSS3, vanilla JavaScript, Bootstrap Icons CDN, Chart.js CDN, Python 3, Flask, Flask-SQLAlchemy, SQLite, and Werkzeug password hashing.

## Architecture

Browser templates call REST endpoints through small vanilla JavaScript modules. Flask blueprints own authentication, dashboard pages, disease analysis, assistant, weather, and reports. SQLAlchemy models persist users, crop analyses, soil analyses, recommendations, and assistant conversations. `services/disease_predictor.py` delegates to `ai/predictor.py`, where a TensorFlow or PyTorch implementation can later replace the demo profile predictor without changing the route contract.

## Installation on Windows

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000/). If PowerShell blocks activation, use `Set-ExecutionPolicy -Scope Process Bypass` for the current terminal, or run the venv interpreter directly:

```powershell
.\venv\Scripts\python.exe app.py
```

The SQLite database is created automatically at `database/agroguard.db`. Copy `.env.example` to `.env` and set a strong `SECRET_KEY` for non-demo use. `WEATHER_API_KEY` is optional; the current service intentionally falls back to Demo Weather Mode.

## Demo credentials

Create an account from the registration screen. No credential is hard-coded. Demo predictions are available immediately after registration.

## API documentation

- `POST /api/register`, `POST /api/login`, `POST /api/logout`
- `POST /api/disease/analyze`, `GET /api/disease/history`, `DELETE /api/disease/<id>`
- `POST /api/soil/analyze`, `POST /api/fertilizer/recommend`
- `POST /api/assistant`, `GET /api/weather`
- `GET /api/analytics`, `GET /api/reports/`

JSON requests should include the fields shown by the matching form. Disease analysis uses multipart form data with `crop` and `image`.

## Testing

```powershell
.\venv\Scripts\python.exe -m pytest -q
```

## Project structure

```text
app.py config.py requirements.txt
models/ routes/ services/ ai/
templates/ static/ database/ uploads/ tests/
```

## Future improvements

Replace the demo predictor with a versioned TensorFlow/PyTorch model, connect a weather provider, add CSRF protection and rate limiting for production deployment, and add role-based agronomist review workflows.

## Author

AgroGuard AI project workspace.
