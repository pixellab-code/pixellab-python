from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Optional, Union, Dict

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


class GenerateIsometricTileResponse(BaseModel):
    image: Base64Image
    usage: Usage


def generate_isometric_tile(
    client: Any,
    description: str,
    image_size: Union[ImageSize, Dict[str, int]],
    text_guidance_scale: float = 8,
    outline: Optional[Outline] = None,
    shading: Optional[Shading] = None,
    detail: Optional[Detail] = None,
    init_image: Optional[PIL.Image.Image] = None,
    init_image_strength: int = 300,
    isometric_tile_size: Optional[Literal[16, 32]] = 16,
    isometric_tile_shape: Literal["thick tile", "thin tile", "block", "reference shape"] = "thick tile",
    reference_shape: Optional[PIL.Image.Image] = None,
    reference_shape_strength: int = 300,
    color_image: Optional[PIL.Image.Image] = None,
    seed: int = 0,
) -> GenerateIsometricTileResponse:
    """Generate an isometric tile using PixelLab.

    Args:
        client: The PixelLab client instance
        description: Text description of the image to generate
        image_size: Size of the generated image (16x16 to 128x128)
        text_guidance_scale: How closely to follow the text description (1.0-20.0)
        outline: Outline style reference (weakly guiding)
        shading: Shading style reference (weakly guiding)
        detail: Detail style reference (weakly guiding)
        init_image: Initial image to start from
        init_image_strength: Strength of the initial image influence (1-999)
        isometric_tile_size: Size of the isometric tile (16 or 32)
        isometric_tile_shape: Shape of the isometric tile
        reference_shape: Reference image to use for the tile shape
        reference_shape_strength: Guidance strength for the reference shape (1-999)
        color_image: Forced color palette image
        seed: Seed for deterministic generation

    Returns:
        GenerateIsometricTileResponse containing the generated image

    Raises:
        ValueError: If authentication fails or validation errors occur
        requests.exceptions.HTTPError: For other HTTP-related errors
    """
    # Convert PIL images to Base64Image objects if provided
    init_image_b64 = Base64Image.from_pil_image(init_image) if init_image else None
    color_image_b64 = Base64Image.from_pil_image(color_image) if color_image else None
    reference_shape_b64 = Base64Image.from_pil_image(reference_shape) if reference_shape else None

    # Build request data - matches GenerateIsometricTileRequest model
    request_data = {
        "description": description,
        "image_size": image_size,
        "text_guidance_scale": text_guidance_scale,
        "init_image_strength": init_image_strength,
        "isometric_tile_size": isometric_tile_size,
        "isometric_tile_shape": isometric_tile_shape,
        "reference_shape_strength": reference_shape_strength,
        "seed": seed,
    }
    
    # Add optional parameters if provided
    if outline:
        request_data["outline"] = outline
    if shading:
        request_data["shading"] = shading
    if detail:
        request_data["detail"] = detail
    if init_image_b64:
        request_data["init_image"] = init_image_b64.model_dump()
    if color_image_b64:
        request_data["color_image"] = color_image_b64.model_dump()
    if reference_shape_b64:
        request_data["reference_shape"] = reference_shape_b64.model_dump()

    try:
        response = requests.post(
            f"{client.base_url}/v2/create-isometric-tile",
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

    return GenerateIsometricTileResponse(**response.json())
