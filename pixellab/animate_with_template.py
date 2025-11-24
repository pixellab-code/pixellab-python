from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional, Union

import requests
from pydantic import BaseModel

from .models import Base64Image, ImageSize

if TYPE_CHECKING:
    from .client import PixelLabClient


class Usage(BaseModel):
    type: Literal["usd"] = "usd"
    usd: float


class GenerateAnimationResponse(BaseModel):
    images: List[Base64Image]
    frame_count: int
    spritesheet: Base64Image
    usage: Usage


def animate_with_template(
    client: Any,
    description: str,
    action: str = "walking",
    image_size: Union[ImageSize, Dict[str, int]] = None,
    n_frames: Optional[int] = None,
    text_guidance_scale: float = 8.0,
    view: str = "low top-down",
    direction: str = "south",
    reference: Optional[Dict[str, Any]] = None,
    outline: Optional[str] = None,
    shading: Optional[str] = None,
    detail: Optional[str] = None,
    isometric: bool = False,
    seed: int = 0,
    **kwargs
) -> GenerateAnimationResponse:
    """Generate animation sequence.

    Args:
        client: The PixelLab client instance
        description: Text description of the character to animate
        action: Action description (e.g., "walking", "running", "idle")
        image_size: Size of each frame
        n_frames: Number of frames to generate (2-12), None to use default or template frame count
        text_guidance_scale: How closely to follow the text description (1.0-20.0)
        view: Camera view angle (side, low top-down, high top-down)
        direction: Character direction (south, west, east, north)
        reference: Template or image reference for guidance
        outline: Outline style (optional)
        shading: Shading style (optional)
        detail: Detail level (optional)
        isometric: Generate in isometric view
        seed: Seed for deterministic generation

    Returns:
        GenerateAnimationResponse containing frames and optional spritesheet

    Raises:
        ValueError: If authentication fails or validation errors occur
        requests.exceptions.HTTPError: For other HTTP-related errors
    """
    if image_size is None:
        image_size = {"width": 64, "height": 64}

    request_data = {
        "description": description,
        "action_description": action,
        "image_size": image_size,
        "text_guidance_scale": text_guidance_scale,
        "view": view,
        "direction": direction,
        "isometric": isometric,
        "seed": seed,
        **kwargs
    }
    
    # Only add n_frames if it's not None
    if n_frames is not None:
        request_data["n_frames"] = n_frames

    # Add optional parameters if provided
    if reference:
        request_data["reference"] = reference
    if outline:
        request_data["outline"] = outline
    if shading:
        request_data["shading"] = shading
    if detail:
        request_data["detail"] = detail

    try:
        response = requests.post(
            f"{client.base_url}/v2/animate-with-template",
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

    return GenerateAnimationResponse(**response.json())