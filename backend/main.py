import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone
import json
import numpy as np

from optimizer import load_models, run_optimizer, CATEGORY_CONFIG
from compliance import check_compliance
from pdf_report import generate_pdf
from subcategories import SUBCATEGORIES, get_subcategories_for_category, get_subcategory

# ── App setup ──────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app):
    load_models()
    print("[OK] NoteStack models loaded")
    yield

app = FastAPI(
    title="NoteStack API",
    description="Reverse Sensory Formulation Engine for Indian Food Products",
    version="2.0.0",
    lifespan=lifespan,
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
    subcategory     = Column(String, nullable=True)
    target_scores   = Column(Text)
    formulation     = Column(Text)
    predicted_scores= Column(Text)
    confidence_pct  = Column(Float)
    compliance_status = Column(String)
    created_at      = Column(DateTime, default=lambda: datetime.now(timezone.utc))

Base.metadata.create_all(bind=engine)


# ── Request / Response schemas ──────────────────────────────
class FormulateRequest(BaseModel):
    category: str
    subcategory: Optional[str] = None
    target_scores: list[float]

class FormulateResponse(BaseModel):
    category: str
    subcategory: Optional[str] = None
    formulation: dict
    predicted_scores: dict
    target_scores: dict
    confidence_pct: float
    residual_error: float
    compliance: dict


def transform_subcategory_scores(subcategory_key: str, user_scores: list[float], parent_category: str) -> list[float]:
    """
    Transform 6 user-facing subcategory scores into 5 model target scores
    using the weight mappings defined in subcategories.py.
    """
    subcat = get_subcategory(subcategory_key)
    if not subcat:
        raise ValueError(f"Unknown subcategory: {subcategory_key}")

    config = CATEGORY_CONFIG[parent_category]
    model_targets = config["targets"]

    # Initialize accumulator for each model target
    target_accum = {t: 0.0 for t in model_targets}
    target_weight_sum = {t: 0.0 for t in model_targets}

    for attr, score in zip(subcat["attributes"], user_scores):
        mapping = attr["mapping"]
        for model_target, weight in mapping.items():
            target_accum[model_target] += score * weight
            target_weight_sum[model_target] += weight

    # Normalize: divide by total weight contributed to each target
    model_scores = []
    for t in model_targets:
        if target_weight_sum[t] > 0:
            model_scores.append(target_accum[t] / target_weight_sum[t])
        else:
            model_scores.append(5.0)  # Default neutral value

    return model_scores


# ── Routes ──────────────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "NoteStack API is running", "version": "2.0.0"}

@app.get("/categories")
def get_categories():
    result = {}
    for cat, config in CATEGORY_CONFIG.items():
        # Get subcategories for this parent
        subcats = get_subcategories_for_category(cat)
        subcat_list = []
        for key, val in subcats.items():
            subcat_list.append({
                "key": key,
                "name": val["name"],
                "icon": val["icon"],
                "description": val["description"],
                "attributes": val["attributes"],
            })

        result[cat] = {
            "features": config["features"],
            "targets":  config["targets"],
            "bounds":   config["bounds"],
            "subcategories": subcat_list,
        }
    return result

@app.get("/subcategories/{category}")
def get_subcategories_endpoint(category: str):
    """Return all subcategories for a given parent category."""
    category = category.lower()
    if category not in CATEGORY_CONFIG:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown category '{category}'. Choose from: {list(CATEGORY_CONFIG.keys())}"
        )
    subcats = get_subcategories_for_category(category)
    result = []
    for key, val in subcats.items():
        result.append({
            "key": key,
            "name": val["name"],
            "icon": val["icon"],
            "description": val["description"],
            "attributes": val["attributes"],
        })
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

    # If subcategory is provided, transform 6 user-facing scores → 5 model targets
    if request.subcategory:
        subcat = get_subcategory(request.subcategory)
        if not subcat:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown subcategory '{request.subcategory}'"
            )
        if subcat["parent_category"] != category:
            raise HTTPException(
                status_code=400,
                detail=f"Subcategory '{request.subcategory}' does not belong to category '{category}'"
            )
        if len(request.target_scores) != len(subcat["attributes"]):
            raise HTTPException(
                status_code=400,
                detail=f"Expected {len(subcat['attributes'])} target scores for subcategory '{request.subcategory}', got {len(request.target_scores)}"
            )

        # Transform user scores to model targets
        model_scores = transform_subcategory_scores(request.subcategory, request.target_scores, category)

        # Store original user-facing attribute names and scores for response
        user_target_names = [attr["key"] for attr in subcat["attributes"]]
        user_target_scores = request.target_scores
    else:
        # Legacy: direct model target scores
        if len(request.target_scores) != len(config["targets"]):
            raise HTTPException(
                status_code=400,
                detail=f"Expected {len(config['targets'])} target scores for {category}, got {len(request.target_scores)}"
            )
        model_scores = request.target_scores
        user_target_names = config["targets"]
        user_target_scores = request.target_scores

    result     = run_optimizer(category, model_scores)
    compliance = check_compliance(category, result["formulation"])

    # Build user-facing target and predicted scores
    if request.subcategory:
        subcat = get_subcategory(request.subcategory)
        # Map model predicted scores back to user-facing attributes
        model_pred = result["predicted_scores"]  # dict of model_target: value

        user_predicted = {}
        user_targets = {}
        for attr, user_score in zip(subcat["attributes"], user_target_scores):
            attr_key = attr["key"]
            mapping = attr["mapping"]
            # Compute predicted value for this user-facing attribute from model predictions
            pred_val = sum(model_pred[mt] * w for mt, w in mapping.items())
            weight_sum = sum(mapping.values())
            if weight_sum > 0:
                pred_val /= weight_sum
            user_predicted[attr_key] = round(pred_val, 2)
            user_targets[attr_key] = round(user_score, 2)

        response_predicted = user_predicted
        response_targets = user_targets
    else:
        response_predicted = result["predicted_scores"]
        response_targets = result["target_scores"]

    # Save to history
    db = Session()
    try:
        record = FormulationHistory(
            category          = category,
            subcategory       = request.subcategory,
            target_scores     = json.dumps(request.target_scores),
            formulation       = json.dumps(result["formulation"]),
            predicted_scores  = json.dumps(response_predicted),
            confidence_pct    = result["confidence_pct"],
            compliance_status = compliance["status"],
        )
        db.add(record)
        db.commit()
    finally:
        db.close()

    return FormulateResponse(
        category         = category,
        subcategory      = request.subcategory,
        formulation      = result["formulation"],
        predicted_scores = response_predicted,
        target_scores    = response_targets,
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
                "subcategory":      r.subcategory,
                "confidence_pct":   r.confidence_pct,
                "compliance_status":r.compliance_status,
                "created_at":       r.created_at.isoformat(),
            }
            for r in records
        ]
    finally:
        db.close()

class ReportFromResultRequest(BaseModel):
    category: str
    subcategory: Optional[str] = None
    formulation: dict
    predicted_scores: dict
    target_scores: dict
    confidence_pct: float
    residual_error: float
    compliance: dict

@app.post("/report-from-result")
def download_report_from_result(request: ReportFromResultRequest):
    """Generate PDF from pre-computed formulation data — skips optimizer."""
    from fastapi.responses import Response

    # Get attribute descriptions if subcategory is provided
    attribute_descriptions = {}
    if request.subcategory:
        subcat = get_subcategory(request.subcategory)
        if subcat:
            for attr in subcat["attributes"]:
                attribute_descriptions[attr["key"]] = attr["description"]

    pdf_bytes = generate_pdf(
        category         = request.category,
        formulation      = request.formulation,
        predicted_scores = request.predicted_scores,
        target_scores    = request.target_scores,
        confidence_pct   = request.confidence_pct,
        residual_error   = request.residual_error,
        compliance       = request.compliance,
        subcategory      = request.subcategory,
        attribute_descriptions = attribute_descriptions,
    )

    sub_label = f"_{request.subcategory}" if request.subcategory else ""
    return Response(
        content      = pdf_bytes,
        media_type   = "application/pdf",
        headers      = {"Content-Disposition": f"attachment; filename=notestack_{request.category}{sub_label}_report.pdf"}
    )

@app.post("/report")
def download_report(request: FormulateRequest):
    """Fallback: re-runs optimizer to generate PDF (slower)."""
    from fastapi.responses import Response

    category = request.category.lower()
    if category not in CATEGORY_CONFIG:
        raise HTTPException(status_code=400, detail=f"Unknown category '{category}'")

    # Handle subcategory transformation
    if request.subcategory:
        model_scores = transform_subcategory_scores(request.subcategory, request.target_scores, category)
    else:
        model_scores = request.target_scores

    result     = run_optimizer(category, model_scores)
    compliance = check_compliance(category, result["formulation"])

    attribute_descriptions = {}
    if request.subcategory:
        subcat = get_subcategory(request.subcategory)
        if subcat:
            for attr in subcat["attributes"]:
                attribute_descriptions[attr["key"]] = attr["description"]

    pdf_bytes  = generate_pdf(
        category         = category,
        formulation      = result["formulation"],
        predicted_scores = result["predicted_scores"],
        target_scores    = result["target_scores"],
        confidence_pct   = result["confidence_pct"],
        residual_error   = result["residual_error"],
        compliance       = compliance,
        subcategory      = request.subcategory,
        attribute_descriptions = attribute_descriptions,
    )

    sub_label = f"_{request.subcategory}" if request.subcategory else ""
    return Response(
        content      = pdf_bytes,
        media_type   = "application/pdf",
        headers      = {"Content-Disposition": f"attachment; filename=notestack_{category}{sub_label}_report.pdf"}
    )