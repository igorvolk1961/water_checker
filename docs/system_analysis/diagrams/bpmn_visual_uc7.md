# BPMN (визуальная версия) — UC7: Cold Start

**Версия:** 1.0 (визуализация `bpmn_uc7_cold_start.md`; канонические BPMN 2.0/SVG — `diagrams/bpmn/uc7.*`). Термины — `02_glossary.md`.

```mermaid
flowchart TB
  classDef person fill:#e8f0fe,stroke:#1a73e8,color:#16262e
  classDef sys fill:#e2f1f2,stroke:#0e7c86,color:#16262e
  classDef event fill:#fff8e1,stroke:#a3660a,color:#16262e
  classDef gw fill:#fdecea,stroke:#b03a2e,color:#16262e

  subgraph L1["Система (ETL-пайплайн)"]
    direction TB
    S1["Импорт архива: SCADA (CSV/<br/>OPC-UA HDA) + журналы<br/>отчёт о качестве (FR-10.1)"]:::sys
    G1{"архивных данных<br/>достаточно?"}:::gw
    S2["Pre-training на синтетике<br/>цифрового двойника,<br/>продление калибровки (7а)"]:::sys
    S3["Матчинг «срез 2 ч → проба»<br/>отчёт, цель ≥ 90 % (FR-10.2)"]:::sys
    S4["Обучение Baseline-профиля<br/>(Anomaly Detection) → [Черновик]"]:::sys
    S5["Shadow Mode: прогнозы<br/>персоналу не показываются,<br/>накопление метрик (FR-04.2)"]:::sys
    G2{"критерии §4 выполнены?<br/>(Recall ≥ 0,75, FPR ≤ 0,10,<br/>≥ 4 нед, ≥ N инцидентов)"}:::gw
    S6["Переключение в Advisor<br/>(решение фиксируется)"]:::sys
  end

  subgraph L2["ML-инженер (DS)"]
    direction TB
    D1["Запуск мастера Cold Start<br/>(SCR-08)"]:::person
    D2["Проверка профиля,<br/>размещение в Shadow"]:::person
  end

  subgraph L3["Главный технолог (ГТ)"]
    direction TB
    H1["Подтверждение профиля<br/>«Эталонный» (ST-06,<br/>фиксация в аудите)"]:::person
  end

  E0(("▶ Доступны архивы<br/>SCADA и журналы")):::event
  E1(("⏹ Режим Advisor —<br/>калибровка завершена")):::event

  E0 --> D1 --> S1 --> G1
  G1 -- "да" --> S3
  G1 -- "нет (7а)" --> S2 --> S3
  S3 --> S4 --> D2 --> S5
  S5 --> H1 --> G2
  G2 -- "да" --> S6 --> E1
  G2 -- "нет" --> S5
```

## Инварианты

- Слой 1 (правила) стартует независимо от Cold Start; Слой 2 — по критериям перехода (`10_cold_start_and_archival_data.md` §4, `kpi.md` §6).
- Матчинг архива — тот же механизм, что и связка в текущей работе (FR-08.4).
- Доля успешного матчинга ≥ 90 % — системный KPI (`kpi.md` §4).
