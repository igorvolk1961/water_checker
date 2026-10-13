# AquaPredict — Технологический стек (Architecture Stack)

**Статус:** утверждён 2026-10-13 (заказчиком/ведущим). Фиксирует выбор платформы и библиотек для реализации бэклога (`backlog/product_backlog.md`, план — `plans/backlog_implementation_plan.md`).

## 1. Стек

| Слой | Технология | Назначение | Обоснование |
| --- | --- | --- | --- |
| Web/API (SCR-01…12) | **FastAPI** + **Pydantic v2** + **uvicorn** | API веб-консоли, алерты, задачи, метрики | async, быстрый, автовалидация и OpenAPI |
| Веб-консоль (frontend) | **Jinja2 + HTMX + Chart.js** | экраны SCR-01…12 (server-rendered) | без node-сборки, быстрый старт, read-only поверх 1С (OQ-12) |
| Конфигурация | **pydantic-settings** | типизированные настройки из env | единый источник конфигурации |
| Данные | **PostgreSQL** + **SQLAlchemy 2.0** + **Alembic** | партии, инциденты, корректирующие действия, вердикты, аудит | надёжная реляционная БД, миграции |
| Телеметрия (хранение) | PostgreSQL (партиционирование) или **TimescaleDB** | time-series, retention 1 год (LGL-06) | эффективное хранение рядов |
| Интеграции | **httpx** (OData/HTTP к 1С), **asyncua** (OPC-UA), **paho-mqtt** (MQTT) | EPIC-01 (1С), EPIC-02 (телеметрия) | зрелые клиенты под протоколы проекта |
| ML (Слой 2, Cold Start) | **scikit-learn** (+ **pandas**, **numpy**); опц. **PyOD** | риск-скоринг, Anomaly Detection Baseline | стандарт для tabular/unsupervised |
| MLOps | **MLflow** (опц.) | версионирование моделей, метрики по слоям | эксперименты и реестр моделей |
| Фоновые задачи / очередь | **Redis** | ретраи синхронизации, переобучение, мониторинг дрейфа | брокер/хранилище очередей (например, на базе Redis) |
| Качество | **pytest**, **pytest-asyncio**, **respx**, **ruff**, **mypy** | тесты, линт, типы | стандартный инструментарий |
| Среда/зависимости | **uv** | venv, зависимости, lock | скорость и воспроизводимость |

## 2. Маппинг на эпики бэклога

- FastAPI/uvicorn → EPIC-13 (веб-консоль), EPIC-04/05/11 (API алертов/задач/метрик).
- httpx/asyncua/paho-mqtt → EPIC-01 (1С), EPIC-02 (телеметрия).
- SQLAlchemy/Alembic/PostgreSQL → данные всех эпиков; партиционирование телеметрии → EPIC-02.
- scikit-learn/pandas/numpy → EPIC-03 (Слой 1), EPIC-08 (Cold Start/Baseline), EPIC-09 (Слой 2).
- Redis → EPIC-01 (ретраи), EPIC-10 (переобучение/дрейф).
- MLflow → EPIC-10/11 (жизненный цикл моделей, метрики).

## 3. Замечания по окружению

- Проект — **приложение**, не библиотека: в `pyproject.toml` задано `[tool.uv] package = false`. Причина — сборка PEP 517 backend'ов в текущем окружении падает (SIGSEGV); пакет не устанавливается, импорт для тестов — через `pythonpath = ["src"]`, для запуска — `PYTHONPATH=src`. При переносе в «обычное» окружение установку пакета можно вернуть.
- Файл `.env` (по `.env.example`) не коммитится.

## 4. Связь с артефактами

- Требования и границы: `01_vision_and_scope.md`, `07_nonfunctional_requirements.md`.
- Интеграции и параметры: `02_glossary.md` §7, `requirements/measured_parameters.md`.
- Жизненный цикл ML: `10_cold_start_and_archival_data.md`, `kpi.md`.
- Экономика (роли/ставки): `cost/cost_estimation.md`.
