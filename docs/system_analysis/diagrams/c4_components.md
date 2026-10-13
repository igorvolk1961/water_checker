# C4-3. Диаграмма компонентов (Components: API-сервер и ML-воркер)

**Версия:** 1.0. Раскрыты два самых нагруженных контейнера; состав компонентов — из FR v1.1 (блоки → модули). Обозначения как на C4-2.

```mermaid
flowchart TB
  classDef container fill:#e2f1f2,stroke:#0e7c86,color:#16262e
  classDef comp fill:#ffffff,stroke:#0e7c86,color:#16262e
  classDef data fill:#fff8e1,stroke:#a3660a,color:#16262e
  classDef ext fill:#f1f3f4,stroke:#5f6368,stroke-dasharray:4,color:#16262e

  subgraph API["API-сервер (FastAPI)"]
    direction TB
    ALERT["Контур алертинга<br/>RiskAlert ≤ 5 с (NFR-1),<br/>бюджет ≤ 10/час, подавление дублей<br/>до инцидента (NFR-5, В-6),<br/>рабочая точка (LGL-09)"]:::comp
    ENGINE["Риск-движок<br/>Слой 1: справочник правил;<br/>Слой 2: ML-inference,<br/>Shadow → Advisor (ST-05)"]:::comp
    SYNC["Сервис интеграции 1С<br/>OData-ридер (пакетирование),<br/>HTTP-писатель с ключом<br/>идемпотентности (FR-15.6)"]:::comp
    QUAL["Контроль качества потока<br/>пропуски/замороженные/<br/>диапазон → FR-16, пометка<br/>достоверности скоринга"]:::comp
    LABEL["Агрегатор обучающих примеров<br/>проба → срез 2 ч (FR-08.4),<br/>приоритет: протокол &gt; вердикт,<br/>карантин конфликтов (FR-11.2)"]:::comp
    AUDIT["Аудит-сервис<br/>рекомендация системы /<br/>решение человека / действие;<br/>источник AquaPredict|1С (LGL-10)"]:::comp
    RBAC["RBAC и сессии<br/>7 ролей, маскирование ПДн (LGL-05)"]:::comp
  end

  subgraph MLW["ML-воркер"]
    direction TB
    TRAIN["Пайплайн обучения<br/>Baseline (Anomaly Detection),<br/>Слой 2; Pre-training на синтетике (7а)"]:::comp
    EVAL["Сравнение метрик и откат<br/>Recall ≥ 0,75 при FPR ≤ 0,10<br/>(kpi §2), отмена при дрейфе (6а)"]:::comp
    DRIFT["Мониторинг дрейфа<br/>непрерывный (LGL-13, FR-11.6)"]:::comp
    REG["Реестр моделей (MLflow)<br/>версии: Shadow → Advisor →<br/>Production → Архив"]:::comp
  end

  PG[("PostgreSQL")]:::data
  RD[("Redis")]:::data
  ONEC["«БИТ.Лаборатория» (1С)"]:::ext
  TELIN["Приёмник телеметрии"]:::container
  UI["Веб-консоль"]:::container
  PUSH["Push/SMS-шлюз"]:::ext

  TELIN --> QUAL
  QUAL -- "достоверные ряды" --> ENGINE
  ENGINE -- "риск ≥ рабочей точки" --> ALERT
  ALERT -- "инцидент, задачи CA" --> SYNC
  SYNC -- "OData / HTTP" --> ONEC
  ALERT -- "уведомления" --> PUSH
  LABEL --> PG
  TRAIN --> EVAL
  EVAL --> REG
  TRAIN --> PG
  DRIFT --> RD
  ALERT --> UI
  AUDIT --> PG
  RBAC --> PG
```

## Связь с документами

- Компоненты ↔ FR: алертинг — FR-05; движок — FR-03/04; интеграция — FR-15; контроль потока — FR-02.4/FR-16; агрегатор — FR-08.4/FR-11; аудит — FR-14.3; пайплайн — FR-10/FR-11.
- Компоненты ↔ BPMN: шаги UC2/UC3 (alerting → sync → 1С), UC6 (TRAIN/EVAL/DRIFT), UC7 (TRAIN), UC8 (QUAL).
- Состав раскрыт до уровня, достаточного для оценки задач R0–R2 (`plans/backlog_implementation_plan.md`); детализация до «Code»-уровня — в зоне backend при реализации.
