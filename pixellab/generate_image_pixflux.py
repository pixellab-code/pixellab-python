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


class GenerateImagePixFluxResponse(BaseModel):
    image: Base64Image

def generate_image_pixflux(
    client: PixelLabClient,
    description: str,
) -> GenerateImagePixFluxResponse:
    response = requests.post(
        f"{client.base_url}/generate-image-pixflux",
        headers=client.headers(),
        json=dict(description=description),
    )
    
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            error_detail = response.json().get('detail', 'Unknown error')
            raise ValueError(error_detail)
        raise

    return GenerateImagePixFluxResponse(**response.json())
