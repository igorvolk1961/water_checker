"""Дымовые тесты структуры и Слоя 1."""

from __future__ import annotations

from aquapredict import __version__
from aquapredict.risk_engine.layer1_rules import Rule, evaluate_rules


def test_version_defined() -> None:
    assert __version__


def test_rule_triggers_on_threshold() -> None:
    rules = [
        Rule(
            name="ozone_low",
            parameter="TEL-05",
            operator="<",
            threshold=0.2,
            action="Проверить озон",
        )
    ]
    triggered = evaluate_rules(rules, {"TEL-05": 0.1})
    assert [r.name for r in triggered] == ["ozone_low"]


def test_rule_not_triggered_when_missing_parameter() -> None:
    rules = [Rule(name="r", parameter="TEL-06", operator=">", threshold=1.0, action="x")]
    assert evaluate_rules(rules, {"TEL-05": 9.0}) == []
