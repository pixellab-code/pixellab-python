from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any, Literal, Optional, TypedDict

import PIL.Image
import requests
from pydantic import BaseModel, Field, validate_call

from .models import Base64Image, ImageSize
from .types import CameraView, Detail, Direction, Outline, Shading

if TYPE_CHECKING:
    from .client import PixelLabClient


class GenerateImageBitForgeResponse(BaseModel):
    image: Base64Image


@validate_call(config=dict(arbitrary_types_allowed=True))
def generate_image_bitforge(
    client: Any,
    description: str = Field(
        ..., description="Text description of the image to generate"
    ),
    image_size: ImageSize = Field(..., description="Size of the generated image"),
    negative_description: str = Field(
        default="",
        description="Text description of what to avoid in the generated image",
    ),
    text_guidance_scale: float = Field(
        default=3.0,
        ge=1.0,
        le=20.0,
        description="How closely to follow the text description",
    ),
    extra_guidance_scale: float = Field(
        default=3.0,
        ge=0.0,
        le=20.0,
        description="How closely to follow the style reference",
    ),
    style_strength: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="Strength of the style transfer (0-100)",
    ),
    no_background: bool = Field(
        default=False, description="Generate with transparent background"
    ),
    seed: int = Field(default=0, description="Seed decides the starting noise"),
    outline: Optional[Outline] = Field(
        default=None, description="Outline style reference"
    ),
    shading: Optional[Shading] = Field(
        default=None, description="Shading style reference"
    ),
    detail: Optional[Detail] = Field(
        default=None, description="Detail style reference"
    ),
    view: Optional[CameraView] = Field(default=None, description="Camera view angle"),
    direction: Optional[Direction] = Field(
        default=None, description="Subject direction"
    ),
    isometric: bool = Field(default=False, description="Generate in isometric view"),
    oblique_projection: bool = Field(
        default=False, description="Generate in oblique projection"
    ),
    coverage_percentage: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=100.0,
        description="Percentage of the canvas to cover",
    ),
    init_image: Optional[PIL.Image.Image] = Field(
        default=None, description="Initial image to start from"
    ),
    init_image_strength: int = Field(
        default=0,
        ge=0,
        le=1000,
        description="Strength of the initial image influence",
    ),
    style_image: Optional[PIL.Image.Image] = Field(
        default=None, description="Reference image for style transfer"
    ),
    inpainting_image: Optional[PIL.Image.Image] = Field(
        default=None, description="Reference image which is inpainted"
    ),
    mask_image: Optional[PIL.Image.Image] = Field(
        default=None,
        description="Inpainting / mask image (black and white image, where the white is where the model should inpaint)",
    ),
    color_image: Optional[PIL.Image.Image] = Field(
        default=None,
        description="Forced color palette, 64x64 image containing colors used for palette",
    ),
) -> GenerateImageBitForgeResponse:
    init_image = Base64Image.from_pil_image(init_image) if init_image else None
    style_image = Base64Image.from_pil_image(style_image) if style_image else None
    inpainting_image = (
        Base64Image.from_pil_image(inpainting_image) if inpainting_image else None
    )
    mask_image = Base64Image.from_pil_image(mask_image) if mask_image else None
    color_image = Base64Image.from_pil_image(color_image) if color_image else None

    request_data = {
        "description": description,
        "negative_description": negative_description,
        "image_size": image_size.model_dump(),
        "text_guidance_scale": text_guidance_scale,
        "extra_guidance_scale": extra_guidance_scale,
        "style_strength": style_strength,
        "outline": outline,
        "shading": shading,
        "detail": detail,
        "view": view,
        "direction": direction,
        "isometric": isometric,
        "oblique_projection": oblique_projection,
        "no_background": no_background,
        "coverage_percentage": coverage_percentage,
        "init_image": init_image.model_dump() if init_image else None,
        "init_image_strength": init_image_strength,
        "style_image": style_image.model_dump() if style_image else None,
        "inpainting_image": inpainting_image.model_dump() if inpainting_image else None,
        "mask_image": mask_image.model_dump() if mask_image else None,
        "color_image": color_image.model_dump() if color_image else None,
        "seed": seed,
    }

    try:
        response = requests.post(
            f"{client.base_url}/generate-image-bitforge",
            headers=client.headers(),
            json=request_data,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            error_detail = response.json().get("detail", "Unknown error")
            raise ValueError(error_detail)
        elif response.status_code == 422:
            error_detail = response.json().get("detail", "Unknown error")
            raise ValueError(error_detail)
        raise

    return GenerateImageBitForgeResponse(**response.json())
