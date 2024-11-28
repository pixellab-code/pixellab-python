from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

import PIL.Image
import requests
from pydantic import BaseModel, Field, validate_call

from .models import Base64Image, ImageSize, Keypoint
from .types import CameraView, Direction

if TYPE_CHECKING:
    from .client import PixelLabClient


class GenerateAnimationSkeletonResponse(BaseModel):
    images: list[Base64Image]


@validate_call(config=dict(arbitrary_types_allowed=True))
def generate_animation_skeleton(
    client: Any,
    image_size: ImageSize = Field(..., description="Size of the generated image"),
    skeleton_keypoints: list[list[Keypoint]] = Field(
        ..., description="Skeleton points"
    ),
    reference_guidance_scale: float = Field(
        default=1.1,
        ge=1.0,
        le=20.0,
        description="How closely to follow the text description",
    ),
    pose_guidance_scale: float = Field(
        default=3.0,
        ge=1.0,
        le=20.0,
        description="How closely to follow the style reference",
    ),
    view: Optional[CameraView] = Field(default=None, description="Camera view angle"),
    direction: Optional[Direction] = Field(
        default=None, description="Subject direction"
    ),
    isometric: bool = Field(default=False, description="Generate in isometric view"),
    oblique_projection: bool = Field(
        default=False, description="Generate in oblique projection"
    ),
    init_images: Optional[list[PIL.Image.Image]] = Field(
        default=None, description="Initial image to start from"
    ),
    init_image_strength: int = Field(
        default=0,
        ge=0,
        le=1000,
        description="Strength of the initial image influence",
    ),
    reference_image: Optional[PIL.Image.Image] = Field(
        default=None, description="Reference image"
    ),
    animation_images: Optional[list[Optional[PIL.Image.Image]]] = Field(
        default=None,
        description="Images used for showing the model with connected skeleton",
    ),
    mask_images: list[Optional[PIL.Image.Image]] = Field(
        default=None,
        description="Inpainting / mask image (black and white image, where the white is where the model should inpaint)",
    ),
    color_image: Optional[PIL.Image.Image] = Field(
        default=None,
        description="Forced color palette, 64x64 image containing colors used for palette",
    ),
    seed: int = Field(default=0, description="Seed decides the starting noise"),
) -> GenerateAnimationSkeletonResponse:
    """Generate an animation using skeleton points."""
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
        "image_size": image_size.model_dump(),
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
        "skeleton_keypoints": [
            [keypoint.model_dump() for keypoint in frame_keypoints]
            for frame_keypoints in skeleton_keypoints
        ],
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
