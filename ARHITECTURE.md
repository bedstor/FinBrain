# 🗺️ Архитектура платформы FinBrain

## 📥 1. Поток данных (Data Flow)
User (PDF) ➡️ FastAPI (app/api/endpoints.py) ➡️ Parser (app/core/parser.py) ➡️ OpenAI (app/core/ai_advisor.py) ➡️ Pandas (app/core/analytics.py) ➡️ SQLite3 (app/database/models.py) ➡️ Plotly

## 🧩 2. Модули системы
1. `main.py` — Главный асинхронный запуск FastAPI.
2. `parser.py` — Скрипт, который читает PDF и вытаскивает из него текст.
3. `ai_advisor.py` — Модуль для асинхронных запросов к OpenAI.
4. `analytics.py` — Движок Pandas для построения графиков и расчетов.
5. `database.py` — Управление таблицами SQLite3.
