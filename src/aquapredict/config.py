"""Конфигурация приложения из переменных окружения (см. ``.env.example``)."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Настройки приложения."""

    app_env: str = os.getenv("APP_ENV", "dev")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    onec_base_url: str | None = os.getenv("ONEC_BASE_URL")
    onec_user: str | None = os.getenv("ONEC_USER")
    onec_password: str | None = os.getenv("ONEC_PASSWORD")
    opcua_endpoint: str | None = os.getenv("OPCUA_ENDPOINT")
    mqtt_broker: str | None = os.getenv("MQTT_BROKER")


def get_settings() -> Settings:
    """Возвращает экземпляр настроек."""

    return Settings()
