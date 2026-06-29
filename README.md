# NoteStack — Reverse Sensory Formulation Engine

NoteStack predicts the ingredient ratios most likely to produce a target sensory profile, across four Indian food categories: **Dairy · Chocolate & Confectionery · Spices & Condiments · Savory Snacks**.

Instead of running costly trial batches to hit a flavor or texture target, a food technologist inputs what they *want* (sweetness 7, bitterness 3, body 8...) and NoteStack returns the formulation most likely to produce it — along with a confidence score, an FSSAI compliance check, and a downloadable PDF report.

---

## Why

Reverse sensory formulation is used in R&D at companies like Nestlé, Amul, ITC, and Britannia, but the tools are proprietary. Globally, Gastrograph AI does this for craft beverages. NoteStack is a multi-category, India-focused equivalent — with FSSAI regulatory grounding built directly into the compliance checks.

## Categories at a glance

| Category | Sensory attributes | Key FSSAI references |
|---|---|---|
| 🥛 Dairy | Sweetness · Sourness · Body · Aroma · Texture | IS 1479, FSSAI A19 (yoghurt fat & acidity) |
| 🍫 Chocolate & Confectionery | Bitterness · Sweetness · Melt · Aroma · Snap | FSS Schedule I (cocoa solids minimums) |
| 🌶️ Spices & Condiments | Pungency · Earthiness · Saltiness · Aroma intensity · Heat | FSS MRL & aflatoxin limits |
| 🍝 Savory Snacks | Crunchiness · Saltiness · Oiliness · Spice intensity · Aftertaste | FSS trans fat & salt guidelines |

Each category has its own ingredient set, sensory attributes, dataset, and model — loaded dynamically based on what the user selects.

## How it works

```
Frontend (sliders for target sensory profile)
        │  POST /formulate
        ▼
FastAPI backend
   ├─ Dynamic model loader (per category)
   ├─ Inverse optimizer → solves for ingredient ratios
   ├─ Confidence scorer
   ├─ FSSAI compliance checker
   └─ PDF report generator (FPDF2)
        │
        ▼
ML model layer (per-category regression models)
        │
        ▼
Data layer (per-category sensory datasets)
```

## Features

**Backend**
- Per-category formulation prediction via `/formulate`
- Confidence scoring (how achievable the target profile is)
- FSSAI compliance checks with specific standard citations per category
- PDF formulation report, generated on demand via `/report`
- Formulation history store
- Auto-generated API docs via FastAPI's Swagger UI at `/docs`

**Frontend**
- Welcome → category select → sensory sliders → results, as a single-page flow
- Radar chart comparing target vs. predicted sensory profile
- Ingredient ratio breakdown with score cards per attribute
- FSSAI compliance badge with passed/warning/flagged items
- One-click PDF report download, with an in-app download confirmation
- Mobile responsive
- Parchment/ink visual theme, consistent across all screens

## Tech stack

```
Backend             FastAPI (Python)
Modeling            Per-category regression + inverse optimization
Report generation   FPDF2
Database            SQLite
Frontend            Vanilla HTML5, CSS3, JavaScript (ES6)
Visualization        Chart.js (radar chart)
```

## Getting started

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The API will be live at `http://127.0.0.1:8000`, with interactive docs at `http://127.0.0.1:8000/docs`.

### Frontend

The frontend is plain HTML/CSS/JS — no build step required.

```bash
cd frontend
# open index.html directly in a browser, or serve it locally, e.g.:
python -m http.server 5500
```

Then visit `http://127.0.0.1:5500` (make sure the backend is running first — the frontend expects it at `http://127.0.0.1:8000`).

## Project structure

```
NoteStack/
├── backend/
│   ├── main.py            # FastAPI app + endpoints
│   ├── optimizer.py       # Inverse formulation engine
│   ├── compliance.py      # FSSAI compliance checker
│   ├── pdf_report.py      # PDF report generator
│   └── ...
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
└── README.md
```

## Status

This project is under active development. Core prediction, compliance checking, results UI, and PDF reporting are complete and working end-to-end locally. Deployment, automated testing, and final documentation polish are in progress.

## Built by

Drashti Patel — B.Tech, Food Processing Technology, ADIT, CVMU
