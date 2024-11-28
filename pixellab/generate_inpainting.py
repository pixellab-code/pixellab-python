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


def generate_inpainting(
    client: Any,
    description: str,
    image_size: ImageSize,
    inpainting_image: PIL.Image.Image,
    mask_image: PIL.Image.Image,
    negative_description: str = "",
    text_guidance_scale: float = 3.0,
    extra_guidance_scale: float = 1.0,
    outline: Optional[Outline] = None,
    shading: Optional[Shading] = None,
    detail: Optional[Detail] = None,
    view: Optional[CameraView] = None,
    direction: Optional[Direction] = None,
    isometric: bool = False,
    oblique_projection: bool = False,
    no_background: bool = False,
    init_image: Optional[PIL.Image.Image] = None,
    init_image_strength: int = 0,
    color_image: Optional[PIL.Image.Image] = None,
    seed: int = 0,
) -> GenerateInpaintingResponse:
    """Generate an inpainted image.

    Args:
        client: The PixelLab client instance
        description: Text description of the image to generate
        image_size: Size of the generated image
        inpainting_image: Reference image which is inpainted
        mask_image: Inpainting mask (black and white image, white is where to inpaint)
        negative_description: Text description of what to avoid in the generated image
        text_guidance_scale: How closely to follow the text description (1.0-20.0)
        extra_guidance_scale: How closely to follow the style reference (0.0-20.0)
        outline: Outline style reference
        shading: Shading style reference
        detail: Detail style reference
        view: Camera view angle
        direction: Subject direction
        isometric: Generate in isometric view
        oblique_projection: Generate in oblique projection
        no_background: Generate with transparent background
        init_image: Initial image to start from
        init_image_strength: Strength of the initial image influence (0-1000)
        color_image: Forced color palette (64x64 image containing colors)
        seed: Seed for deterministic generation

    Returns:
        GenerateInpaintingResponse containing the generated image

    Raises:
        ValueError: If authentication fails or validation errors occur
        requests.exceptions.HTTPError: For other HTTP-related errors
    """
    init_image = Base64Image.from_pil_image(init_image) if init_image else None
    inpainting_image = Base64Image.from_pil_image(inpainting_image)
    mask_image = Base64Image.from_pil_image(mask_image)
    color_image = Base64Image.from_pil_image(color_image) if color_image else None

    request_data = {
        "description": description,
        "image_size": image_size,
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
