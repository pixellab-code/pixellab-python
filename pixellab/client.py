from __future__ import annotations

import json
from typing import Generator, List, Optional

import requests
from pydantic import BaseModel
from .settings import settings


class PixelLabClient(BaseModel):
    secret: str
    base_url: str = "https://api.track.pixellab.io/external/v1"

    @classmethod
    def from_env(cls) -> PixelLabClient:
        return cls(**settings(env_file=None).model_dump(exclude_none=True))

    @classmethod
    def from_env_file(cls, env_file: str) -> PixelLabClient:
        return cls(**settings(env_file=env_file).model_dump(exclude_none=True))

    def auth_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token()}",
        }

    def headers(self):
        return {"Authorization": f"Bearer {self.secret}"}

    from .generate_image_v6 import generate_image_v6
