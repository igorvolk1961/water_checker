"""Слой 1 риск-скоринга: правило-ориентированный движок (FR-03, EPIC-03)."""

from __future__ import annotations

from dataclasses import dataclass

_COMPARATORS: dict[str, object] = {
    "<": lambda v, t: v < t,
    "<=": lambda v, t: v <= t,
    ">": lambda v, t: v > t,
    ">=": lambda v, t: v >= t,
}


@dataclass(frozen=True)
class Rule:
    """Правило телеметрии: параметр, условие, порог и рекомендованное действие."""

    name: str
    parameter: str
    operator: str
    threshold: float
    action: str


def evaluate_rules(rules: list[Rule], readings: dict[str, float]) -> list[Rule]:
    """Возвращает правила, сработавшие на текущем срезе телеметрии."""

    triggered: list[Rule] = []
    for rule in rules:
        if rule.parameter not in readings:
            continue
        comparator = _COMPARATORS.get(rule.operator)
        if comparator is None:
            raise ValueError(f"Неизвестный оператор правила: {rule.operator!r}")
        if comparator(readings[rule.parameter], rule.threshold):
            triggered.append(rule)
    return triggered
