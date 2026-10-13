# Доменные события системы (Domain Events)

Схемы асинхронных событий, циркулирующих через очередь (Redis). Используются воркерами (ретраи к 1С, инциденты/задачи, разметка) и для аудита. **Версия:** v1.0 — FROZEN.

## 0. Общие правила

- Транспорт: очередь Redis (persistent, AOF/RDB); доставка **at-least-once**.
- Для каждого события: `event_id` (UUID), `type`, `ts` (ISO-8601 UTC), `version` (схема события), `payload`.
- **Идемпотентность потребителя:** обработка по `event_id` + бизнес-ключу (см. `integration_contract_1c.md`).
- Все события, влияющие на решения/задачи, зеркалируются в аудит-лог (LGL-10).
- Ошибки обработки → повтор с экспоненциальной задержкой; после N попыток → «мёртвая» очередь + уведомление.

## 1. Перечень событий

| Тип | Producer | Consumer | Назначение | FR |
| --- | --- | --- | --- | --- |
| `RiskAlert` | Движок риск-скоринга | Алертинг, UI (SSE) | сформирован алерт о риске | FR-05 |
| `IncidentCreated` | Алертинг | Задачи, аудит | создан предиктивный инцидент | FR-06.1 |
| `CorrectiveActionRequested` | Инциденты | Синхронизация с 1С | создать задачу на корректирующее действие | FR-06.3 |
| `SamplingRequested` | Инциденты | Синхронизация с 1С | создать задание внепланового отбора | FR-07.1 |
| `VerdictRecorded` | Инциденты | Синхронизация, разметка | зафиксирован вердикт по инциденту | FR-06.5, FR-12 |
| `BatchCloseBlocked` | Инциденты | Синхронизация с 1С | блокировка закрытия партии | FR-01.4 |
| `BatchCloseUnblocked` | Инциденты | Синхронизация с 1С | снятие блокировки | FR-01.4 |
| `TelemetryQualityEvent` | Приёмник телеметрии | Мониторинг (EPIC-14) | событие качества канала (пропуск/заморозка/диапазон) | FR-02.4, FR-16 |
| `ModelDeployed` | ML-воркер (MLOps) | UI, аудит | развёрнута новая версия модели | FR-11.4 |
| `DriftDetected` | ML-воркер (дрейф) | UI, уведомления | обнаружен дрейф модели | FR-11.6 |

## 2. Схемы payload (ключевые поля)

**`RiskAlert`:** `party_id`, `param` (TEL-код), `risk_score` (0..1), `horizon` (мин), `recommendation`, `source` (`Слой 1`|`Слой 2`).

**`IncidentCreated`:** `incident_id`, `party_id`, `param`, `risk_score`, `alert_id`.

**`CorrectiveActionRequested`:** `incident_id`, `party_id`, `steps[]`, `priority`; ключ идемпотентности: `incident_id + task_type + version`.

**`SamplingRequested`:** `incident_id`, `party_id`, `target_param`, `priority="urgent"`.

**`VerdictRecorded`:** `incident_id`, `value` (`подтверждён`|`ложное_срабатывание`), `reason_code`, `author`, `ts`.

**`BatchCloseBlocked` / `BatchCloseUnblocked`:** `party_id`, `reason`/`context`.

**`TelemetryQualityEvent`:** `sensor` (TEL-код), `issue` (`no_data`|`frozen`|`out_of_range`|`delay`), `ts`.

**`ModelDeployed`:** `model_id`, `version`, `status` (`Shadow`|`Advisor`|`Production`), `metrics{}`.

**`DriftDetected`:** `model_id`, `version`, `signal` (`ks`|`psi`|`cusum`|`adwin`), `score`, `action_recommended`.

## 3. Гарантии и аудит

- **Гарантия доставки:** at-least-once; повторная обработка безопасна за счёт идемпотентности.
- **Упорядоченность:** не гарантируется между разными типами; внутри одного `party_id` — по возможности через ключ партиционирования.
- **Аудит:** события, связанные с рекомендацией/решением/действием, пишутся в аудит-лог с источником `AquaPredict`.
- **Хранение:** журнал событий и «мёртвая» очередь — в PostgreSQL; обретают срок хранения по LGL-06 (1 год) для операционных журналов.

## 4. Связь с артефактами

- Интеграция с 1С: `integration_contract_1c.md`; API: `api_contract.md`.
- Архитектура (очередь, idempotency, outbox-подобная модель): `architecture.md` §4.
- Требования: FR-01/02/05/06/07/11/12/16, NFR-5/6.
