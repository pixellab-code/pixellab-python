from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

import PIL.Image
import requests
from pydantic import BaseModel, Field, validate_call

from .models import Base64Image, ImageSize
from .types import CameraView, Detail, Direction, Outline, Shading

if TYPE_CHECKING:
    from .client import PixelLabClient


class GenerateInpaintingResponse(BaseModel):
    image: Base64Image


@validate_call(config=dict(arbitrary_types_allowed=True))
def generate_inpainting(
    client: Any,
    description: str = Field(
        ..., description="Text description of the image to generate"
    ),
    image_size: ImageSize = Field(..., description="Size of the generated image"),
    inpainting_image: PIL.Image.Image = Field(
        description="Reference image which is inpainted"
    ),
    mask_image: PIL.Image.Image = Field(
        description="Inpainting / mask image (black and white image, where the white is where the model should inpaint)"
    ),
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
        default=1.0,
        ge=0.0,
        le=20.0,
        description="How closely to follow the style reference",
    ),
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
    no_background: bool = Field(
        default=False, description="Generate with transparent background"
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
    color_image: Optional[PIL.Image.Image] = Field(
        default=None,
        description="Forced color palette, 64x64 image containing colors used for palette",
    ),
    seed: int = Field(default=0, description="Seed decides the starting noise"),
) -> GenerateInpaintingResponse:
    """Generate an inpainted image."""
    init_image = Base64Image.from_pil_image(init_image) if init_image else None
    inpainting_image = Base64Image.from_pil_image(inpainting_image)
    mask_image = Base64Image.from_pil_image(mask_image)
    color_image = Base64Image.from_pil_image(color_image) if color_image else None

    request_data = {
        "description": description,
        "image_size": image_size.model_dump(),
        "negative_description": negative_description,
        "text_guidance_scale": text_guidance_scale,
        "extra_guidance_scale": extra_guidance_scale,
        "outline": outline,
        "shading": shading,
        "detail": detail,
        "view": view,
        "direction": direction,
        "isometric": isometric,
        "oblique_projection": oblique_projection,
        "no_background": no_background,
        "init_image": init_image.model_dump() if init_image else None,
        "init_image_strength": init_image_strength,
        "inpainting_image": inpainting_image.model_dump(),
        "mask_image": mask_image.model_dump(),
        "color_image": color_image.model_dump() if color_image else None,
        "seed": seed,
    }

    try:
        response = requests.post(
            f"{client.base_url}/generate-inpainting",
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

    return GenerateInpaintingResponse(**response.json())
