"""
Tender RF API - FastAPI application entry point.

Provides REST API for tender search and AI document analysis.
"""

import asyncio
import os
from datetime import datetime

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.schemas.analysis import AnalysisResponse
from app.services.ai_analyzer import analyze_tender_document

app = FastAPI(
    title="Tender RF API",
    description="AI-платформа для поиска и анализа тендеров (44-ФЗ, 223-ФЗ)",
    version="0.1.0",
)

# CORS: allow Next.js frontend on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------------------------------------------
# Mock data for GET /api/tenders (matches Tender model structure)
# -----------------------------------------------------------------------------
MOCK_TENDERS = [
    {
        "id": 1,
        "external_id": "0373100017823000001",
        "title": "Поставка оргтехники для государственных нужд",
        "fz_type": "44-ФЗ",
        "initial_price": 2_500_000.0,
        "region": "Москва",
        "deadline": "2025-04-15",
        "document_url": None,
    },
    {
        "id": 2,
        "external_id": "0373100017823000002",
        "title": "Ремонт административного здания",
        "fz_type": "223-ФЗ",
        "initial_price": 15_000_000.0,
        "region": "Санкт-Петербург",
        "deadline": "2025-04-20",
        "document_url": None,
    },
    {
        "id": 3,
        "external_id": "0373100017823000003",
        "title": "Закупка медицинского оборудования",
        "fz_type": "44-ФЗ",
        "initial_price": 8_750_000.0,
        "region": "Московская область",
        "deadline": "2025-04-25",
        "document_url": None,
    },
    {
        "id": 4,
        "external_id": "0373100017823000004",
        "title": "Разработка программного обеспечения",
        "fz_type": "223-ФЗ",
        "initial_price": 12_300_000.0,
        "region": "Новосибирск",
        "deadline": "2025-04-30",
        "document_url": None,
    },
    {
        "id": 5,
        "external_id": "0373100017823000005",
        "title": "Поставка канцелярских товаров",
        "fz_type": "44-ФЗ",
        "initial_price": 450_000.0,
        "region": "Казань",
        "deadline": "2025-05-05",
        "document_url": None,
    },
    {
        "id": 6,
        "external_id": "0373100017823000006",
        "title": "Строительство спортивного комплекса",
        "fz_type": "44-ФЗ",
        "initial_price": 125_000_000.0,
        "region": "Екатеринбург",
        "deadline": "2025-05-15",
        "document_url": None,
    },
    {
        "id": 7,
        "external_id": "0373100017823000007",
        "title": "Услуги по охране объектов",
        "fz_type": "223-ФЗ",
        "initial_price": 3_200_000.0,
        "region": "Нижний Новгород",
        "deadline": "2025-05-22",
        "document_url": None,
    },
    {
        "id": 8,
        "external_id": "0373100017823000008",
        "title": "Поставка продуктов питания",
        "fz_type": "44-ФЗ",
        "initial_price": 1_850_000.0,
        "region": "Краснодар",
        "deadline": "2025-05-28",
        "document_url": None,
    },
]


def _format_tender_for_frontend(tender: dict) -> dict:
    """Format tender for frontend display (price as string, deadline as DD.MM.YYYY)."""
    price_str = f"{tender['initial_price']:,.0f}".replace(",", " ") + " ₽"
    deadline_str = _format_deadline(tender["deadline"])
    return {
        "id": tender["id"],
        "title": tender["title"],
        "fzType": tender["fz_type"],
        "price": price_str,
        "region": tender["region"],
        "deadline": deadline_str,
    }


def _format_deadline(deadline: str) -> str:
    """Convert YYYY-MM-DD to DD.MM.YYYY."""
    try:
        dt = datetime.strptime(deadline, "%Y-%m-%d")
        return dt.strftime("%d.%m.%Y")
    except (ValueError, TypeError):
        return str(deadline)


# -----------------------------------------------------------------------------
# API Endpoints
# -----------------------------------------------------------------------------


@app.get("/api/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "ok", "message": "Tender RF API is running"}


@app.get("/api/tenders")
def get_tenders():
    """
    Returns a list of tenders for frontend display.
    Uses mock data matching the Tender model structure.
    """
    return [_format_tender_for_frontend(t) for t in MOCK_TENDERS]


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
