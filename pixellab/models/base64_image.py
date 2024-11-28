from __future__ import annotations

import base64
from io import BytesIO
from typing import Literal

import PIL.Image
from pydantic import BaseModel


class Base64Image(BaseModel):
    type: Literal["base64"] = "base64"
    base64: str
    format: str = "png"

    @classmethod
    def from_pil_image(cls, image: PIL.Image) -> Base64Image:
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return cls(base64=img_str)

    def pil_image(self) -> PIL.Image:
        return PIL.Image.open(BytesIO(base64.b64decode(self.base64)))

    def _repr_png_(self):
        return self.pil_image()._repr_png_()
