"""
Seed data for development and first run.

Fills the database with mock tenders if the tenders table is empty.
"""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models import Tender


# Mock tenders matching the Tender model structure
SEED_TENDERS = [
    {
        "external_id": "0373100017823000001",
        "title": "Поставка оргтехники для государственных нужд",
        "fz_type": "44-ФЗ",
        "initial_price": 2_500_000.0,
        "region": "Москва",
        "deadline": "2025-04-15",
        "document_url": None,
    },
    {
        "external_id": "0373100017823000002",
        "title": "Ремонт административного здания",
        "fz_type": "223-ФЗ",
        "initial_price": 15_000_000.0,
        "region": "Санкт-Петербург",
        "deadline": "2025-04-20",
        "document_url": None,
    },
    {
        "external_id": "0373100017823000003",
        "title": "Закупка медицинского оборудования",
        "fz_type": "44-ФЗ",
        "initial_price": 8_750_000.0,
        "region": "Московская область",
        "deadline": "2025-04-25",
        "document_url": None,
    },
    {
        "external_id": "0373100017823000004",
        "title": "Разработка программного обеспечения",
        "fz_type": "223-ФЗ",
        "initial_price": 12_300_000.0,
        "region": "Новосибирск",
        "deadline": "2025-04-30",
        "document_url": None,
    },
    {
        "external_id": "0373100017823000005",
        "title": "Поставка канцелярских товаров",
        "fz_type": "44-ФЗ",
        "initial_price": 450_000.0,
        "region": "Казань",
        "deadline": "2025-05-05",
        "document_url": None,
    },
    {
        "external_id": "0373100017823000006",
        "title": "Строительство спортивного комплекса",
        "fz_type": "44-ФЗ",
        "initial_price": 125_000_000.0,
        "region": "Екатеринбург",
        "deadline": "2025-05-15",
        "document_url": None,
    },
    {
        "external_id": "0373100017823000007",
        "title": "Услуги по охране объектов",
        "fz_type": "223-ФЗ",
        "initial_price": 3_200_000.0,
        "region": "Нижний Новгород",
        "deadline": "2025-05-22",
        "document_url": None,
    },
    {
        "external_id": "0373100017823000008",
        "title": "Поставка продуктов питания",
        "fz_type": "44-ФЗ",
        "initial_price": 1_850_000.0,
        "region": "Краснодар",
        "deadline": "2025-05-28",
        "document_url": None,
    },
]


def _parse_deadline(value: str) -> datetime:
    """Parse YYYY-MM-DD string to timezone-aware datetime (UTC)."""
    dt = datetime.strptime(value, "%Y-%m-%d")
    return dt.replace(tzinfo=timezone.utc)


def seed_tenders_if_empty(db: Session) -> int:
    """
    Add mock tenders if the tenders table is empty.
    Returns the number of tenders added.
    """
    count = db.query(Tender).count()
    if count > 0:
        return 0

    for data in SEED_TENDERS:
        tender = Tender(
            external_id=data["external_id"],
            title=data["title"],
            fz_type=data["fz_type"],
            initial_price=data["initial_price"],
            region=data["region"],
            deadline=_parse_deadline(data["deadline"]),
            document_url=data["document_url"],
        )
        db.add(tender)

    db.commit()
    return len(SEED_TENDERS)
