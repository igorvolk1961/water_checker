# BPMN (визуальная версия) — UC5: Получение Ground Truth

**Версия:** 1.0 (визуализация `bpmn_uc5_ground_truth.md`; канонические BPMN 2.0/SVG — `diagrams/bpmn/uc5.*`). Термины — `02_glossary.md`.

```mermaid
flowchart TB
  classDef person fill:#e8f0fe,stroke:#1a73e8,color:#16262e
  classDef sys fill:#e2f1f2,stroke:#0e7c86,color:#16262e
  classDef onec fill:#f1f3f4,stroke:#5f6368,stroke-dasharray:4,color:#16262e
  classDef event fill:#fff8e1,stroke:#a3660a,color:#16262e
  classDef gw fill:#fdecea,stroke:#b03a2e,color:#16262e

  subgraph L1["Лабораторный контур (в 1С) — Out-of-Scope"]
    direction TB
    O1["Лаборант вносит результаты,<br/>протокол формируется"]:::onec
    O2["Утверждение протокола,<br/>ПЭП РЛ (LGL-02)"]:::onec
    O3["Выгрузка во ФГИС —<br/>штатный функционал 1С (LGL-01)"]:::onec
  end

  subgraph L2["Система AquaPredict"]
    direction TB
    S1["Периодическое чтение утверждённых<br/>результатов по OData<br/>(FR-08.1, ≤ 60 зап/мин NFR-6)"]:::sys
    S2["Информационная сверка<br/>со справочником нормативов<br/>(подсветка, LGL-11)"]:::sys
    S3["Сохранение Ground Truth<br/>с привязкой к партии/пробе;<br/>чтение статуса ФГИС и UUID (FR-09.3)"]:::sys
    S4["Связка «проба → срез 2 ч» →<br/>метка (приоритет: протокол)<br/>→ UC6"]:::sys
  end

  E0(("▶ Утверждённый протокол<br/>в 1С")):::event
  E1(("⏹ Ground Truth сохранён,<br/>пример в выборке (UC6)")):::event

  E0 --> O1 --> O2 --> O3
  O3 --> S1 --> S2 --> S3 --> S4 --> E1
```

## Инварианты

- AquaPredict не формирует, не подписывает и не выгружает протоколы (LGL-01/02/07 в редакции ведущего); неподписанные протоколы не отображаются как «отправляемые» (SCR-05).
- Сверка с нормативами — информационная; решение о несоответствии — в 1С (LGL-11).
