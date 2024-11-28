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


def generate_rotation(
    client: Any,
    image_size: ImageSize,
    from_image: PIL.Image.Image,
    image_guidance_scale: float = 7.5,
    from_view: Optional[CameraView] = None,
    to_view: Optional[CameraView] = None,
    from_direction: Optional[Direction] = None,
    to_direction: Optional[Direction] = None,
    isometric: bool = False,
    oblique_projection: bool = False,
    init_image: Optional[PIL.Image.Image] = None,
    init_image_strength: int = 0,
    mask_image: Optional[PIL.Image.Image] = None,
    color_image: Optional[PIL.Image.Image] = None,
    seed: int = 0,
) -> GenerateRotationResponse:
    """Generate a rotated version of an image.

    Args:
        client: The PixelLab client instance
        image_size: Size of the generated image
        from_image: Reference image to rotate
        image_guidance_scale: How closely to follow the reference image (1.0-20.0)
        from_view: From camera view angle
        to_view: To camera view angle
        from_direction: From subject direction
        to_direction: To subject direction
        isometric: Generate in isometric view
        oblique_projection: Generate in oblique projection
        init_image: Initial image to start from
        init_image_strength: Strength of the initial image influence (0-1000)
        mask_image: Inpainting mask (black and white image, white is where to inpaint)
        color_image: Forced color palette (64x64 image containing colors)
        seed: Seed for deterministic generation

    Returns:
        GenerateRotationResponse containing the generated image

    Raises:
        ValueError: If authentication fails or validation errors occur
        requests.exceptions.HTTPError: For other HTTP-related errors
    """
    init_image = Base64Image.from_pil_image(init_image) if init_image else None
    mask_image = Base64Image.from_pil_image(mask_image) if mask_image else None
    from_image = Base64Image.from_pil_image(from_image)
    color_image = Base64Image.from_pil_image(color_image) if color_image else None

    request_data = {
        "image_size": image_size,
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
        print(response)
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
