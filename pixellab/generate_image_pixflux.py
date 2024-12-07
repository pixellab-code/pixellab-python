from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Literal

import PIL.Image
import requests
from pydantic import BaseModel

from .models import Base64Image, ImageSize
from .types import CameraView, Detail, Direction, Outline, Shading

if TYPE_CHECKING:
    from .client import PixelLabClient

class Usage(BaseModel):
    type: Literal["usd"] = "usd"
    usd: float

class GenerateImagePixFluxResponse(BaseModel):
    image: Base64Image
    usage: Usage

def generate_image_pixflux(
    client: Any,
    description: str,
    image_size: ImageSize,
    negative_description: str = "",
    text_guidance_scale: float = 8,
    outline: Optional[Outline] = None,
    shading: Optional[Shading] = None,
    detail: Optional[Detail] = None,
    view: Optional[CameraView] = None,
    direction: Optional[Direction] = None,
    isometric: bool = False,
    no_background: bool = False,
    coverage_percentage: Optional[float] = None,
    init_image: Optional[PIL.Image.Image] = None,
    init_image_strength: int = 300,
    color_image: Optional[PIL.Image.Image] = None,
    seed: int = 0,
) -> GenerateImagePixFluxResponse:
    """Generate an image using PixFlux.

    Args:
        client: The PixelLab client instance
        description: Text description of the image to generate
        image_size: Size of the generated image
        negative_description: Text description of what to avoid in the generated image
        text_guidance_scale: How closely to follow the text description (1.0-20.0)
        outline: Outline style reference
        shading: Shading style reference
        detail: Detail style reference
        view: Camera view angle
        direction: Subject direction
        isometric: Generate in isometric view
        no_background: Generate with transparent background
        coverage_percentage: Percentage of the canvas to cover (0-100)
        init_image: Initial image to start from
        init_image_strength: Strength of the initial image influence (0-1000)
        color_image: Forced color palette
        seed: Seed for deterministic generation

    Returns:
        GenerateImagePixFluxResponse containing the generated image

    Raises:
        ValueError: If authentication fails or validation errors occur
        requests.exceptions.HTTPError: For other HTTP-related errors
    """
    init_image = Base64Image.from_pil_image(init_image) if init_image else None
    color_image = Base64Image.from_pil_image(color_image) if color_image else None

    request_data = {
        "description": description,
        "image_size": image_size,
        "negative_description": negative_description,
        "text_guidance_scale": text_guidance_scale,
        "outline": outline.model_dump() if outline else None,
        "shading": shading.model_dump() if shading else None,
        "detail": detail.model_dump() if detail else None,
        "view": view,
        "direction": direction,
        "isometric": isometric,
        "no_background": no_background,
        "coverage_percentage": coverage_percentage,
        "init_image": init_image.model_dump() if init_image else None,
        "init_image_strength": init_image_strength,
        "color_image": color_image.model_dump() if color_image else None,
        "seed": seed,
    }

    try:
        response = requests.post(
            f"{client.base_url}/generate-image-pixflux",
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

    return GenerateImagePixFluxResponse(**response.json())
