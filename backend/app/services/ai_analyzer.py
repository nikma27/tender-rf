"""
AI document analysis service using LangChain and OpenAI.

Extracts text from PDF/Word, analyzes with LLM as Russian tender specialist.
"""

import io
import json
import logging
from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from pypdf import PdfReader
from pydantic import ValidationError

from app.schemas.analysis import AnalysisResponse

logger = logging.getLogger(__name__)

# System prompt: strict instructions for Russian tender specialist
SYSTEM_PROMPT = """Ты — строгий эксперт по анализу тендерной документации (44-ФЗ, 223-ФЗ) в России.
Твоя задача: выявить риски, неоднозначности и ловушки в техническом задании и условиях контракта.

АНАЛИЗИРУЙ ДОКУМЕНТ И ВЕРНИ СТРОГО JSON со следующими полями (все массивы строк, margin_estimation — одна строка):

{
  "hidden_risks": ["риск 1", "риск 2", ...],
  "unclear_terms": ["неоднозначность 1", ...],
  "short_deadlines": ["срок 1", ...],
  "technical_traps": ["ловушка 1", ...],
  "margin_estimation": "Рекомендация по марже с учётом рисков"
}

ПРАВИЛА:
1. hidden_risks: скрытые штрафы, отсутствие авансов, невыгодные условия оплаты, размытые критерии приёмки.
2. unclear_terms: формулировки типа «в разумные сроки», «соответствие ГОСТ» без указания редакции, неопределённые требования.
3. short_deadlines: нереалистичные сроки подачи заявки или исполнения контракта (сравни с отраслевыми нормами).
4. technical_traps: привязка к конкретному бренду/модели без «или эквивалент» (особенно ВКР, вентиляция, кондиционирование, HVAC, оборудование).
5. margin_estimation: краткая рекомендация по маржинальности (например: «Рекомендуемая маржа 12–18% с учётом рисков»).
6. Если по категории ничего не найдено — верни пустой массив [].
7. Отвечай ТОЛЬКО валидным JSON, без markdown, без пояснений до или после."""


def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF using pypdf."""
    reader = PdfReader(io.BytesIO(file_content))
    text_parts = []
    for page in reader.pages:
        try:
            text_parts.append(page.extract_text() or "")
        except Exception as e:
            logger.warning("Failed to extract page: %s", e)
    return "\n\n".join(text_parts).strip()


def extract_text_from_docx(file_content: bytes) -> str:
    """Extract text from DOCX using python-docx."""
    from docx import Document

    doc = Document(io.BytesIO(file_content))
    return "\n\n".join(p.text for p in doc.paragraphs).strip()


def extract_text(file_content: bytes, filename: str) -> str:
    """Extract text from PDF or DOCX based on file extension."""
    path = Path(filename.lower())
    if path.suffix == ".pdf":
        return extract_text_from_pdf(file_content)
    if path.suffix == ".docx":
        return extract_text_from_docx(file_content)
    raise ValueError(f"Unsupported file type: {path.suffix}")


def analyze_tender_document(
    file_content: bytes,
    filename: str,
    *,
    model: str = "gpt-4o-mini",
    api_key: str | None = None,
) -> AnalysisResponse:
    """
    Analyze tender document text with LLM and return structured result.

    Args:
        file_content: Raw file bytes
        filename: Original filename (for extension detection)
        model: OpenAI model (gpt-4o, gpt-4o-mini, gpt-3.5-turbo)
        api_key: OpenAI API key (default from env OPENAI_API_KEY)

    Returns:
        AnalysisResponse with risks, traps, deadlines, margin
    """
    text = extract_text(file_content, filename)
    if not text or len(text.strip()) < 50:
        return AnalysisResponse(
            file_name=filename,
            hidden_risks=["Документ пуст или текст не извлечён"],
            unclear_terms=[],
            short_deadlines=[],
            technical_traps=[],
            margin_estimation="Невозможно оценить маржу без содержимого документа.",
        )

    # Truncate if too long (context limit)
    max_chars = 120_000
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n[... документ обрезан ...]"

    llm = ChatOpenAI(
        model=model,
        temperature=0.1,
        api_key=api_key,
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Проанализируй следующий фрагмент тендерной документации:\n\n{text}"),
    ]

    response = llm.invoke(messages)
    raw = response.content.strip()

    # Remove markdown code blocks if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        logger.error("LLM returned invalid JSON: %s", e)
        return AnalysisResponse(
            file_name=filename,
            hidden_risks=["Ошибка разбора ответа ИИ. Попробуйте загрузить документ снова."],
            unclear_terms=[],
            short_deadlines=[],
            technical_traps=[],
            margin_estimation="",
        )

    data["file_name"] = filename
    try:
        return AnalysisResponse.model_validate(data)
    except ValidationError as e:
        logger.error("Validation error: %s", e)
        return AnalysisResponse(
            file_name=filename,
            hidden_risks=[f"Ошибка формата ответа: {str(e)}"],
            unclear_terms=[],
            short_deadlines=[],
            technical_traps=[],
            margin_estimation="",
        )
