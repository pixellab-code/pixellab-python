from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Literal, Optional, Union

import PIL.Image
import requests
from pydantic import BaseModel

from .models import Base64Image, ImageSize

if TYPE_CHECKING:
    from .client import PixelLabClient


class Usage(BaseModel):
    type: Literal["usd"] = "usd"
    usd: float


class ImageToPixelArtResponse(BaseModel):
    image: Base64Image
    usage: Usage


def image_to_pixelart(
    client: Any,
    image: PIL.Image.Image,
    image_size: Union[ImageSize, Dict[str, int]],
    output_size: Union[ImageSize, Dict[str, int]],
    text_guidance_scale: float = 8.0,
    seed: Optional[int] = None,
) -> ImageToPixelArtResponse:
    """Convert regular images to pixel art style.

    Args:
        client: The PixelLab client instance
        image: Source image to convert to pixel art
        image_size: Size of the input image
        output_size: Size of the output pixel art
        text_guidance_scale: How closely to follow pixel art style (1.0-20.0)
        seed: Seed for reproducible generation

    Returns:
        ImageToPixelArtResponse containing the converted pixel art image

    Raises:
        ValueError: If authentication fails, validation errors occur, or invalid image size constraints
        requests.exceptions.HTTPError: For other HTTP-related errors

    Best practices:
        - Input: Minimum 16x16, maximum 1280x1280
        - Output: Minimum 16x16, maximum 320x320
        - Recommended output size is 1/4 of the input size
    """
    image_b64 = Base64Image.from_pil_image(image)

    request_data = {
        "image": image_b64.model_dump(),
        "image_size": image_size,
        "output_size": output_size,
        "text_guidance_scale": text_guidance_scale,
    }

    if seed is not None:
        request_data["seed"] = seed

    try:
        response = requests.post(
            f"{client.base_url}/v2/image-to-pixelart",
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

    return ImageToPixelArtResponse(**response.json())
