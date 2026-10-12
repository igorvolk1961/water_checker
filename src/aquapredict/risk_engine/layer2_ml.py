"""Слой 2 риск-скоринга: ML-модель (FR-04, EPIC-09). Плейсхолдер."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MlRiskModel:
    """ML-модель прогноза риска с горизонтом ≥ 2 ч."""

    version: str = "0.0.0"

    def predict(self, features: dict[str, float]) -> float:
        """Возвращает риск-скор (0..1). Реализация — за ML-инженером (R2)."""

        raise NotImplementedError("Слой 2: обучение и инференс ML-модели (EPIC-09)")
