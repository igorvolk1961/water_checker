"""Приём телеметрии OPC-UA/MQTT и буферизация (FR-02, EPIC-02).

Плейсхолдер: реализации добавляются на этапе R0.
"""

from __future__ import annotations

from collections.abc import Iterable


class TelemetryReceiver:
    """Приёмник показаний TEL-01…TEL-13."""

    def __init__(
        self,
        opcua_endpoint: str | None = None,
        mqtt_broker: str | None = None,
    ) -> None:
        self.opcua_endpoint = opcua_endpoint
        self.mqtt_broker = mqtt_broker

    def start(self) -> None:
        """Запуск приёма телеметрии."""

        raise NotImplementedError("Приёмник телеметрии (EPIC-02)")

    def recent(self, parameter: str) -> Iterable[float]:
        """Последние значения параметра."""

        raise NotImplementedError("Чтение последних значений (EPIC-02)")
