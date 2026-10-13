# C4-2. Диаграмма контейнеров (Containers)

**Версия:** 1.0. Технологии — утверждённый стек `architecture_stack.md`; состав — FR v1.1. Обозначения: голубой — персона, зелёный контур — контейнеры AquaPredict, серый пунктир — внешние.

```mermaid
flowchart LR
  classDef person fill:#e8f0fe,stroke:#1a73e8,color:#16262e
  classDef container fill:#e2f1f2,stroke:#0e7c86,color:#16262e
  classDef data fill:#fff8e1,stroke:#a3660a,color:#16262e
  classDef ext fill:#f1f3f4,stroke:#5f6368,stroke-dasharray:4,color:#16262e

  ГТ["👤 ГТ"]:::person
  КИП["👤 КИПиА"]:::person
  DS["👤 DS"]:::person
  АДМ["👤 АДМ"]:::person

  subgraph AQ["AquaPredict"]
    direction TB
    UI["Веб-консоль<br/>SCR-01…12, дисклеймеры,<br/>баннер синхронизации"]:::container
    API["API-сервер<br/>FastAPI/uvicorn,<br/>REST + SSE, RBAC"]:::container
    SYNC["Сервис синхронизации с 1С<br/>httpx: OData-ридер,<br/>HTTP-писатель (идемпотентно),<br/>≤ 60 зап/мин (NFR-6)"]:::container
    TELIN["Приёмник телеметрии<br/>asyncua (OPC-UA),<br/>paho-mqtt (MQTT),<br/>контроль качества потока"]:::container
    MLW["ML-воркер<br/>scikit-learn, MLflow:<br/>Baseline, Слой 2,<br/>переобучение, дрейф"]:::container
    PG[("PostgreSQL<br/>партии/инциденты/вердикты/<br/>аудит; телеметрия —<br/>партиционирование, 1 год (LGL-06)")]:::data
    RD[("Redis<br/>очередь: ретраи 1С,<br/>переобучение, дрейф")]:::data
  end

  ONEC["«БИТ.Лаборатория» (1С)"]:::ext
  GW["IoT-шлюз + датчики"]:::ext
  PUSH["Push/SMS-шлюз"]:::ext

  ГТ --> UI
  КИП --> UI
  DS --> UI
  АДМ --> UI
  UI -- "REST + SSE<br/>(API-контракт консоли)" --> API
  API --> PG
  API --> RD
  API -- "уведомления" --> PUSH
  RD -- "задачи переобучения/дрейфа" --> MLW
  MLW --> PG
  API -- "задания на синхронизацию" --> SYNC
  SYNC -- "OData чтение /<br/>HTTP запись" --> ONEC
  TELIN -- "запись рядов,<br/>события качества" --> PG
  GW -- "OPC-UA/MQTT" --> TELIN
```

## Примечания

- **Пуш/SMS-шлюз** — внешний сервис доставки (SCR-12); лаборанту уведомления идут средствами 1С (OQ-04).
- **IoT-шлюз** — оборудование, поставляемое Исполнителем (Приложение № 3); буферизация ≥ 2 ч (NFR-2), NTP.
- Деградация 1С не блокирует приём телеметрии и скоринг — очередь в Redis персистентна (FR-15.5).
- Выбор фронтенд-технологии консоли — OQ-12 (решение ведущего); на диаграмме контейнер не зависит от этого решения.
