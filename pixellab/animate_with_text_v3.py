from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

import PIL.Image
from pydantic import BaseModel

from ._common import Usage, post
from .models import Base64Image

if TYPE_CHECKING:
    from .client import PixelLabClient


class AnimateWithTextV3Response(BaseModel):
    background_job_id: str
    status: str = "processing"
    usage: Optional[Usage] = None


def animate_with_text_v3(
    client: Any,
    first_frame: PIL.Image.Image,
    action: str,
    last_frame: Optional[PIL.Image.Image] = None,
    frame_count: int = 8,
    seed: Optional[int] = 0,
    no_background: Optional[bool] = None,
) -> AnimateWithTextV3Response:
    """Animate an image from a text action description (v3, async).

    This endpoint runs asynchronously. The response contains a
    ``background_job_id``; poll it with ``client.wait_for_background_job(...)``
    (or ``client.get_background_job(...)``) to retrieve the result.

    Args:
        client: The PixelLab client instance
        first_frame: Starting frame of the animation
        action: Text description of the action to animate
        last_frame: Optional ending frame to interpolate towards
        frame_count: Number of frames to generate (default: 8)
        seed: Seed for reproducible generation (default: 0)
        no_background: Remove the background from generated frames

    Returns:
        AnimateWithTextV3Response with the background job id and status
    """
    request_data: Dict[str, Any] = {
        "first_frame": Base64Image.from_pil_image(first_frame).model_dump(),
        "action": action,
        "frame_count": frame_count,
    }
    if last_frame is not None:
        request_data["last_frame"] = Base64Image.from_pil_image(last_frame).model_dump()
    if seed is not None:
        request_data["seed"] = seed
    if no_background is not None:
        request_data["no_background"] = no_background

    return AnimateWithTextV3Response(
        **post(client, "animate-with-text-v3", request_data)
    )
