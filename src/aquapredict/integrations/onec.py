"""Интеграция с «БИТ.Лаборатория» (1С): OData чтение / HTTP запись (FR-15, EPIC-01).

Плейсхолдер: реализации добавляются на этапе R0
(см. ``docs/system_analysis/plans/backlog_implementation_plan.md``).
"""

from __future__ import annotations

from typing import Any


class OneCClient:
    """Клиент обмена с 1С: чтение по OData, запись через HTTP-сервис."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def read_batches(self) -> list[dict[str, Any]]:
        """Чтение производственных партий (OData)."""

        raise NotImplementedError("OData: чтение партий (EPIC-01)")

    def read_lab_results(self) -> list[dict[str, Any]]:
        """Чтение утверждённых результатов испытаний (Ground Truth)."""

        raise NotImplementedError("OData: чтение результатов (EPIC-07)")

    def write_task(self, payload: dict[str, Any]) -> str:
        """Запись задачи (корректирующее действие / внеплановый отбор) через HTTP-сервис."""

        raise NotImplementedError("HTTP-сервис: запись задачи (EPIC-01)")
