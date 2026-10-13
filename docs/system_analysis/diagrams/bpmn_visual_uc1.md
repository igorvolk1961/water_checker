# BPMN (визуальная версия) — UC1: Синхронизация партии

**Версия:** 1.0 (визуализация `bpmn_uc1_party_telemetry.md`; канонические BPMN 2.0/SVG — `diagrams/bpmn/uc1.*`). Термины — `02_glossary.md`.

```mermaid
flowchart TB
  classDef person fill:#e8f0fe,stroke:#1a73e8,color:#16262e
  classDef sys fill:#e2f1f2,stroke:#0e7c86,color:#16262e
  classDef onec fill:#f1f3f4,stroke:#5f6368,stroke-dasharray:4,color:#16262e
  classDef event fill:#fff8e1,stroke:#a3660a,color:#16262e
  classDef gw fill:#fdecea,stroke:#b03a2e,color:#16262e

  subgraph L1["БИТ LIMS (1С)"]
    direction TB
    O1["Регистрация партии<br/>(штатный процесс,<br/>номер — прослеживаемость)"]:::onec
    O2["Попытка закрытия партии"]:::onec
  end

  subgraph L2["Система AquaPredict"]
    direction TB
    S1["Чтение партии по OData<br/>(пакет, ≤ 60 зап/мин NFR-6)"]:::sys
    S2["Начало наблюдения:<br/>привязка телеметрии<br/>к партии (FR-01.2)"]:::sys
    S3["Контроль качества потока<br/>→ события для КИПиА (FR-16)"]:::sys
    G1{"есть инциденты<br/>вне [Закрыт]?"}:::gw
    S4["Статус в 1С:<br/>«закрытие блокировано<br/>до проверки инцидентов»"]:::sys
  end

  subgraph L3["Линия и IoT-шлюз"]
    direction TB
    W1["Телеметрия TEL-01…13<br/>≥ 1 изм/мин (OPC-UA/MQTT)<br/>буфер ≤ 2 ч (NFR-2)"]:::person
  end

  E0(("Новая партия в 1С")):::event
  E1(("Партия закрыта<br/>в 1С штатно")):::event
  E2(("Партия закрыта после<br/>проверки инцидентов")):::event

  E0 --> O1 --> S1 --> S2
  W1 --> S2
  S2 --> S3
  S3 -- "скоринг запущен (UC2)" --> E1
  O2 --> G1
  G1 -- "да" --> S4 --> S2
  G1 -- "нет" --> E1
```

## Инварианты

- Партии создаёт и закрывает только 1С (вариант A); система записывает лишь статус/комментарий блокировки (FR-15.2).
- Данные буфера досинхронизируются в исходном порядке без дублей (FR-01.3).
