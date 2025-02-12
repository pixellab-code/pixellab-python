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
    description: str,
    action: str,
    reference_image: PIL.Image.Image,
    view: CameraView = "side",
    direction: Direction = "east",
    negative_description: Optional[str] = None,
    text_guidance_scale: float = 7.5,
    image_guidance_scale: float = 1.5,
    n_frames: int = 4,
    start_frame_index: int = 0,
    init_images: Optional[list[Optional[PIL.Image.Image]]] = None,
    init_image_strength: float = 300,
    inpainting_images: Optional[list[Optional[PIL.Image.Image]]] = None,
    mask_images: Optional[list[Optional[PIL.Image.Image]]] = None,
    color_image: Optional[PIL.Image.Image] = None,
    seed: int = 0,
) -> AnimateWithTextResponse:
    """Generate an animation using text description.

    Args:
        client: The PixelLab client instance
        image_size: Image size
        description: Character description
        action: Action description
        reference_image: Reference image for style guidance
        view: Camera view angle
        direction: Subject direction
        negative_description: What not to generate
        text_guidance_scale: How closely to follow the text prompts (1.0-20.0)
        image_guidance_scale: How closely to follow the reference image (1.0-20.0)
        n_frames: Number of frames to generate (1-20)
        start_frame_index: Starting frame index
        init_images: Initial images to start from
        init_image_strength: Strength of the initial image influence (1-999)
        inpainting_images: Images for inpainting
        mask_images: Mask images for inpainting (white areas are inpainted)
        color_image: Forced color palette
        seed: Seed for deterministic generation (0 for random)

    Returns:
        AnimateWithTextResponse containing the generated images

    Raises:
        ValueError: If authentication fails or validation errors occur
        requests.exceptions.HTTPError: For other HTTP-related errors
    """
    reference_image = Base64Image.from_pil_image(reference_image)

    init_images = (
        [Base64Image.from_pil_image(img) if img else None for img in init_images]
        if init_images
        else None
    )

    inpainting_images = (
        [Base64Image.from_pil_image(img) if img else None for img in inpainting_images]
        if inpainting_images
        else [None] * 4
    )

    mask_images = (
        [Base64Image.from_pil_image(img) if img else None for img in mask_images]
        if mask_images
        else None
    )

    color_image = Base64Image.from_pil_image(color_image) if color_image else None

    request_data = {
        "image_size": image_size,
        "description": description,
        "action": action,
        "negative_description": negative_description,
        "text_guidance_scale": text_guidance_scale,
        "image_guidance_scale": image_guidance_scale,
        "n_frames": n_frames,
        "start_frame_index": start_frame_index,
        "view": view,
        "direction": direction,
        "reference_image": reference_image.model_dump(),
        "init_images": (
            [img.model_dump() if img else None for img in init_images]
            if init_images
            else None
        ),
        "init_image_strength": init_image_strength,
        "inpainting_images": [
            img.model_dump() if img else None for img in inpainting_images
        ],
        "mask_images": (
            [img.model_dump() if img else None for img in mask_images]
            if mask_images
            else None
        ),
        "color_image": color_image.model_dump() if color_image else None,
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
