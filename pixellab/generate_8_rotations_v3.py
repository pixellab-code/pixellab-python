from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

import PIL.Image
from pydantic import BaseModel

from ._common import Usage, post
from .models import Base64Image

if TYPE_CHECKING:
    from .client import PixelLabClient


class Generate8RotationsV3Response(BaseModel):
    background_job_id: str
    status: str = "processing"
    usage: Optional[Usage] = None


def generate_8_rotations_v3(
    client: Any,
    first_frame: PIL.Image.Image,
    no_background: Optional[bool] = None,
    seed: Optional[int] = 0,
) -> Generate8RotationsV3Response:
    """Generate 8 directional rotations of a character/object (v3, async).

    This endpoint runs asynchronously. The response contains a
    ``background_job_id``; poll it with ``client.wait_for_background_job(...)``
    to retrieve the generated rotations.

    Args:
        client: The PixelLab client instance
        first_frame: Reference frame to rotate
        no_background: Remove the background from generated frames
        seed: Seed for reproducible generation (default: 0)

    Returns:
        Generate8RotationsV3Response with the background job id and status
    """
    request_data: Dict[str, Any] = {
        "first_frame": Base64Image.from_pil_image(first_frame).model_dump(),
    }
    if no_background is not None:
        request_data["no_background"] = no_background
    if seed is not None:
        request_data["seed"] = seed

    return Generate8RotationsV3Response(
        **post(client, "generate-8-rotations-v3", request_data)
    )
