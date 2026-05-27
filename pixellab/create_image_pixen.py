from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from pydantic import BaseModel

from ._common import Usage, post
from .models import Base64Image, ImageSize
from .types import CameraView, Detail, Direction, Outline

if TYPE_CHECKING:
    from .client import PixelLabClient


class CreateImagePixenResponse(BaseModel):
    image: Base64Image
    usage: Optional[Usage] = None


def create_image_pixen(
    client: Any,
    description: str,
    image_size: Union[ImageSize, Dict[str, int]],
    outline: Optional[Outline] = None,
    detail: Optional[Detail] = "highly detailed",
    view: Optional[CameraView] = None,
    direction: Optional[Direction] = None,
    no_background: bool = False,
    background_removal_task: str = "remove_simple_background",
    seed: Optional[int] = None,
) -> CreateImagePixenResponse:
    """Generate a pixel art image using the Pixen model.

    Args:
        client: The PixelLab client instance
        description: What to generate
        image_size: Size of the generated image (width and height)
        outline: Outline style (optional)
        detail: Detail level (default: "highly detailed")
        view: Camera view (optional)
        direction: Facing direction of the subject (optional)
        no_background: Remove the background (default: False)
        background_removal_task: Background removal strategy when no_background
        seed: Seed for reproducible generation

    Returns:
        CreateImagePixenResponse containing the generated image and usage info
    """
    request_data: Dict[str, Any] = {
        "description": description,
        "image_size": image_size,
        "no_background": no_background,
        "background_removal_task": background_removal_task,
    }
    if outline is not None:
        request_data["outline"] = outline
    if detail is not None:
        request_data["detail"] = detail
    if view is not None:
        request_data["view"] = view
    if direction is not None:
        request_data["direction"] = direction
    if seed is not None:
        request_data["seed"] = seed

    return CreateImagePixenResponse(**post(client, "create-image-pixen", request_data))
