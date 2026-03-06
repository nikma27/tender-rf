# Tender RF — Настройка среды разработки

Руководство для синхронизации локальной и облачной среды разработки.

## Требования

- **Node.js** 18+ (для frontend)
- **Python** 3.11+ (для backend)
- **Git**
- **PostgreSQL** (опционально, для production)

## Локальная настройка

### 1. Клонирование репозитория

```bash
git clone <repository-url> tender-rf
cd tender-rf
```

### 2. Frontend

```bash
cd frontend
npm install
cp .env.example .env.local  # если есть
npm run dev
```

### 3. Backend

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Добавьте OPENAI_API_KEY в .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Переменные окружения

**Backend (.env):**
```
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tender_rf
DEBUG=false
```

**Frontend:** API вызывается на `http://localhost:8000` (настраивается в `document-dropzone.tsx`).

## Подключение удалённого репозитория

```bash
# GitHub
git remote add origin https://github.com/<username>/tender-rf.git
git branch -M main
git push -u origin main

# Или GitLab
git remote add origin https://gitlab.com/<username>/tender-rf.git
git push -u origin main
```

## Облачный агент (Cursor)

Проект настроен для работы с Cursor Cloud Agent:

- **AGENTS.md** — контекст проекта для AI-агента
- **.cursor/rules/** — правила кодирования (frontend, backend, общие)

### Синхронизация локального и облачного агента

1. **Правила (.cursor/rules/)** — автоматически подхватываются при открытии проекта
2. **AGENTS.md** — даёт агенту контекст о стеке, структуре и конвенциях
3. **Коммиты** — держите репозиторий в актуальном состоянии для облачной разработки

### Рекомендации

- Делайте коммиты после значимых изменений
- Обновляйте AGENTS.md при добавлении новых модулей или изменении архитектуры
- Используйте одинаковые версии зависимостей в локальной и облачной среде
