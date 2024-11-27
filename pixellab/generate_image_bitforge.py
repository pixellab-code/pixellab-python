from __future__ import annotations

from typing import TYPE_CHECKING, Optional
import requests
from pydantic import BaseModel, Field

from .models import Base64Image, ImageSize

if TYPE_CHECKING:
    from .client import PixelLabClient


class GenerateImageBitForgeRequest(BaseModel):
    description: str
    negative_description: str = ""
    image_size: ImageSize = ImageSize()
    text_guidance_scale: float = Field(default=3.0, ge=1.0, le=20.0)
    extra_guidance_scale: float = Field(default=3.0, ge=0.0, le=20.0)
    style_strength: float = Field(default=0.0, ge=0.0, le=100.0)
    no_background: bool = False
    seed: int = 0
    style_image: Optional[Base64Image] = None
    inpainting_image: Optional[Base64Image] = None
    mask_image: Optional[Base64Image] = None
    init_image: Optional[Base64Image] = None
    init_image_strength: int = Field(default=0, ge=0, le=1000)
    color_image: Optional[Base64Image] = None
    coverage_percentage: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    isometric: bool = False
    oblique_projection: bool = False


class GenerateImageBitForgeResponse(BaseModel):
    image: Base64Image


def generate_image_bitforge(
    client: PixelLabClient,
    description: str,
    negative_description: str = "",
    image_size: Optional[ImageSize] = None,
    text_guidance_scale: float = 3.0,
    extra_guidance_scale: float = 3.0,
    style_strength: float = 0.0,
    no_background: bool = False,
    seed: int = 0,
    style_image: Optional[Base64Image] = None,
    inpainting_image: Optional[Base64Image] = None,
    mask_image: Optional[Base64Image] = None,
    init_image: Optional[Base64Image] = None,
    init_image_strength: int = 0,
    color_image: Optional[Base64Image] = None,
    coverage_percentage: Optional[float] = None,
    isometric: bool = False,
    oblique_projection: bool = False,
) -> GenerateImageBitForgeResponse:
    request = GenerateImageBitForgeRequest(
        description=description,
        negative_description=negative_description,
        image_size=image_size or ImageSize(),
        text_guidance_scale=text_guidance_scale,
        extra_guidance_scale=extra_guidance_scale,
        style_strength=style_strength,
        no_background=no_background,
        seed=seed,
        style_image=style_image,
        inpainting_image=inpainting_image,
        mask_image=mask_image,
        init_image=init_image,
        init_image_strength=init_image_strength,
        color_image=color_image,
        coverage_percentage=coverage_percentage,
        isometric=isometric,
        oblique_projection=oblique_projection,
    )

    try:
        response = requests.post(
            f"{client.base_url}/generate-image-bitforge",
            headers=client.headers(),
            json=request.model_dump(),
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            error_detail = response.json().get('detail', 'Unknown error')
            raise ValueError(error_detail)
        raise

    return GenerateImageBitForgeResponse(**response.json())
