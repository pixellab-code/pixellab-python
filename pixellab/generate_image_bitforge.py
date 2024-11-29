from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any, Literal, Optional, TypedDict

import PIL.Image
import requests
from pydantic import BaseModel

from .models import Base64Image, ImageSize
from .types import CameraView, Detail, Direction, Outline, Shading

if TYPE_CHECKING:
    from .client import PixelLabClient

class GenerateImageBitForgeResponse(BaseModel):
    image: Base64Image

def generate_image_bitforge(
    client: Any,
    description: str,
    image_size: ImageSize,
    negative_description: str = "",
    text_guidance_scale: float = 3.0,
    extra_guidance_scale: float = 3.0,
    style_strength: float = 0.0,
    no_background: bool = False,
    seed: int = 0,
    outline: Optional[Outline] = None,
    shading: Optional[Shading] = None,
    detail: Optional[Detail] = None,
    view: Optional[CameraView] = None,
    direction: Optional[Direction] = None,
    isometric: bool = False,
    oblique_projection: bool = False,
    coverage_percentage: Optional[float] = None,
    init_image: Optional[PIL.Image.Image] = None,
    init_image_strength: int = 0,
    style_image: Optional[PIL.Image.Image] = None,
    inpainting_image: Optional[PIL.Image.Image] = None,
    mask_image: Optional[PIL.Image.Image] = None,
    color_image: Optional[PIL.Image.Image] = None,
) -> GenerateImageBitForgeResponse:
    """Generate an image using BitForge.

    Args:
        client: The PixelLab client instance
        description: Text description of the image to generate
        image_size: Size of the generated image
        negative_description: Text description of what to avoid in the generated image
        text_guidance_scale: How closely to follow the text description (1.0-20.0)
        extra_guidance_scale: How closely to follow the style reference (0.0-20.0)
        style_strength: Strength of the style transfer (0-100)
        no_background: Generate with transparent background
        seed: Seed for deterministic generation
        outline: Outline style reference (weakly guiding)
        shading: Shading style reference (weakly guiding)
        detail: Detail style reference (weakly guiding)
        view: Camera view angle (weakly guiding)
        direction: Subject direction (weakly guiding)
        isometric: Generate in isometric view (weakly guiding)
        oblique_projection: Generate in oblique projection (beta)
        coverage_percentage: Percentage of the canvas to cover (0-100) (weakly guiding)
        init_image: Initial image to start from
        init_image_strength: Strength of the initial image influence (0-1000)
        style_image: Reference image for style transfer
        inpainting_image: Reference image which is inpainted
        mask_image: Inpainting mask (black and white image, white is where to inpaint)
        color_image: Forced color palette

    Returns:
        GenerateImageBitForgeResponse containing the generated image

    Raises:
        ValueError: If authentication fails or validation errors occur
        requests.exceptions.HTTPError: For other HTTP-related errors
    """
    init_image = Base64Image.from_pil_image(init_image) if init_image else None
    style_image = Base64Image.from_pil_image(style_image) if style_image else None
    inpainting_image = (
        Base64Image.from_pil_image(inpainting_image) if inpainting_image else None
    )
    mask_image = Base64Image.from_pil_image(mask_image) if mask_image else None
    color_image = Base64Image.from_pil_image(color_image) if color_image else None

    request_data = {
        "description": description,
        "image_size": image_size,
        "negative_description": negative_description,
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
