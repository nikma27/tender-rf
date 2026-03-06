"""
Pydantic schemas for AI document analysis response.

Strict structure for LLM output - ensures clean JSON for frontend.
"""

from pydantic import BaseModel, Field


class AnalysisResponse(BaseModel):
    """Structured AI analysis result for tender documentation."""

    file_name: str = Field(..., description="Original uploaded file name")
    hidden_risks: list[str] = Field(
        default_factory=list,
        description="Скрытые риски: штрафы, отсутствие авансов, невыгодные условия",
    )
    unclear_terms: list[str] = Field(
        default_factory=list,
        description="Неоднозначные формулировки и требования",
    )
    short_deadlines: list[str] = Field(
        default_factory=list,
        description="Нереалистичные сроки исполнения или подачи заявки",
    )
    technical_traps: list[str] = Field(
        default_factory=list,
        description="Технические ловушки: привязка к бренду без «или аналог», ВКР, вентиляция и т.д.",
    )
    margin_estimation: str = Field(
        default="",
        description="Рекомендация по маржинальности с учётом рисков",
    )
