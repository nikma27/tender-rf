from fastapi import APIRouter

router = APIRouter()

MOCK_TENDERS = [
    {
        "id": 1,
        "title": "Поставка оргтехники для государственных нужд",
        "fzType": "44-ФЗ",
        "price": "2 500 000 ₽",
        "region": "Москва",
        "deadline": "15.04.2025",
    },
    {
        "id": 2,
        "title": "Ремонт административного здания",
        "fzType": "223-ФЗ",
        "price": "15 000 000 ₽",
        "region": "Санкт-Петербург",
        "deadline": "20.04.2025",
    },
    {
        "id": 3,
        "title": "Закупка медицинского оборудования",
        "fzType": "44-ФЗ",
        "price": "8 750 000 ₽",
        "region": "Московская область",
        "deadline": "25.04.2025",
    },
]


@router.get("")
def get_tenders():
    """Возвращает список тендеров (заглушка для MVP)."""
    return MOCK_TENDERS
