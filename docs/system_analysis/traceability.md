# AquaPredict LIMS — Матрица трассируемости (Traceability Matrix)

Интеграционный артефакт ведущего. Связывает варианты использования, функциональные требования (коллега), UI/BPMN, эпики бэклога, оценку стоимости и юридические требования. Заполняется по мере готовности артефактов (см. `roadmap_and_plan.md`, Gates 1–3).

## 1. Матрица

| UC / источник | FR (коллега) | UI / BPMN | Эпик | Стоимость | Юр-требование | Статус |
| --- | --- | --- | --- | --- | --- | --- |
| UC1 Регистрация партии | TBD | TBD | EPIC-01, EPIC-02 | TBD | — | 🟡 ожидает FR |
| UC2 Предиктивный алерт | TBD | TBD | EPIC-03, EPIC-04, EPIC-11 | TBD | LGL-04, LGL-09, LGL-10, LGL-11, LGL-14 | 🟡 ожидает FR |
| UC3 Корректирующее действие | TBD | TBD | EPIC-05 | TBD | LGL-04 | 🟡 ожидает FR |
| UC4 Внеплановый отбор | TBD | TBD | EPIC-06 | TBD | — | 🟡 ожидает FR |
| UC5 Протокол и ФГИС | TBD | TBD | EPIC-07 | TBD | LGL-01, LGL-02, LGL-07, LGL-11 | 🟡 ожидает FR |
| UC6 Валидация и разметка | TBD | TBD | EPIC-10 | TBD | LGL-03 | 🟡 ожидает FR |
| UC7 Cold Start | TBD | TBD | EPIC-08, EPIC-09 | TBD | — | 🟡 ожидает FR |
| NFR (07) | — | — | EPIC-11, EPIC-12 | TBD | LGL-03 | 🟢 базис готов |
| Legal (LGL-01…14) | TBD | TBD | EPIC-12 | TBD | — | 🟡 вход для FR |

Обозначения статуса: 🟢 готово, 🟡 в работе/ожидает, 🔴 конфликт.

## 2. Правила ведения

- Каждому FR присваивается ID (`FR-xx`), у каждой User Story — `US-xx`; они добавляются в столбцы.
- Строка считается «зелёной» только при заполненных FR, UI/BPMN и оценке стоимости.
- Расхождения (FR без UC, эпик без FR, юр-требование без реализации) фиксируются как 🔴 и выносятся на ревью ведущего (Gate 3).

## 3. Связь с другими артефактами

- Источники: `04_use_cases.md` (UC1–UC7), `07_nonfunctional_requirements.md` (NFR), `legal/legal_risks_and_requirements.md` (LGL).
- Цели: `backlog/product_backlog.md` (эпики), `cost/cost_estimation.md` (стоимость), будущие `requirements/functional_requirements.md`, `requirements/ui_requirements.md`, `diagrams/`.
