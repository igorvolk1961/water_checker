# AquaPredict LIMS — Матрица трассируемости (Traceability Matrix)

Интеграционный артефакт ведущего. Связывает варианты использования, функциональные требования (коллега), UI/BPMN, эпики бэклога, оценку стоимости и юридические требования. Заполняется по мере готовности артефактов (см. `roadmap_and_plan.md`, Gates 1–3).

## 1. Матрица

| UC / источник | FR (коллега) | UI / BPMN | Эпик | Стоимость | Юр-требование | Статус |
| --- | --- | --- | --- | --- | --- | --- |
| UC1 Синхронизация партии | FR-01, FR-02, FR-15 | BPMN uc1 | EPIC-01, EPIC-02 | TBD | — | 🟢 FR |
| UC2 Предиктивный алерт | FR-03, FR-04, FR-05, FR-06, FR-12 | BPMN uc2; seq uc2/uc3; state | EPIC-03, EPIC-04, EPIC-11 | TBD | LGL-04, LGL-09, LGL-10, LGL-11, LGL-14 | 🟢 FR |
| UC3 Корректирующее действие | FR-06 | BPMN uc3; seq uc2/uc3; state | EPIC-05 | TBD | LGL-04 | 🟢 FR |
| UC4 Внеплановый отбор | FR-07, FR-08 | BPMN uc4; seq uc4 | EPIC-06 | TBD | — | 🟢 FR |
| UC5 Получение результатов (Ground Truth) | FR-08, FR-09, FR-15 | BPMN uc5; seq uc5 | EPIC-07 | TBD | LGL-01, LGL-02, LGL-07, LGL-11 | 🟢 FR |
| UC6 Валидация и разметка | FR-11, FR-12 | BPMN uc6; state | EPIC-10 | TBD | LGL-03 | 🟢 FR |
| UC7 Cold Start | FR-10, FR-04 | BPMN uc7 | EPIC-08, EPIC-09 | TBD | — | 🟢 FR |
| UC8 Мониторинг телеметрии (КИПиА) | FR-16 | BPMN uc8 (черновик) | EPIC-14, EPIC-02 | TBD | — | 🟢 FR |
| NFR (07) | — | — | EPIC-11, EPIC-12 | TBD | LGL-03 | 🟢 базис готов |
| Legal (LGL-01…14) | FR-09 (LGL-01/02/07), FR-06/08/14 (LGL-04/10/11), FR-14 (LGL-05/06), FR-04/11 (LGL-13) | §H чек-лист | EPIC-12 | TBD | — | 🟡 карта покрытия — Gate 3 |

Обозначения статуса: 🟢 готово, 🟡 в работе/ожидает, 🔴 конфликт.

## 2. Правила ведения

- Каждому FR присваивается ID (`FR-xx`), у каждой User Story — `US-xx`; они добавляются в столбцы.
- Строка считается «зелёной» только при заполненных FR, UI/BPMN и оценке стоимости.
- Расхождения (FR без UC, эпик без FR, юр-требование без реализации) фиксируются как 🔴 и выносятся на ревью ведущего (Gate 3).

## 3. Связь с другими артефактами

- Источники: `04_use_cases.md` (UC1–UC8), `07_nonfunctional_requirements.md` (NFR), `legal/legal_risks_and_requirements.md` (LGL), `requirements/measured_parameters.md` (TEL/LAB — параметры для KPI/FR/UI).
- Метрики: `kpi.md` (цели по слоям + Baseline) — данные экрана «Метрики модели» (I-10).
- Экономика: `business_case.md` (ROI), `cost/cost_estimation.md` (метод и оценка по эпикам).
- Цели: `backlog/product_backlog.md` (эпики), `cost/cost_estimation.md` (стоимость), будущие `requirements/functional_requirements.md`, `requirements/ui_requirements.md`, `diagrams/`.
