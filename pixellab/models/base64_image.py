from __future__ import annotations

from io import BytesIO
import base64
from typing import Literal
import PIL.Image
from pydantic import BaseModel


class Base64Image(BaseModel):
    type: Literal["base64"] = "base64"
    base64: str
    format: str = "png"

    def pil_image(self) -> PIL.Image:
        return PIL.Image.open(BytesIO(base64.b64decode(self.base64)))

    def _repr_png_(self):
        return self.pil_image()._repr_png_() 