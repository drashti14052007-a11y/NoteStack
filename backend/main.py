import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import json

from optimizer import load_models, run_optimizer, CATEGORY_CONFIG
from compliance import check_compliance
from pdf_report import generate_pdf

# ── App setup ──────────────────────────────────────────────
app = FastAPI(
    title="NoteStack API",
    description="Reverse Sensory Formulation Engine for Indian Food Products",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Database setup ──────────────────────────────────────────
BASE_DIR = os.path.dirname(__file__)
DB_PATH  = os.path.join(BASE_DIR, "history.db")
engine   = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
Base     = declarative_base()
Session  = sessionmaker(bind=engine)

class FormulationHistory(Base):
    __tablename__ = "history"
    id              = Column(Integer, primary_key=True, index=True)
    category        = Column(String)
    target_scores   = Column(Text)
    formulation     = Column(Text)
    predicted_scores= Column(Text)
    confidence_pct  = Column(Float)
    compliance_status = Column(String)
    created_at      = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# ── Load ML models on startup ───────────────────────────────
@app.on_event("startup")
def startup_event():
    load_models()
    print("✅ NoteStack models loaded")

# ── Request / Response schemas ──────────────────────────────
class FormulateRequest(BaseModel):
    category: str
    target_scores: list[float]

class FormulateResponse(BaseModel):
    category: str
    formulation: dict
    predicted_scores: dict
    target_scores: dict
    confidence_pct: float
    residual_error: float
    compliance: dict

# ── Routes ──────────────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "NoteStack API is running", "version": "1.0.0"}

@app.get("/categories")
def get_categories():
    result = {}
    for cat, config in CATEGORY_CONFIG.items():
        result[cat] = {
            "features": config["features"],
            "targets":  config["targets"],
            "bounds":   config["bounds"],
        }
    return result

@app.post("/formulate", response_model=FormulateResponse)
def formulate(request: FormulateRequest):
    category = request.category.lower()

    if category not in CATEGORY_CONFIG:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown category '{category}'. Choose from: {list(CATEGORY_CONFIG.keys())}"
        )

    config = CATEGORY_CONFIG[category]
    if len(request.target_scores) != len(config["targets"]):
        raise HTTPException(
            status_code=400,
            detail=f"Expected {len(config['targets'])} target scores for {category}, got {len(request.target_scores)}"
        )

    result     = run_optimizer(category, request.target_scores)
    compliance = check_compliance(category, result["formulation"])

    db = Session()
    try:
        record = FormulationHistory(
            category          = category,
            target_scores     = json.dumps(request.target_scores),
            formulation       = json.dumps(result["formulation"]),
            predicted_scores  = json.dumps(result["predicted_scores"]),
            confidence_pct    = result["confidence_pct"],
            compliance_status = compliance["status"],
        )
        db.add(record)
        db.commit()
    finally:
        db.close()

    return FormulateResponse(
        category         = category,
        formulation      = result["formulation"],
        predicted_scores = result["predicted_scores"],
        target_scores    = result["target_scores"],
        confidence_pct   = result["confidence_pct"],
        residual_error   = result["residual_error"],
        compliance       = compliance,
    )

@app.get("/history")
def get_history(limit: int = 10):
    db = Session()
    try:
        records = db.query(FormulationHistory)\
                    .order_by(FormulationHistory.created_at.desc())\
                    .limit(limit).all()
        return [
            {
                "id":               r.id,
                "category":         r.category,
                "confidence_pct":   r.confidence_pct,
                "compliance_status":r.compliance_status,
                "created_at":       r.created_at.isoformat(),
            }
            for r in records
        ]
    finally:
        db.close()

@app.post("/report")
def download_report(request: FormulateRequest):
    from fastapi.responses import Response

    category = request.category.lower()
    if category not in CATEGORY_CONFIG:
        raise HTTPException(status_code=400, detail=f"Unknown category '{category}'")

    result     = run_optimizer(category, request.target_scores)
    compliance = check_compliance(category, result["formulation"])
    pdf_bytes  = generate_pdf(
        category         = category,
        formulation      = result["formulation"],
        predicted_scores = result["predicted_scores"],
        target_scores    = result["target_scores"],
        confidence_pct   = result["confidence_pct"],
        residual_error   = result["residual_error"],
        compliance       = compliance,
    )

    return Response(
        content      = pdf_bytes,
        media_type   = "application/pdf",
        headers      = {"Content-Disposition": f"attachment; filename=notestack_{category}_report.pdf"}
    )