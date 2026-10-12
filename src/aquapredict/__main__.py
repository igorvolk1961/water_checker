"""Точка входа: ``python -m aquapredict``."""

from __future__ import annotations

from aquapredict.config import get_settings


def main() -> int:
    settings = get_settings()
    print(f"AquaPredict запущен (env={settings.app_env}, log_level={settings.log_level})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
