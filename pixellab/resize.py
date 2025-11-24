from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Literal, Optional, Union

import PIL.Image
import requests
from pydantic import BaseModel

from .models import Base64Image, ImageSize
from .types import Direction

if TYPE_CHECKING:
    from .client import PixelLabClient


class Usage(BaseModel):
    type: Literal["usd"] = "usd"
    usd: float


class ResizeResponse(BaseModel):
    image: Base64Image
    usage: Usage


def resize(
    client: Any,
    description: str,
    reference_image: PIL.Image.Image,
    reference_image_size: Union[ImageSize, Dict[str, int]],
    target_size: Union[ImageSize, Dict[str, int]],
    color_image: Optional[PIL.Image.Image] = None,
    direction: Optional[Direction] = None,
    init_image: Optional[PIL.Image.Image] = None,
    init_image_strength: int = 150,
    isometric: bool = False,
    no_background: bool = False,
    oblique_projection: bool = False,
    seed: Optional[int] = None,
) -> ResizeResponse:
    """Intelligently resize pixel art images while maintaining pixel art aesthetics.

    Args:
        client: The PixelLab client instance
        description: Text description of the character/object
        reference_image: Source image to resize
        reference_image_size: Size of the reference image
        target_size: Desired output size
        color_image: Forced color palette
        direction: Directional view (none, south, west, east, north, south-east, north-east, north-west, south-west)
        init_image: Initial image to start from
        init_image_strength: Strength of initial image influence (0-999)
        isometric: Apply isometric perspective
        no_background: Remove background
        oblique_projection: Apply oblique projection
        seed: Seed for reproducible generation

    Returns:
        ResizeResponse containing the resized image

    Raises:
        ValueError: If authentication fails, validation errors occur, or invalid image size constraints
        requests.exceptions.HTTPError: For other HTTP-related errors

    Best practices:
        - For best results, resize iteratively in small steps
        - Recommended: At most 50% decrease or 2x increase per resize
        - Example: 32x32 → 64x64 (2x) is good, 32x32 → 128x128 (4x) should be done in two steps
        - Minimum area 16x16 and maximum area 200x200 (both source and target)
    """
    reference_image_b64 = Base64Image.from_pil_image(reference_image)
    color_image_b64 = Base64Image.from_pil_image(color_image) if color_image else None
    init_image_b64 = Base64Image.from_pil_image(init_image) if init_image else None

    request_data = {
        "description": description,
        "reference_image": reference_image_b64.model_dump(),
        "reference_image_size": reference_image_size,
        "target_size": target_size,
        "isometric": isometric,
        "no_background": no_background,
        "oblique_projection": oblique_projection,
    }

    # Add optional parameters if provided
    if color_image_b64:
        request_data["color_image"] = color_image_b64.model_dump()
    if direction:
        request_data["direction"] = direction
    if init_image_b64:
        request_data["init_image"] = init_image_b64.model_dump()
        request_data["init_image_strength"] = init_image_strength
    if seed is not None:
        request_data["seed"] = seed

    try:
        response = requests.post(
            f"{client.base_url}/v2/resize",
            headers=client.headers(),
            json=request_data,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            error_detail = response.json().get("detail", "Unknown error")
            raise ValueError(error_detail)
        elif response.status_code == 401:
            error_detail = response.json().get("detail", "Unknown error")
            raise ValueError(error_detail)
        elif response.status_code == 403:
            error_detail = response.json().get("detail", "Unknown error")
            raise ValueError(error_detail)
        elif response.status_code == 422:
            error_detail = response.json().get("detail", "Unknown error")
            raise ValueError(error_detail)
        elif response.status_code >= 500:
            error_detail = response.json().get("detail", "Internal server error")
            raise ValueError(f"Server error: {error_detail}")
        raise

    return ResizeResponse(**response.json())
