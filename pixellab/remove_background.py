from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Union

import PIL.Image
from pydantic import BaseModel

from ._common import Usage, post
from .models import Base64Image, ImageSize

if TYPE_CHECKING:
    from .client import PixelLabClient


class RemoveBackgroundResponse(BaseModel):
    image: Base64Image
    usage: Optional[Usage] = None


def remove_background(
    client: Any,
    image: PIL.Image.Image,
    image_size: Union[ImageSize, Dict[str, int]],
    background_removal_task: str = "remove_simple_background",
    text: Optional[str] = None,
    seed: Optional[int] = None,
) -> RemoveBackgroundResponse:
    """Remove the background from a pixel art image to create transparency.

    Args:
        client: The PixelLab client instance
        image: Source image whose background should be removed
        image_size: Size of the input image (width and height)
        background_removal_task: Background removal strategy
            (default: "remove_simple_background")
        text: Optional text hint describing the foreground subject
        seed: Seed for reproducible generation

    Returns:
        RemoveBackgroundResponse containing the image with the background removed
    """
    image_b64 = Base64Image.from_pil_image(image)

    request_data: Dict[str, Any] = {
        "image": image_b64.model_dump(),
        "image_size": image_size,
        "background_removal_task": background_removal_task,
    }
    if text is not None:
        request_data["text"] = text
    if seed is not None:
        request_data["seed"] = seed

    return RemoveBackgroundResponse(**post(client, "remove-background", request_data))
