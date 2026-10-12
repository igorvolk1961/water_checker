"""Интеграции: «БИТ.Лаборатория» (1С) и телеметрия линии."""

from __future__ import annotations

from aquapredict.integrations.onec import OneCClient
from aquapredict.integrations.telemetry import TelemetryReceiver

__all__ = ["OneCClient", "TelemetryReceiver"]
