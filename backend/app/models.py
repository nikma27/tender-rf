"""
SQLAlchemy database models for Tender RF platform.

Tables:
- User: Authentication and user management
- Tender: Government and commercial tenders (44-FZ, 223-FZ)
- DocumentAnalysis: AI analysis results for uploaded tender documents
"""

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


class User(Base):
    """
    User account for authentication and personalization.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Tender(Base):
    """
    Government or commercial tender (44-FZ or 223-FZ).
    external_id typically comes from zakupki.gov.ru or similar sources.
    """

    __tablename__ = "tenders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    external_id: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    fz_type: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # '44-ФЗ' or '223-ФЗ'
    initial_price: Mapped[float] = mapped_column(Float, nullable=False)
    region: Mapped[str] = mapped_column(String(200), nullable=False)
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    document_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Relationship to document analyses
    analyses: Mapped[list["DocumentAnalysis"]] = relationship(
        "DocumentAnalysis", back_populates="tender", cascade="all, delete-orphan"
    )


class DocumentAnalysis(Base):
    """
    AI analysis result for an uploaded tender document.
    Stores summary, detected risks, and other insights.
    """

    __tablename__ = "document_analyses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tender_id: Mapped[int] = mapped_column(
        ForeignKey("tenders.id", ondelete="CASCADE"), nullable=False
    )
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    ai_summary: Mapped[str] = mapped_column(Text, nullable=True)
    risks_found: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationship back to tender
    tender: Mapped["Tender"] = relationship("Tender", back_populates="analyses")
