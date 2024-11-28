from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

import PIL.Image
import requests
from pydantic import BaseModel, Field, validate_call

from .models import Base64Image, ImageSize
from .types import CameraView, Direction

if TYPE_CHECKING:
    from .client import PixelLabClient


class GenerateRotationResponse(BaseModel):
    image: Base64Image


@validate_call(config=dict(arbitrary_types_allowed=True))
def generate_rotation(
    client: Any,
    image_size: ImageSize = Field(..., description="Size of the generated image"),
    from_image: PIL.Image.Image = Field(description="Reference image to rotate"),
    image_guidance_scale: float = Field(
        default=7.5,
        ge=1.0,
        le=20.0,
        description="How closely to follow the reference image",
    ),
    from_view: Optional[CameraView] = Field(
        default=None, description="From camera view angle"
    ),
    to_view: Optional[CameraView] = Field(
        default=None, description="To camera view angle"
    ),
    from_direction: Optional[Direction] = Field(
        default=None, description="From subject direction"
    ),
    to_direction: Optional[Direction] = Field(
        default=None, description="From subject direction"
    ),
    isometric: bool = Field(default=False, description="Generate in isometric view"),
    oblique_projection: bool = Field(
        default=False, description="Generate in oblique projection"
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
    mask_image: Optional[PIL.Image.Image] = Field(
        default=None,
        description="Inpainting / mask image (black and white image, where the white is where the model should inpaint)",
    ),
    color_image: Optional[PIL.Image.Image] = Field(
        default=None,
        description="Forced color palette, 64x64 image containing colors used for palette",
    ),
    seed: int = Field(default=0, description="Seed decides the starting noise"),
) -> GenerateRotationResponse:
    """Generate a rotated version of an image."""
    init_image = Base64Image.from_pil_image(init_image) if init_image else None
    mask_image = Base64Image.from_pil_image(mask_image) if mask_image else None
    from_image = Base64Image.from_pil_image(from_image)
    color_image = Base64Image.from_pil_image(color_image) if color_image else None

    request_data = {
        "image_size": image_size.model_dump(),
        "image_guidance_scale": image_guidance_scale,
        "from_view": from_view,
        "to_view": to_view,
        "from_direction": from_direction,
        "to_direction": to_direction,
        "isometric": isometric,
        "oblique_projection": oblique_projection,
        "init_image": init_image.model_dump() if init_image else None,
        "init_image_strength": init_image_strength,
        "mask_image": mask_image.model_dump() if mask_image else None,
        "from_image": from_image.model_dump(),
        "color_image": color_image.model_dump() if color_image else None,
        "seed": seed,
    }

    try:
        response = requests.post(
            f"{client.base_url}/generate-rotation",
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

    return GenerateRotationResponse(**response.json())
