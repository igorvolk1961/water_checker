# BPMN (визуальная версия) — UC4: Внеплановый отбор пробы

**Версия:** 1.0 (визуализация `bpmn_uc4_trigger_sampling.md` стандартным mermaid). Термины — `02_glossary.md`.

```mermaid
flowchart TB
  classDef person fill:#e8f0fe,stroke:#1a73e8,color:#16262e
  classDef sys fill:#e2f1f2,stroke:#0e7c86,color:#16262e
  classDef onec fill:#f1f3f4,stroke:#5f6368,stroke-dasharray:4,color:#16262e
  classDef event fill:#fff8e1,stroke:#a3660a,color:#16262e
  classDef gw fill:#fdecea,stroke:#b03a2e,color:#16262e

  subgraph L1["Система AquaPredict"]
    direction TB
    S1["Генерация задания<br/>«Внеплановый отбор»,<br/>«Срочно» → в 1С (FR-07.1)"]:::sys
    S2["Чтение статуса задания<br/>и пробы (OData)<br/>ссылка: инцидент →<br/>задание → проба"]:::sys
    S3["Связка «проба → срез<br/>телеметрии 2 ч» → метка<br/>(FR-08.4)"]:::sys
  end

  subgraph L2["Лаборант (в 1С)"]
    direction TB
    H1["Уведомление штатными<br/>средствами 1С (OQ-04)"]:::person
    H2["Физический отбор пробы,<br/>стерильная тара, маркировка<br/>(вне систем, HITL)"]:::person
    H3["Сканирование штрихкода<br/>— подтверждение отбора<br/>(Chain of Custody — 1С)"]:::person
  end

  subgraph L3["БИТ:LIMS (1С)"]
    direction TB
    O1["Задание в модуле отбора,<br/>уведомление лаборанту"]:::onec
    O2["Лабораторный анализ,<br/>протокол испытаний<br/>(ground truth, LGL-01/02)"]:::onec
  end

  E0(("Вход: высокий риск<br/>(из UC2)")):::event
  E1(("Ground Truth →<br/>обучающая выборка (UC6)")):::event

  E0 --> S1 --> O1 --> H1 --> H2 --> H3 --> O2
  O2 --> S2 --> S3
  S3 -- "источники согласованы" --> E1
  S3 -- "конфликт → карантин (6б)" --> E1
```

## Инварианты

- Двойной ввод исключён: журнал проб — только 1С (FR-08.2, вариант A).
- Приоритет метки: лабораторный протокол > вердикт технолога (FR-11.1); конфликт → карантин (FR-11.2).
- True Positive / False Positive фиксируются автоматически из связки «прогноз → факт» (UC6).
