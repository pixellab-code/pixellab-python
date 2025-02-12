from __future__ import annotations

from typing import Any, List, Literal, Optional

import PIL.Image
import requests
from pydantic import BaseModel

from .models import Base64Image, ImageSize
from .types import CameraView, Direction


class Usage(BaseModel):
    type: Literal["usd"] = "usd"
    usd: float


class AnimateWithTextResponse(BaseModel):
    images: list[Base64Image]
    usage: Usage


def animate_with_text(
    client: Any,
    image_size: ImageSize,
    character: str,
    action: str,
    view: CameraView,
    direction: Direction,
    selected_reference_image: PIL.Image.Image,
    negative_description: Optional[str] = None,
    text_guidance_scale: float = 7.5,
    image_guidance_scale: float = 1.5,
    n_frames: int = 4,
    start_frame_index: int = 0,
    movement_images: Optional[list[Optional[PIL.Image.Image]]] = None,
    inpainting_images: Optional[list[Optional[PIL.Image.Image]]] = None,
    init_images: Optional[list[Optional[PIL.Image.Image]]] = None,
    init_image_strength: int = 300,
    color_image: Optional[PIL.Image.Image] = None,
    output_method: str = "replace",
    seed: int = 0,
) -> AnimateWithTextResponse:
    """Generate an animation using text description.

    Args:
        client: The PixelLab client instance
        image_size: Size of the generated image
        character: Character description
        action: Action description
        view: Camera view angle
        direction: Subject direction
        selected_reference_image: Reference image for style guidance
        negative_description: What not to generate
        text_guidance_scale: How closely to follow the text prompts (1.0-20.0)
        image_guidance_scale: How closely to follow the reference image (1.0-20.0)
        n_frames: Number of frames to generate (1-8)
        start_frame_index: Starting frame index
        movement_images: Existing animation frames to guide generation
        inpainting_images: Images for inpainting
        init_images: Initial images to start from
        init_image_strength: Strength of the initial image influence (0-1000)
        color_image: Forced color palette
        output_method: How to handle inpainting output
        seed: Seed for deterministic generation

    Returns:
        AnimateWithTextResponse containing the generated images

    Raises:
        ValueError: If authentication fails or validation errors occur
        requests.exceptions.HTTPError: For other HTTP-related errors
    """
    selected_reference_image = Base64Image.from_pil_image(selected_reference_image)

    movement_images = (
        [Base64Image.from_pil_image(img) if img else None for img in movement_images]
        if movement_images
        else []
    )

    inpainting_images = (
        [Base64Image.from_pil_image(img) if img else None for img in inpainting_images]
        if inpainting_images
        else []
    )

    init_images = (
        [Base64Image.from_pil_image(img) if img else None for img in init_images]
        if init_images
        else []
    )

    color_image = (
        Base64Image.from_pil_image(color_image)
        if color_image
        else Base64Image(base64="")
    )

    request_data = {
        "image_size": image_size,
        "character": character,
        "action": action,
        "negative_description": negative_description,
        "text_guidance_scale": text_guidance_scale,
        "image_guidance_scale": image_guidance_scale,
        "n_frames": n_frames,
        "start_frame_index": start_frame_index,
        "view": view,
        "direction": direction,
        "selected_reference_image": selected_reference_image.model_dump(),
        "movement_images": [
            img.model_dump() if img else None for img in movement_images
        ],
        "inpainting_images": [
            img.model_dump() if img else None for img in inpainting_images
        ],
        "init_images": [img.model_dump() if img else None for img in init_images],
        "init_image_strength": init_image_strength,
        "color_image": color_image.model_dump(),
        "output_method": output_method,
        "seed": seed,
    }

    try:
        response = requests.post(
            f"{client.base_url}/animate-with-text",
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

    return AnimateWithTextResponse(**response.json())
