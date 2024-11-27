from __future__ import annotations

from io import BytesIO
import base64
from typing import TYPE_CHECKING, Optional, Literal
import PIL.Image
import requests
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from .client import PixelLabClient

class Base64Image(BaseModel):
    type: Literal["base64"] = "base64"
    base64: str
    format: str = "png"

    def pil_image(self) -> PIL.Image:
        return PIL.Image.open(BytesIO(base64.b64decode(self.base64)))

    def _repr_png_(self):
        return self.pil_image()._repr_png_()

class ImageSize(BaseModel):
    width: int = Field(default=128, ge=16, le=200)
    height: int = Field(default=128, ge=16, le=200)

class GenerateImagePixFluxRequest(BaseModel):
    description: str
    negative_description: str = ""
    image_size: ImageSize = ImageSize()
    text_guidance_scale: float = Field(default=3.0, ge=1.0, le=20.0)
    extra_guidance_scale: float = Field(default=3.0, ge=0.0, le=20.0)
    style_strength: float = Field(default=0.0, ge=0.0, le=100.0)
    no_background: bool = False
    seed: int = 0

class GenerateImagePixFluxResponse(BaseModel):
    image: Base64Image

def generate_image_pixflux(
    client: PixelLabClient,
    description: str,
    *,
    negative_description: str = "",
    image_size: Optional[ImageSize] = None,
    text_guidance_scale: float = 3.0,
    extra_guidance_scale: float = 3.0,
    style_strength: float = 0.0,
    no_background: bool = False,
    seed: int = 0,
) -> GenerateImagePixFluxResponse:
    request = GenerateImagePixFluxRequest(
        description=description,
        negative_description=negative_description,
        image_size=image_size or ImageSize(),
        text_guidance_scale=text_guidance_scale,
        extra_guidance_scale=extra_guidance_scale,
        style_strength=style_strength,
        no_background=no_background,
        seed=seed,
    )

    try:
        response = requests.post(
            f"{client.base_url}/generate-image-pixflux",
            headers=client.headers(),
            json=request.model_dump(),
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            error_detail = response.json().get('detail', 'Unknown error')
            raise ValueError(error_detail)
        raise

    return GenerateImagePixFluxResponse(**response.json())
