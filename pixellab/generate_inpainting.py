from __future__ import annotations

from io import BytesIO
import base64
from typing import TYPE_CHECKING
import PIL.Image
import requests
from pydantic import BaseModel

if TYPE_CHECKING:
    from .client import PixelLabClient

class Base64Image(BaseModel):
    type: str = "base64"
    base64: str
    format: str = "png"

    def pil_image(self) -> PIL.Image:
        return PIL.Image.open(BytesIO(base64.b64decode(self.base64)))

    def _repr_png_(self):
        return self.pil_image()._repr_png_()


class GenerateInpaintingResponse(BaseModel):
    image: Base64Image

def generate_inpainting(
    client: PixelLabClient,
    prompt: str,
) -> GenerateInpaintingResponse:
    response = requests.post(
        f"{client.base_url}/generate-inpainting",
        headers=client.headers(),
        json=dict(prompt),
    )

    return GenerateInpaintingResponse(**response.json())
