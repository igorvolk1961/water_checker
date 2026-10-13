"""Доменные модели и перечисления (см. ``docs/system_analysis/06_domain_model.md``)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class IncidentStatus(StrEnum):
    """Статусы предиктивного инцидента (FT-06.1)."""

    NEW = "Новый"
    CONFIRMED = "Подтверждён"
    FALSE_ALERT = "Ложный_алерт"
    CLOSED = "Закрыт"


class CAStatus(StrEnum):
    """Результат корректирующего действия (FR-06.5)."""

    DONE = "Выполнено"
    CANCELLED = "Отменено"


class Verdict(StrEnum):
    """Вердикт по инциденту — отдельная сущность (решение В-1)."""

    CONFIRMED = "Подтверждён"
    FALSE_POSITIVE = "Ложное_срабатывание"


class AlertSource(StrEnum):
    """Источник риск-оценки."""

    LAYER1 = "Слой 1"
    LAYER2 = "Слой 2"


@dataclass
class Batch:
    """Производственная партия."""

    id: str
    number: str


@dataclass
class Alert:
    """Уведомление о высоком риске (отдельно от инцидента)."""

    id: str
    batch_id: str
    parameter: str
    risk_score: float
    horizon_hours: int
    source: AlertSource = AlertSource.LAYER1


@dataclass
class Incident:
    """Предиктивный инцидент — учётная запись риска с задачей/вердиктом."""

    id: str
    batch_id: str
    parameter: str
    risk_score: float
    status: IncidentStatus = IncidentStatus.NEW


@dataclass
class CorrectiveAction:
    """Корректирующее действие (задача в «БИТ:LIMS»)."""

    id: str
    incident_id: str
    status: CAStatus = CAStatus.DONE


@dataclass
class IncidentVerdict:
    """Вердикт по инциденту: значение, причина, автор (аудируемая запись)."""

    incident_id: str
    value: Verdict
    reason: str | None = None
    author: str | None = None
