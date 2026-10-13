# API-контракт системы (API Contract)

Сводный контракт интеграционных поверхностей AquaPredict. Определяет **границы API**, сквозные конвенции и статусы версий. Основано на C4 (`diagrams/c4_*`), архитектуре (`architecture.md`), UI v0.3, FR v1.1 и NFR.

## 1. Поверхности API

| Поверхность | Направление | Протокол | Контракт | Статус |
| --- | --- | --- | --- | --- |
| **Интеграция с 1С** | AquaPredict ↔ «БИТ:LIMS» | OData (чтение), HTTP-сервис (запись) | `integration_contract_1c.md` | **v1.0 — FROZEN** |
| **Консольный API** | Веб-консоль ↔ API-сервер | REST + SSE | этот документ, §4 | **v0.1 — draft-frozen** (v1.0 к Gate 3/R0) |
| **Доменные события (async)** | модули/воркеры ↔ очередь | очередь Redis | `domain_events.md` | **v1.0 — FROZEN** |

Принцип: фронтенд **никогда не обращается к 1С напрямую**; все интеграции — на бэкенде (NFR-6).

## 2. Сквозные конвенции

- **База и формат:** `/api/v1`, JSON (UTF-8), Content-Type `application/json`.
- **Время:** ISO-8601 в UTC (суффикс `Z`); события/ряды содержат `ts`.
- **Идентификаторы:** UUID; доменные коды (TEL-xx, LAB-xx, EPIC-xx…) — по `02_glossary.md`.
- **Аутентификация:** сессия (cookie) или JWT после `POST /auth/login`; интеграция с AD/LDAP (NFR-8), локальные УЗ — фолбэк.
- **Авторизация:** RBAC на каждый эндпоинт (FR-14.1); нет роли → `403`.
- **Ошибки:** `{ "code": "...", "message": "...", "details": {}, "trace_id": "..." }` с корректным HTTP-кодом.
- **Идемпотентность:** для мутирующих операций — заголовок `Idempotency-Key`; повтор с тем же ключом возвращает существующий результат (FR-15.6).
- **Пагинация:** `?limit=&cursor=`; ответ `{ "items": [...], "next_cursor": "..." }`.
- **Лимиты:** при превышении лимита запросов — `429` + заголовок `Retry-After`. Внутренний guardrail к 1С — ≤ 60 зап./мин (NFR-6).
- **Индикатор синхронизации (UI-08, ST-07):** ответы содержат `X-Sync-Status: ok|queue|error` и `X-Sync-Last-Ok: <ts>`.
- **Версионирование и deprecation:** версия в пути (`/v1`); изменение — новая версия; deprecation объявляется за N недель; для 1С — LGL-R3.
- **Машиночитаемый контракт:** `openapi.json` (генерируется FastAPI) — версионируемый артефакт; фронтенд использует его для типизации.

## 3. Аутентификация

| Метод | Путь | Назначение |
| --- | --- | --- |
| POST | `/auth/login` | вход → роль и права |
| POST | `/auth/logout` | выход |
| GET | `/me` | профиль, роль, права (скрытие экранов по RBAC) |

## 4. Консольный API (v0.1)

| SCR / FR | Метод | Путь | Назначение |
| --- | --- | --- | --- |
| SCR-01 / FR-05 | GET | `/alerts?status=&layer=&line=&limit=` | лента алертов |
| SCR-01 / FR-05 | POST | `/alerts/{id}/ack` | подтверждение ознакомления (NFR-4) → аудит |
| SCR-01 / NFR-5 | GET | `/alerts/budget?line=` | потребление бюджета алертов (лимит 10/час) |
| SCR-01 | GET | `/lines` | линии и статусы партий |
| SCR-02 / FR-06 | GET | `/incidents?status=&party_id=` | список инцидентов |
| SCR-02 / FR-06 | GET | `/incidents/{id}` | карточка: атрибуты, ссылки, журнал |
| SCR-02 / FR-12 | POST | `/incidents/{id}/verdicts` | вердикт (В-1): `{value, reason_code, comment}` |
| SCR-02 | GET | `/verdict-reasons` | справочник причин |
| SCR-02/04 / FR-02/08 | GET | `/parties/{id}/telemetry?params=&window=` | ряды для трендов (метка достоверности — FR-16.4) |
| SCR-04 / FR-08 | GET | `/parties/{id}/lab-results` | результаты LAB-xx + сверка (информационная) |
| SCR-04 | GET | `/parties?status=` | партии из 1С (read-only) |
| SCR-03 / FR-06/07 | GET | `/tasks?type=ca\|sampling&status=` | задачи (read-only поверх 1С) |
| SCR-03 | GET | `/tasks/{id}` | карточка задачи (без мутаций) |
| SCR-06 / FR-13 | GET | `/metrics/model` | метрики по слоям, Baseline, статус модели |
| SCR-11 / LGL-09 | GET | `/settings/operating-point` | рабочая точка (порог, FPR/FNR, история) |
| SCR-11 / LGL-09 | PUT | `/settings/operating-point` | изменение порога (только АДМ) → аудит |
| SCR-09 / FR-16 | GET | `/telemetry/health` | статусы датчиков и буфер шлюза |
| SCR-10 / LGL-10 | GET | `/audit?from=&to=&user=&entity=&source=&category=` | журнал аудита |
| SCR-10 / FR-14.5 | GET | `/audit/export` | выгрузка аудита (РЛ/АДМ) |
| FR-05 | GET | `/ws/alerts` | **SSE**-поток алертов |

## 5. SSE-поток алертов

- Формат события: `event: alert`, `data: {json}` (атрибуты `RiskAlert`), heartbeat каждые ~15 с.
- Разрыв соединения → повторное подключение клиента; потерянные события восполняются из `GET /alerts` (курсор).
- SSE выбран вместо polling (низкая задержка, один канал); WebSocket — избыточен (ADR-04).

## 6. Коды ошибок (основные)

| Код | HTTP | Смысл |
| --- | --- | --- |
| `unauthorized` | 401 | не аутентифицирован |
| `forbidden` | 403 | нет роли/права |
| `not_found` | 404 | объект не найден |
| `validation_error` | 422 | некорректные данные |
| `conflict_idempotency` | 409 | конфликт ключа идемпотентности |
| `rate_limited` | 429 | превышен лимит запросов |
| `upstream_1c_unavailable` | 503 | 1С недоступна (запись в очередь) |

## 7. Связь с артефактами

- 1С: `integration_contract_1c.md`; события: `domain_events.md`.
- Требования: FR-05/06/08/09/13/14/15/16, NFR-1/4/5/6/8/9; UI `ui_requirements.md`.
- Архитектура: `architecture.md`, `diagrams/c4_components.md`.
