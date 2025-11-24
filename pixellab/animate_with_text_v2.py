from __future__ import annotations

from typing import Any, Literal, Optional

import PIL.Image
import requests
from pydantic import BaseModel

from .models import Base64Image, ImageSize


class Usage(BaseModel):
    type: Literal["usd"] = "usd"
    usd: float


class AnimateWithTextV2Response(BaseModel):
    images: list[Base64Image]
    image: Optional[Base64Image] = None
    usage: Usage


def animate_with_text_v2(
    client: Any,
    reference_image: PIL.Image.Image,
    reference_image_size: ImageSize,
    action: str,
    image_size: ImageSize,
    seed: Optional[int] = None,
    no_background: Optional[bool] = True,
) -> AnimateWithTextV2Response:
    """Generate pixel art animation from text description using Gemini AI.

    This endpoint uses Google's Gemini 3 Pro Image model to create smooth animations
    from a reference image and action description.

    Args:
        client: The PixelLab client instance
        reference_image: Reference image (character/object to animate) as PIL Image
        reference_image_size: Size of the reference image
        action: Action description (e.g., 'walk', 'jump', 'attack')
        image_size: Size of each animation frame
        seed: Seed for reproducible generation (0 for random)
        no_background: Remove background from generated frames

    Returns:
        AnimateWithTextV2Response containing the generated animation frames

    Raises:
        ValueError: If authentication fails or validation errors occur
        requests.exceptions.HTTPError: For other HTTP-related errors

    Example:
        ```python
        import pixellab
        import PIL.Image

        client = pixellab.Client(secret="YOUR_API_TOKEN")
        reference_image = PIL.Image.open("character.png")

        response = client.animate_with_text_v2(
            reference_image=reference_image,
            reference_image_size={"width": 64, "height": 64},
            action="walk",
            image_size={"width": 64, "height": 64}
        )

        # Access individual frames
        for i, frame in enumerate(response.images):
            frame.pil_image().save(f"frame_{i}.png")
        ```
    """
    # Convert reference image to Base64Image
    reference_image_b64 = Base64Image.from_pil_image(reference_image)

    request_data = {
        "reference_image": reference_image_b64.model_dump(),
        "reference_image_size": reference_image_size,
        "action": action,
        "image_size": image_size,
        "seed": seed,
        "no_background": no_background,
    }

    try:
        response = requests.post(
            f"{client.base_url}/v2/animate-with-text-v2",
            headers=client.headers(),
            json=request_data,
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            error_detail = response.json().get("detail", "Bad request")
            raise ValueError(f"Bad request: {error_detail}")
        elif response.status_code == 401:
            error_detail = response.json().get("detail", "Unauthorized")
            raise ValueError(f"Authentication failed: {error_detail}")
        elif response.status_code == 402:
            error_detail = response.json().get("detail", "Insufficient credits")
            raise ValueError(f"Payment required: {error_detail}")
        elif response.status_code == 422:
            error_detail = response.json().get("detail", "Validation error")
            raise ValueError(f"Validation error: {error_detail}")
        elif response.status_code == 429:
            error_detail = response.json().get("detail", "Too many requests")
            raise ValueError(f"Rate limit exceeded: {error_detail}")
        raise

    return AnimateWithTextV2Response(**response.json())
