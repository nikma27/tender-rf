# Tender RF — Контекст для AI-агента

## О проекте

**Tender RF** — SaaS-платформа для поиска и анализа государственных и коммерческих тендеров в России (44-ФЗ, 223-ФЗ).

## Стек технологий

| Слой | Технологии |
|------|-------------|
| Frontend | Next.js 16 (App Router), React 19, Tailwind CSS v4, shadcn/ui |
| Backend | Python, FastAPI, SQLAlchemy |
| БД | PostgreSQL (тендеры), векторная БД (RAG — в планах) |
| AI | LangChain, OpenAI API (gpt-4o-mini), pypdf, python-docx |

## Структура проекта

```
tender-rf/
├── frontend/           # Next.js
│   └── src/
│       ├── app/        # App Router: layout, page, routes
│       ├── components/  # layout/, dashboard/, ui/
│       ├── data/       # mock-tenders
│       └── lib/        # utils
├── backend/            # FastAPI
│   └── app/
│       ├── main.py     # API endpoints
│       ├── models.py   # SQLAlchemy: User, Tender, DocumentAnalysis
│       ├── schemas/    # Pydantic: AnalysisResponse
│       ├── services/   # ai_analyzer (LangChain, PDF/DOCX)
│       ├── db/         # database.py
│       └── core/       # config
└── .cursor/rules/      # Правила для агента
```

## Ключевые эндпоинты

- `GET /api/health` — health check
- `GET /api/tenders` — список тендеров (mock)
- `POST /api/analyze` — загрузка PDF/DOCX, AI-анализ (LangChain + OpenAI)

## Дизайн-система (Frontend)

- Тёмная тема по умолчанию
- Glassmorphism: `bg-white/5 backdrop-blur-md border border-white/10`
- Шрифт: Manrope
- Минимализм, без лишних декораций

## Синхронизация облачного и локального агента

1. **Правила** в `.cursor/rules/` — общие для всех сессий
2. **AGENTS.md** — контекст проекта (этот файл)
3. **Переменные окружения** — `backend/.env` с `OPENAI_API_KEY`, `DATABASE_URL`
4. **Запуск**:
   - Frontend: `cd frontend && npm run dev` → http://localhost:3000
   - Backend: `cd backend && .\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000` → http://localhost:8000

## Текущий этап MVP

- [x] Dashboard, Sidebar, Tender Table, Document Dropzone
- [x] AI-анализ документов (PDF/DOCX) через LangChain
- [ ] Подключение PostgreSQL
- [ ] Аутентификация
- [ ] Интеграция с zakupki.gov.ru

## Cursor Cloud specific instructions

### Services

| Service | Command | Port |
|---------|---------|------|
| Frontend (Next.js) | `cd frontend && npm run dev` | 3000 |
| Backend (FastAPI) | `cd backend && python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` | 8000 |

- **Backend**: use `python3 -m uvicorn` (not bare `uvicorn`) — the pip-installed script may not be on `PATH` in the Cloud VM.
- **Backend `.env`**: copy from `backend/.env.example` if `backend/.env` doesn't exist (`cp backend/.env.example backend/.env`). The `OPENAI_API_KEY` secret is optional — without it, `/api/analyze` returns 503, but the dashboard, tender table, and navigation work fine.
- PostgreSQL is **not wired in** yet (`main.py` doesn't import any DB code), so no database is needed.

### Lint / Build / Test

- Frontend lint: `npm run lint` (in `frontend/`)
- Frontend build: `npm run build` (in `frontend/`)
- Backend has no automated tests or lint configured yet.

### Gotchas

- The frontend tender table uses **local mock data** (`frontend/src/data/mock-tenders.ts`), not the backend API. The document dropzone on the main dashboard page calls `localhost:8000/api/analyze` client-side.
- Some sidebar pages (AI Анализ, Мои тендеры, Настройки) show "Страница в разработке" — this is expected, not a bug.
