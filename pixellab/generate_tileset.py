from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Literal, Optional, Union

import requests
from pydantic import BaseModel

from .models import Base64Image, ImageSize

if TYPE_CHECKING:
    from .client import PixelLabClient


class Usage(BaseModel):
    type: Literal["usd"] = "usd"
    usd: float


class GenerateTilesetResponse(BaseModel):
    image: Base64Image
    usage: Usage


def generate_tileset(
    client: Any,
    inner_description: str,
    outer_description: str,
    image_size: Union[ImageSize, Dict[str, int]] = None,
    tile_size: Union[ImageSize, Dict[str, int]] = None,
    transition_description: Optional[str] = None,
    transition_size: float = 0.0,
    text_guidance_scale: float = 8.0,
    outline: Optional[str] = None,
    shading: Optional[str] = None,
    detail: Optional[str] = None,
    seed: int = 0,
    **kwargs
) -> GenerateTilesetResponse:
    """Generate seamless game tileset.

    Args:
        client: The PixelLab client instance
        inner_description: Description of the inner terrain/area (sent as lower_description to API)
        outer_description: Description of the outer terrain/area (sent as upper_description to API)
        image_size: Total size of the tileset image
        tile_size: Size of individual tiles
        transition_description: Description of transition area (optional)
        transition_size: Size of transition area (0-1)
        text_guidance_scale: How closely to follow the text description (1.0-20.0)
        outline: Outline style (optional)
        shading: Shading style (optional)
        detail: Detail level (optional)
        seed: Seed for deterministic generation

    Returns:
        GenerateTilesetResponse containing the tileset

    Raises:
        ValueError: If authentication fails or validation errors occur
        requests.exceptions.HTTPError: For other HTTP-related errors
    """
    if image_size is None:
        image_size = {"width": 128, "height": 128}
    if tile_size is None:
        tile_size = {"width": 16, "height": 16}

    request_data = {
        "lower_description": inner_description,
        "upper_description": outer_description,
        "tile_size": tile_size,
        "transition_size": transition_size,
        "text_guidance_scale": text_guidance_scale,
        "seed": seed,
        **kwargs
    }

    # Add optional parameters if provided
    if transition_description:
        request_data["transition_description"] = transition_description
    if outline:
        request_data["outline"] = outline
    if shading:
        request_data["shading"] = shading
    if detail:
        request_data["detail"] = detail

    try:
        response = requests.post(
            f"{client.base_url}/v2/create-tileset",
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

    return GenerateTilesetResponse(**response.json())