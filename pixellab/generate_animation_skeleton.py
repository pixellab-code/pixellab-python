from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, TypedDict

import PIL.Image
import requests
from pydantic import BaseModel

from .models import Base64Image, ImageSize, Keypoint
from .types import CameraView, Direction

if TYPE_CHECKING:
    from .client import PixelLabClient


class SkeletonFrame(TypedDict):
    """A single frame of skeleton keypoints."""

    keypoints: list[Keypoint]


class GenerateAnimationSkeletonResponse(BaseModel):
    images: list[Base64Image]


def generate_animation_skeleton(
    client: Any,
    image_size: ImageSize,
    skeleton_keypoints: list[SkeletonFrame],
    view: CameraView,
    direction: Direction,
    reference_guidance_scale: float = 1.1,
    pose_guidance_scale: float = 3.0,
    isometric: bool = False,
    oblique_projection: bool = False,
    init_images: Optional[list[PIL.Image.Image]] = None,
    init_image_strength: int = 0,
    reference_image: Optional[PIL.Image.Image] = None,
    animation_images: Optional[list[Optional[PIL.Image.Image]]] = None,
    mask_images: Optional[list[Optional[PIL.Image.Image]]] = None,
    color_image: Optional[PIL.Image.Image] = None,
    seed: int = 0,
) -> GenerateAnimationSkeletonResponse:
    """Generate an animation using skeleton points.

    Args:
        client: The PixelLab client instance
        image_size: Size of the generated image
        skeleton_keypoints: List of frames, where each frame contains keypoints for the skeleton
        reference_guidance_scale: How closely to follow the text description (1.0-20.0)
        pose_guidance_scale: How closely to follow the style reference (1.0-20.0)
        view: Camera view angle
        direction: Subject direction
        isometric: Generate in isometric view
        oblique_projection: Generate in oblique projection
        init_images: Initial images to start from
        init_image_strength: Strength of the initial image influence (0-1000)
        reference_image: Reference image for style guidance
        animation_images: Images used for showing the model with connected skeleton
        mask_images: Inpainting masks (black and white images, where white is where to inpaint)
        color_image: Forced color palette
        seed: Seed for deterministic generation

    Returns:
        GenerateAnimationSkeletonResponse containing the generated images

    Raises:
        ValueError: If authentication fails or validation errors occur
        requests.exceptions.HTTPError: For other HTTP-related errors
    """
    init_images = (
        [Base64Image.from_pil_image(img) for img in init_images]
        if init_images
        else None
    )
    reference_image = (
        Base64Image.from_pil_image(reference_image) if reference_image else None
    )
    animation_images = (
        [Base64Image.from_pil_image(img) if img else None for img in animation_images]
        if animation_images
        else None
    )
    mask_images = (
        [Base64Image.from_pil_image(img) if img else None for img in mask_images]
        if mask_images
        else None
    )
    color_image = Base64Image.from_pil_image(color_image) if color_image else None

    request_data = {
        "image_size": image_size,
        "reference_guidance_scale": reference_guidance_scale,
        "pose_guidance_scale": pose_guidance_scale,
        "view": view,
        "direction": direction,
        "isometric": isometric,
        "oblique_projection": oblique_projection,
        "init_images": (
            [img.model_dump() for img in init_images] if init_images else None
        ),
        "init_image_strength": init_image_strength,
        "skeleton_keypoints": skeleton_keypoints,
        "reference_image": reference_image.model_dump() if reference_image else None,
        "animation_images": (
            [img.model_dump() if img else None for img in animation_images]
            if animation_images
            else None
        ),
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
            f"{client.base_url}/generate-animation-skeleton",
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

    return GenerateAnimationSkeletonResponse(**response.json())
