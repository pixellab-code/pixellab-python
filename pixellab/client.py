from __future__ import annotations

import json
from typing import Generator, List, Optional

import requests
from pydantic import BaseModel

from .settings import settings


class PixelLabClient(BaseModel):
    secret: str
    # base_url: str = "https://api.pixellab.ai/v1"
    base_url: str = "http://localhost:8000/v1"

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

    from .generate_animation_skeleton import generate_animation_skeleton
    from .generate_image_bitforge import generate_image_bitforge
    from .generate_image_pixflux import generate_image_pixflux
    from .generate_inpainting import generate_inpainting
    from .generate_rotation import generate_rotation
