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


class Rotation8Images(BaseModel):
    south: Base64Image
    south_east: Base64Image
    east: Base64Image
    north_east: Base64Image
    north: Base64Image
    north_west: Base64Image
    west: Base64Image
    south_west: Base64Image


class Generate8RotationsResponse(BaseModel):
    images: Union[Rotation8Images, Dict[str, Base64Image]]
    usage: Usage
    
    @property
    def rotation_images(self) -> Rotation8Images:
        """Get images as Rotation8Images object for backwards compatibility"""
        if isinstance(self.images, dict):
            # Handle both hyphenated and underscore keys
            normalized_images = {}
            for key, value in self.images.items():
                normalized_key = key.replace("-", "_")
                normalized_images[normalized_key] = value
            return Rotation8Images(**normalized_images)
        return self.images


def rotate8_with_template(
    client: Any,
    description: str,
    image_size: Union[ImageSize, Dict[str, int]],
    text_guidance_scale: float = 8.0,
    reference: Optional[Dict[str, Any]] = None,
    view: str = "low top-down",
    outline: Optional[str] = None,
    shading: Optional[str] = None,
    detail: Optional[str] = None,
    isometric: bool = False,
    color_image: Optional[Union[Base64Image, Dict[str, str]]] = None,
    force_colors: bool = False,
    seed: Optional[int] = None,
    output_type: Literal["dict", "list"] = "dict",
    **kwargs
) -> Generate8RotationsResponse:
    """Generate character in 8 directions (cardinal + diagonals).

    Args:
        client: The PixelLab client instance
        description: Text description of the character to generate
        image_size: Size of each generated image
        text_guidance_scale: How closely to follow the text description (1.0-20.0)
        reference: Template or image reference for depth guidance
        view: Camera view angle (side, low top-down, high top-down)
        outline: Outline style (optional)
        shading: Shading style (optional)
        detail: Detail level (optional)
        isometric: Generate in isometric view
        color_image: Color palette reference image
        force_colors: Force the use of colors from color_image
        seed: Seed for deterministic generation
        output_type: Output format - "dict" or "list"

    Returns:
        Generate8RotationsResponse containing images for each direction

    Raises:
        ValueError: If authentication fails or validation errors occur
        requests.exceptions.HTTPError: For other HTTP-related errors
    """
    request_data = {
        "description": description,
        "image_size": image_size,
        "text_guidance_scale": text_guidance_scale,
        "view": view,
        "isometric": isometric,
        "force_colors": force_colors,
        "output_type": output_type,
        **kwargs
    }

    # Add optional parameters if provided
    if reference:
        request_data["reference"] = reference
    if outline:
        request_data["outline"] = outline
    if shading:
        request_data["shading"] = shading
    if detail:
        request_data["detail"] = detail
    if color_image:
        request_data["color_image"] = color_image
    if seed is not None:
        request_data["seed"] = seed

    try:
        response = requests.post(
            f"{client.base_url}/v2/rotate8-with-template",
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

    return Generate8RotationsResponse(**response.json())