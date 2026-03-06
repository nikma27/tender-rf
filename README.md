# Tender RF — AI-платформа для тендеров РФ

SaaS-платформа для поиска и анализа государственных и коммерческих тендеров (44-ФЗ, 223-ФЗ).

## Структура проекта

```
tender-rf/
├── frontend/     # Next.js (App Router), React, Tailwind, shadcn/ui
├── backend/      # FastAPI, Python
└── README.md
```

## Запуск

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Приложение будет доступно по адресу http://localhost:3000

### Backend

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API будет доступно по адресу http://localhost:8000

## MVP Phase 1

- [x] Инициализация Next.js и shadcn/ui
- [x] Дизайн-система (тёмная тема, glassmorphism, Manrope)
- [x] Sidebar навигация (Поиск, AI Анализ, Мои тендеры, Настройки)
- [x] Таблица тендеров с mock-данными
- [x] Dropzone для загрузки PDF/Word
- [x] Contact Widget (Менеджер Макс, форма обратного звонка)
- [x] FastAPI backend (health check, заглушка тендеров)
