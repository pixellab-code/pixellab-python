from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

import PIL.Image
import requests
from pydantic import BaseModel

from .models import Base64Image, ImageSize
from .types import CameraView, Direction, Literal

if TYPE_CHECKING:
    from .client import PixelLabClient


class Usage(BaseModel):
    type: Literal["usd"] = "usd"
    usd: float


class Keypoint(BaseModel):
    x: float
    y: float
    label: str
    z_index: int


class EstimateSkeletonResponse(BaseModel):
    keypoints: List[Keypoint]
    usage: Usage


def estimate_skeleton(
    client: Any,
    image: PIL.Image.Image,
) -> EstimateSkeletonResponse:
    """Estimate the skeleton of an image.

    Args:
        client: The PixelLab client instance
        image: An image of the character on a transparent background, to estimate the skeleton for.

    Returns:
        A list of keypoints.

    Raises:
        ValueError: If authentication fails or validation errors occur
        requests.exceptions.HTTPError: For other HTTP-related errors
    """
    image = Base64Image.from_pil_image(image)

    request_data = {
        "image": image.model_dump(),
    }

    try:
        response = requests.post(
            f"{client.base_url}/estimate-skeleton",
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
        elif response.status_code == 422:
            error_detail = response.json().get("detail", "Unknown error")
            raise ValueError(error_detail)
        raise

    return EstimateSkeletonResponse(**response.json())
