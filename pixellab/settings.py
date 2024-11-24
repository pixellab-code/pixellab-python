from __future__ import annotations

from pydantic_settings import BaseSettings


def settings(env_file: str | None = None):
    class Settings(
        BaseSettings, extra="ignore", env_file=env_file, env_prefix="PIXELLAB_"
    ):
        secret: str
        base_url: str | None = None

    return Settings()
