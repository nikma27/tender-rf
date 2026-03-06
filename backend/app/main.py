"""
Tender RF API - FastAPI application entry point.

Provides REST API for tender search and AI document analysis.
"""

import asyncio
import os
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.db.database import get_db, init_db
from app.db.seed import seed_tenders_if_empty
from app.models import Tender
from app.schemas.analysis import AnalysisResponse
from app.services.ai_analyzer import analyze_tender_document


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan: при старте создаём таблицы и заполняем тестовыми данными, если БД пуста.
    """
    init_db()
    db = next(get_db())
    try:
        seed_tenders_if_empty(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="Tender RF API",
    description="AI-платформа для поиска и анализа тендеров (44-ФЗ, 223-ФЗ)",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS: allow Next.js frontend on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _format_tender_for_frontend(tender: Tender) -> dict:
    """Format tender for frontend display (price as string, deadline as DD.MM.YYYY)."""
    price_str = f"{tender.initial_price:,.0f}".replace(",", " ") + " ₽"
    deadline_str = _format_deadline(tender.deadline)
    return {
        "id": tender.id,
        "title": tender.title,
        "fzType": tender.fz_type,
        "price": price_str,
        "region": tender.region,
        "deadline": deadline_str,
    }


def _format_deadline(deadline: datetime) -> str:
    """Convert datetime to DD.MM.YYYY."""
    try:
        return deadline.strftime("%d.%m.%Y")
    except (ValueError, TypeError, AttributeError):
        return str(deadline)


# -----------------------------------------------------------------------------
# API Endpoints
# -----------------------------------------------------------------------------


@app.get("/api/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "ok", "message": "Tender RF API is running"}


@app.get("/api/tenders")
def get_tenders(db: Session = Depends(get_db)):
    """
    Returns a list of tenders for frontend display.
    Reads from PostgreSQL (seeded on first run).
    """
    tenders = db.query(Tender).order_by(Tender.deadline).all()
    return [_format_tender_for_frontend(t) for t in tenders]


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_document(file: UploadFile = File(...)):
    """
    Accepts a PDF or DOCX file upload, extracts text, and analyzes with LLM.
    Returns structured risks, unclear terms, short deadlines, technical traps, and margin estimation.
    """
    allowed_types = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    }
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF and DOCX are accepted.",
        )

    content = await file.read()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="OPENAI_API_KEY not configured. Set it in backend/.env",
        )

    # Run CPU-bound analysis in thread pool to avoid blocking event loop
    import asyncio
    from functools import partial

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        partial(
            analyze_tender_document,
            content,
            file.filename or "document.pdf",
            api_key=api_key,
        ),
    )
    return result
