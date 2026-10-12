# AquaPredict — предиктивная аналитика качества бутилированной воды

Учебный проект по системному анализу: модуль предиктивной аналитики качества воды на базе IoT и ML. Система анализирует потоковые данные датчиков линии розлива и заранее предупреждает о риске выхода параметров за нормы СанПиН, позволяя предотвратить брак.

**Позиционирование (вариант A):** AquaPredict — **аналитическая надстройка** над учётной системой «БИТ.Лаборатория» (1С), а не самостоятельная LIMS. Лабораторный контур (регистрация проб, результаты, протоколы, выгрузка во ФГИС) остаётся в 1С; AquaPredict добавляет телеметрию, риск-скоринг и предиктивные алерты и пишет задачи обратно в 1С.

## Архитектура (кратко)

- **Ввод:** телеметрия линии по OPC-UA/MQTT (TEL-01…TEL-13); партии/пробы/результаты — из «БИТ.Лаборатории» по OData.
- **Движок риск-скоринга:** двухслойный — Слой 1 (rule-based) и Слой 2 (ML); предиктивные алерты и инциденты.
- **Вывод:** задачи (КА, внеплановый отбор) и рекомендации — обратно в 1С через HTTP-сервис; веб-консоль технолога.
- **Принцип:** HITL («человек в контуре») — система рекомендует, решение принимает человек.

## Структура репозитория

- [docs/system_analysis/](docs/system_analysis/)
  - [01_vision_and_scope.md](docs/system_analysis/01_vision_and_scope.md) — видение, границы (In/Out-of-Scope)
  - [02_glossary.md](docs/system_analysis/02_glossary.md) — глоссарий терминов и метрик
  - [03_stakeholder_map.md](docs/system_analysis/03_stakeholder_map.md) — стейкхолдеры
  - [04_use_cases.md](docs/system_analysis/04_use_cases.md) — варианты использования UC1–UC8
  - [05_use_case_specification.md](docs/system_analysis/05_use_case_specification.md) — детальная спецификация UC2
  - [06_domain_model.md](docs/system_analysis/06_domain_model.md) — доменная модель + модель состояний
  - [07_nonfunctional_requirements.md](docs/system_analysis/07_nonfunctional_requirements.md) — NFR и guardrails
  - [08_data_requirements.md](docs/system_analysis/08_data_requirements.md) — требования к данным (ETL, разметка)
  - [09_assumptions_and_constraints.md](docs/system_analysis/09_assumptions_and_constraints.md) — допущения и ограничения
  - [10_cold_start_and_archival_data.md](docs/system_analysis/10_cold_start_and_archival_data.md) — холодный старт и архивные данные
  - [kpi.md](docs/system_analysis/kpi.md) — KPI/метрики по слоям + Baseline
  - [business_case.md](docs/system_analysis/business_case.md) — бизнес-кейс, ROI
  - [open_questions.md](docs/system_analysis/open_questions.md) — открытые вопросы и решения
  - [traceability.md](docs/system_analysis/traceability.md) — трассируемость UC→FR→эпик→стоимость + LGL
  - [risks_register.md](docs/system_analysis/risks_register.md) — реестр проектных рисков
  - [assumptions_log.md](docs/system_analysis/assumptions_log.md) — реестр допущений
  - [change_log.md](docs/system_analysis/change_log.md) — журнал изменений базиса
  - [roadmap_and_plan.md](docs/system_analysis/roadmap_and_plan.md) — волны, ворота, RACI, DoR/DoD
  - [requirements/](docs/system_analysis/requirements/)
    - [functional_requirements.md](docs/system_analysis/requirements/functional_requirements.md) — функциональные требования FR-01…FR-16
    - [ui_requirements.md](docs/system_analysis/requirements/ui_requirements.md) — требования к UI (SCR-01…SCR-12, ST-01…07)
    - [measured_parameters.md](docs/system_analysis/requirements/measured_parameters.md) — измеряемые параметры TEL/LAB
  - [diagrams/](docs/system_analysis/diagrams/)
    - [bpmn_uc1_party_telemetry.md](docs/system_analysis/diagrams/bpmn_uc1_party_telemetry.md)
    - [bpmn_uc2_prediction_alert.md](docs/system_analysis/diagrams/bpmn_uc2_prediction_alert.md)
    - [bpmn_uc3_corrective_action.md](docs/system_analysis/diagrams/bpmn_uc3_corrective_action.md)
    - [bpmn_uc4_trigger_sampling.md](docs/system_analysis/diagrams/bpmn_uc4_trigger_sampling.md)
    - [bpmn_uc5_ground_truth.md](docs/system_analysis/diagrams/bpmn_uc5_ground_truth.md)
    - [bpmn_uc6_retraining.md](docs/system_analysis/diagrams/bpmn_uc6_retraining.md)
    - [bpmn_uc7_cold_start.md](docs/system_analysis/diagrams/bpmn_uc7_cold_start.md)
    - [bpmn_uc8_telemetry_monitoring.md](docs/system_analysis/diagrams/bpmn_uc8_telemetry_monitoring.md)
    - [sequence_uc2_uc3_alert_to_ca.md](docs/system_analysis/diagrams/sequence_uc2_uc3_alert_to_ca.md)
    - [sequence_uc4_ground_truth.md](docs/system_analysis/diagrams/sequence_uc4_ground_truth.md)
    - [sequence_uc5_ground_truth.md](docs/system_analysis/diagrams/sequence_uc5_ground_truth.md)
    - [state_incident_alert_task.md](docs/system_analysis/diagrams/state_incident_alert_task.md)
    - [state_model_and_batch.md](docs/system_analysis/diagrams/state_model_and_batch.md)
  - [legal/](docs/system_analysis/legal/)
    - [legal_risks_and_requirements.md](docs/system_analysis/legal/legal_risks_and_requirements.md) — юридические риски и требования (LGL)
  - [cost/](docs/system_analysis/cost/)
    - [cost_estimation.md](docs/system_analysis/cost/cost_estimation.md) — оценка стоимости (2 прохода)
  - [backlog/](docs/system_analysis/backlog/)
    - [product_backlog.md](docs/system_analysis/backlog/product_backlog.md) — эпики и User Stories
  - [plans/](docs/system_analysis/plans/)
    - [plan_lead.md](docs/system_analysis/plans/plan_lead.md) — план ведущего
    - [plan_colleague.md](docs/system_analysis/plans/plan_colleague.md) — план коллеги (FR/UI/BPMN)
    - [backlog_implementation_plan.md](docs/system_analysis/plans/backlog_implementation_plan.md) — детальный план реализации бэклога (релизы R0–R3)
  - [reviews/](docs/system_analysis/reviews/) — переписка пары
    - [2026-10-12_colleague_to_lead.md](docs/system_analysis/reviews/2026-10-12_colleague_to_lead.md)
    - [2026-10-13_colleague_to_lead_gate2.md](docs/system_analysis/reviews/2026-10-13_colleague_to_lead_gate2.md)
    - [2026-10-13_colleague_to_lead_questions.md](docs/system_analysis/reviews/2026-10-13_colleague_to_lead_questions.md)
    - [2026-10-13_lead_to_colleague_answers.md](docs/system_analysis/reviews/2026-10-13_lead_to_colleague_answers.md)
    - [2026-10-13_lead_to_colleague_request.md](docs/system_analysis/reviews/2026-10-13_lead_to_colleague_request.md)

## С чего начать чтение

1. [01_vision_and_scope.md](docs/system_analysis/01_vision_and_scope.md) — зачем проект и что в границах.
2. [04_use_cases.md](docs/system_analysis/04_use_cases.md) → [05_use_case_specification.md](docs/system_analysis/05_use_case_specification.md) — сценарии.
3. [06_domain_model.md](docs/system_analysis/06_domain_model.md) — структура данных и состояния.
4. [07_nonfunctional_requirements.md](docs/system_analysis/07_nonfunctional_requirements.md), [measured_parameters.md](docs/system_analysis/requirements/measured_parameters.md), [kpi.md](docs/system_analysis/kpi.md) — качество и параметры.
5. [functional_requirements.md](docs/system_analysis/requirements/functional_requirements.md) + [ui_requirements.md](docs/system_analysis/requirements/ui_requirements.md) + [diagrams/](docs/system_analysis/diagrams/) — реализация требований.
6. [traceability.md](docs/system_analysis/traceability.md), [backlog/](docs/system_analysis/backlog/), [cost/](docs/system_analysis/cost/) — связность, план и экономика.
7. [legal/](docs/system_analysis/legal/), [open_questions.md](docs/system_analysis/open_questions.md), [change_log.md](docs/system_analysis/change_log.md) — право и управление.

## Ключевые артефакты

| Область | Артефакты |
| --- | --- |
| Требования | [functional_requirements.md](docs/system_analysis/requirements/functional_requirements.md), [ui_requirements.md](docs/system_analysis/requirements/ui_requirements.md) |
| Данные и параметры | [measured_parameters.md](docs/system_analysis/requirements/measured_parameters.md), [08_data_requirements.md](docs/system_analysis/08_data_requirements.md), [10_cold_start_and_archival_data.md](docs/system_analysis/10_cold_start_and_archival_data.md) |
| Качество/метрики | [07_nonfunctional_requirements.md](docs/system_analysis/07_nonfunctional_requirements.md), [kpi.md](docs/system_analysis/kpi.md) |
| Диаграммы | [diagrams/](docs/system_analysis/diagrams/) (BPMN, sequence, state) |
| Право | [legal_risks_and_requirements.md](docs/system_analysis/legal/legal_risks_and_requirements.md) (LGL-01…14) |
| Экономика | [business_case.md](docs/system_analysis/business_case.md), [cost_estimation.md](docs/system_analysis/cost/cost_estimation.md) |
| Управление | [roadmap_and_plan.md](docs/system_analysis/roadmap_and_plan.md), [backlog/](docs/system_analysis/backlog/), [plans/](docs/system_analysis/plans/), [traceability.md](docs/system_analysis/traceability.md), [change_log.md](docs/system_analysis/change_log.md) |

## Статус ворот (Gate 0–4)

- **Gate 0** — базис заморожен (вариант A), правила приняты. ✅
- **Gate 1** — FR-скелет и карта экранов. ✅
- **Gate 2** — FR v1.1, UI v0.3, BPMN/sequence/state; решения по вопросам коллеги приняты. ✅
- **Gate 3** — FR/UI/BPMN заморожены, стоимость (проход 2 ≈ 8,5 млн ₽), матрица трассируемости и покрытия LGL. 🔄 идёт финализация (см. [request](docs/system_analysis/reviews/2026-10-13_lead_to_colleague_request.md)).
- **Gate 4** — финальный чек-лист, пояснительная записка, защита. ⏳

## Роли и правила работы

- **Ведущий:** стоимость, право, бэклог, трассируемость, интеграция ([plan_lead.md](docs/system_analysis/plans/plan_lead.md)).
- **Коллега:** функциональные требования, UI, диаграммы ([plan_colleague.md](docs/system_analysis/plans/plan_colleague.md)).
- **Термины** — строго по [02_glossary.md](docs/system_analysis/02_glossary.md).
- **Изменения базиса 01–10** — только через PR с ревью ведущего и записью в [change_log.md](docs/system_analysis/change_log.md).
- **Правило упаковки:** UC — источник истины; User Story — упаковка; Acceptance Criteria не дублируют UC.

## Разработка (Python / uv)

Стандартный src-layout-проект; окружение и зависимости управляются через `uv` (метаданные — [pyproject.toml](pyproject.toml), lock — [uv.lock](uv.lock)).

- Установка окружения: `uv sync`
- Тесты: `uv run pytest`
- Линтер: `uv run ruff check .`
- Запуск приложения: `PYTHONPATH=src uv run python -m aquapredict` (пакет не устанавливается: `package = false`)
- Переменные окружения: скопируйте [.env.example](.env.example) в `.env`

Структура исходников:

- [src/aquapredict/](src/aquapredict/) — пакет
  - [config.py](src/aquapredict/config.py) — конфигурация
  - [domain/](src/aquapredict/domain/) — доменные модели ([models.py](src/aquapredict/domain/models.py))
  - [integrations/](src/aquapredict/integrations/) — «БИТ.Лаборатория» (OData/HTTP) и телеметрия (OPC-UA/MQTT)
  - [risk_engine/](src/aquapredict/risk_engine/) — Слой 1 (rules) и Слой 2 (ML)
  - [services/](src/aquapredict/services/), [api/](src/aquapredict/api/) — сервисы и HTTP-слой
- [tests/](tests/) — тесты (unit/integration)

## Открытые вопросы (к заказчику)

Актуальные вводные и принятые решения — в [open_questions.md](docs/system_analysis/open_questions.md) (OQ-01…OQ-06). Закрыто: сроки хранения данных — 1 год (LGL-06). Ожидает: SLA чтения партий, вид ЭП/подписант.

## Примечание

Документы содержат оценочные допущения (помечены как «допущение»/«пример») и подлежат подтверждению заказчиком. Материал учебного назначения; не является юридическим заключением или промышленной документацией.
