# AquaPredict — предиктивная аналитика качества бутилированной воды

Учебный проект по системному анализу: модуль предиктивной аналитики качества воды на базе IoT и ML. Система анализирует потоковые данные датчиков линии розлива и заранее предупреждает о риске выхода параметров за нормы СанПиН, позволяя предотвратить брак.

**Позиционирование (вариант A):** AquaPredict — **аналитическая надстройка** над учётной системой «БИТ.Лаборатория» (1С), а не самостоятельная LIMS. Лабораторный контур (регистрация проб, результаты, протоколы, выгрузка во ФГИС) остаётся в 1С; AquaPredict добавляет телеметрию, риск-скоринг и предиктивные алерты и пишет задачи обратно в 1С.

## Архитектура (кратко)

- **Ввод:** телеметрия линии по OPC-UA/MQTT (TEL-01…TEL-13); партии/пробы/результаты — из «БИТ.Лаборатории» по OData.
- **Движок риск-скоринга:** двухслойный — Слой 1 (rule-based) и Слой 2 (ML); предиктивные алерты и инциденты.
- **Вывод:** задачи (КА, внеплановый отбор) и рекомендации — обратно в 1С через HTTP-сервис; веб-консоль технолога.
- **Принцип:** HITL («человек в контуре») — система рекомендует, решение принимает человек.

## Структура репозитория

```
docs/system_analysis/
  01_vision_and_scope.md            # Видение, границы (In/Out-of-Scope)
  02_glossary.md                    # Глоссарий терминов и метрик
  03_stakeholder_map.md             # Стейкхолдеры
  04_use_cases.md                   # UC1–UC8
  05_use_case_specification.md      # Детальная спецификация UC2
  06_domain_model.md                # Доменная модель + модель состояний
  07_nonfunctional_requirements.md  # NFR и guardrails
  08_data_requirements.md           # Требования к данным (ETL, разметка)
  09_assumptions_and_constraints.md # Допущения и ограничения
  10_cold_start_and_archival_data.md# Холодный старт и архивные данные
  kpi.md                            # KPI/метрики по слоям + Baseline
  business_case.md                  # Бизнес-кейс, ROI
  open_questions.md                 # Открытые вопросы и решения
  traceability.md                   # Трассируемость UC→FR→эпик→стоимость + LGL
  risks_register.md                 # Реестр проектных рисков
  assumptions_log.md                # Реестр допущений
  change_log.md                     # Журнал изменений базиса
  roadmap_and_plan.md               # Волны, ворота, RACI, DoR/DoD
  requirements/
    functional_requirements.md      # Функциональные требования FR-01…FR-16
    ui_requirements.md              # Требования к UI (SCR-01…SCR-12, ST-01…07)
    measured_parameters.md          # Измеряемые параметры TEL/LAB
  diagrams/
    bpmn_uc1…uc8*.md                # BPMN процессов
    sequence_*.md                   # Sequence-диаграммы
    state_*.md                      # Модели состояний
  legal/
    legal_risks_and_requirements.md # Юридические риски и требования (LGL)
  cost/
    cost_estimation.md              # Оценка стоимости (2 прохода)
  backlog/
    product_backlog.md              # Эпики и User Stories
  plans/
    plan_lead.md                    # План ведущего
    plan_colleague.md               # План коллеги (FR/UI/BPMN)
  reviews/                          # Переписка пары (ревью, вопросы/ответы)
```

## С чего начать чтение

1. `01_vision_and_scope.md` — зачем проект и что в границах.
2. `04_use_cases.md` → `05_use_case_specification.md` — сценарии.
3. `06_domain_model.md` — структура данных и состояния.
4. `07_nonfunctional_requirements.md`, `requirements/measured_parameters.md`, `kpi.md` — качество и параметры.
5. `requirements/functional_requirements.md` + `requirements/ui_requirements.md` + `diagrams/` — реализация требований.
6. `traceability.md`, `backlog/`, `cost/` — связность, план и экономика.
7. `legal/`, `open_questions.md`, `change_log.md` — право и управление.

## Ключевые артефакты

| Область | Артефакты |
| --- | --- |
| Требования | `requirements/functional_requirements.md`, `requirements/ui_requirements.md` |
| Данные и параметры | `requirements/measured_parameters.md`, `08_data_requirements.md`, `10_cold_start_and_archival_data.md` |
| Качество/метрики | `07_nonfunctional_requirements.md`, `kpi.md` |
| Диаграммы | `diagrams/` (BPMN, sequence, state) |
| Право | `legal/legal_risks_and_requirements.md` (LGL-01…14) |
| Экономика | `business_case.md`, `cost/cost_estimation.md` |
| Управление | `roadmap_and_plan.md`, `backlog/`, `plans/`, `traceability.md`, `change_log.md` |

## Статус ворот (Gate 0–4)

- **Gate 0** — базис заморожен (вариант A), правила приняты. ✅
- **Gate 1** — FR-скелет и карта экранов. ✅
- **Gate 2** — FR v1.1, UI v0.3, BPMN/sequence/state; решения по вопросам коллеги приняты. ✅
- **Gate 3** — FR/UI/BPMN заморожены, стоимость (проход 2 ≈ 8,5 млн ₽), матрица трассируемости и покрытия LGL. 🔄 идёт финализация (см. `reviews/2026-10-13_lead_to_colleague_request.md`).
- **Gate 4** — финальный чек-лист, пояснительная записка, защита. ⏳

## Роли и правила работы

- **Ведущий:** стоимость, право, бэклог, трассируемость, интеграция (`plans/plan_lead.md`).
- **Коллега:** функциональные требования, UI, диаграммы (`plans/plan_colleague.md`).
- **Термины** — строго по `02_glossary.md`.
- **Изменения базиса 01–10** — только через PR с ревью ведущего и записью в `change_log.md`.
- **Правило упаковки:** UC — источник истины; User Story — упаковка; Acceptance Criteria не дублируют UC.

## Открытые вопросы (к заказчику)

Актуальные вводные и принятые решения — в `open_questions.md` (OQ-01…OQ-06). Закрыто: сроки хранения данных — 1 год (LGL-06). Ожидает: SLA чтения партий, вид ЭП/подписант.

## Примечание

Документы содержат оценочные допущения (помечены как «допущение»/«пример») и подлежат подтверждению заказчиком. Материал учебного назначения; не является юридическим заключением или промышленной документацией.
