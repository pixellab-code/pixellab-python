"""Object / map-object management endpoints (v2).

The create/animate/state endpoints are asynchronous and return a
``background_job_id`` (plus ``object_id``). Poll with
``client.wait_for_background_job(job_id)`` and fetch the result with
``client.get_object(object_id)``.
"""

from __future__ import annotations

import base64
from io import BytesIO
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

import PIL.Image
from pydantic import BaseModel, ConfigDict

from ._common import Usage, delete as _delete, get as _get, patch as _patch, post as _post
from .models import Base64Image, ImageSize

if TYPE_CHECKING:
    from .client import PixelLabClient


def _img(image: Optional[PIL.Image.Image]) -> Optional[Dict[str, Any]]:
    return Base64Image.from_pil_image(image).model_dump() if image is not None else None


def _style_reference(image: PIL.Image.Image) -> Dict[str, Any]:
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return {
        "type": "base64",
        "base64": base64.b64encode(buffered.getvalue()).decode(),
        "format": "png",
    }


class ObjectJobResponse(BaseModel):
    background_job_id: str
    object_id: str
    status: str = "queued"
    usage: Optional[Usage] = None


class Create1DirectionObjectResponse(ObjectJobResponse):
    n_frames: int


class DirectionSubmission(BaseModel):
    model_config = ConfigDict(extra="allow")

    direction: str
    status: str
    background_job_id: Optional[str] = None
    animation_id: Optional[str] = None


class AnimateObjectResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    object_id: str
    animation_group_id: str
    mode: str
    frame_count: int
    description: str
    display_name: Optional[str] = None
    submissions: List[DirectionSubmission] = []
    usage: Optional[Usage] = None

    @property
    def background_job_ids(self) -> List[str]:
        """Background job ids across all per-direction submissions."""
        return [s.background_job_id for s in self.submissions if s.background_job_id]


class DismissReviewResponse(BaseModel):
    usage: Optional[Usage] = None


class SelectObjectFramesResponse(BaseModel):
    created_object_ids: List[str]
    usage: Optional[Usage] = None


class ObjectSummary(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    prompt: str
    size: Dict[str, int]
    directions: int
    created_at: str
    name: Optional[str] = None
    view: Optional[str] = None
    preview_url: Optional[str] = None
    tags: List[str] = []
    status: Optional[str] = None


class ObjectsListResponse(BaseModel):
    objects: List[ObjectSummary]
    total: int
    usage: Optional[Usage] = None


class ObjectDetail(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    prompt: str
    size: Dict[str, int]
    directions: int
    created_at: str
    rotation_urls: Dict[str, Any]
    name: Optional[str] = None
    view: Optional[str] = None
    tags: List[str] = []
    status: Optional[str] = None


def create_1_direction_object(
    client: Any,
    description: str,
    size: Optional[int] = None,
    view: str = "top-down",
    style_images: Optional[List[PIL.Image.Image]] = None,
    item_descriptions: Optional[List[str]] = None,
) -> Create1DirectionObjectResponse:
    """Create a single-direction object, optionally with multiple items (async)."""
    request_data: Dict[str, Any] = {
        "description": description,
        "view": view,
        "style_images": [_style_reference(img) for img in (style_images or [])],
    }
    if size is not None:
        request_data["size"] = size
    if item_descriptions is not None:
        request_data["item_descriptions"] = item_descriptions

    return Create1DirectionObjectResponse(
        **_post(client, "create-1-direction-object", request_data)
    )


def create_8_direction_object(
    client: Any,
    description: str,
    size: Optional[int] = None,
    view: str = "low top-down",
    reference_image: Optional[PIL.Image.Image] = None,
    style_image: Optional[PIL.Image.Image] = None,
) -> ObjectJobResponse:
    """Create an 8-direction object (async)."""
    request_data: Dict[str, Any] = {"description": description, "view": view}
    for key, value in {
        "size": size,
        "reference_image": _img(reference_image),
        "style_image": _img(style_image),
    }.items():
        if value is not None:
            request_data[key] = value

    return ObjectJobResponse(**_post(client, "create-8-direction-object", request_data))


def create_map_object(
    client: Any,
    description: str,
    image_size: Union[ImageSize, Dict[str, int]],
    view: str = "high top-down",
    outline: Optional[str] = None,
    shading: Optional[str] = None,
    detail: Optional[str] = None,
    text_guidance_scale: float = 8.0,
    init_image: Optional[PIL.Image.Image] = None,
    init_image_strength: int = 300,
    color_image: Optional[PIL.Image.Image] = None,
    background_image: Optional[PIL.Image.Image] = None,
    inpainting: Optional[Dict[str, Any]] = None,
    seed: Optional[int] = None,
) -> ObjectJobResponse:
    """Generate a transparent map object for game maps (async)."""
    request_data: Dict[str, Any] = {
        "description": description,
        "image_size": image_size,
        "view": view,
        "text_guidance_scale": text_guidance_scale,
        "init_image_strength": init_image_strength,
    }
    for key, value in {
        "outline": outline,
        "shading": shading,
        "detail": detail,
        "init_image": _img(init_image),
        "color_image": _img(color_image),
        "background_image": _img(background_image),
        "inpainting": inpainting,
        "seed": seed,
    }.items():
        if value is not None:
            request_data[key] = value

    return ObjectJobResponse(**_post(client, "map-objects", request_data))


def animate_object(
    client: Any,
    object_id: str,
    animation_description: Optional[str] = None,
    directions: Optional[List[str]] = None,
    mode: str = "v3",
    frame_count: Optional[int] = None,
    display_name: Optional[str] = None,
    animation_group_id: Optional[str] = None,
    replace_existing: bool = False,
) -> AnimateObjectResponse:
    """Add an animation to an existing object (async).

    One background job is submitted per direction; inspect
    ``response.submissions`` (or ``response.background_job_ids``) and poll each
    with ``client.wait_for_background_job(job_id)``.

    Args:
        client: The PixelLab client instance
        object_id: Id of the object to animate
        animation_description: Text describing the animation (e.g. "opening")
        directions: Directions to animate (defaults to all on the server)
        mode: Animation mode (default: "v3")
        frame_count: Number of frames per animation
        display_name: Human-readable name for the animation
        animation_group_id: Reuse an existing animation group id
        replace_existing: Replace an existing animation in the group
    """
    request_data: Dict[str, Any] = {"mode": mode, "replace_existing": replace_existing}
    for key, value in {
        "animation_description": animation_description,
        "directions": directions,
        "frame_count": frame_count,
        "display_name": display_name,
        "animation_group_id": animation_group_id,
    }.items():
        if value is not None:
            request_data[key] = value

    return AnimateObjectResponse(
        **_post(client, f"objects/{object_id}/animations", request_data)
    )


def create_object_state(
    client: Any,
    object_id: str,
    edit_description: str,
    seed: Optional[int] = None,
) -> ObjectJobResponse:
    """Apply a text edit to an object, producing a new state (async)."""
    request_data: Dict[str, Any] = {"edit_description": edit_description}
    if seed is not None:
        request_data["seed"] = seed
    return ObjectJobResponse(**_post(client, f"objects/{object_id}/states", request_data))


def dismiss_object_review(client: Any, object_id: str) -> DismissReviewResponse:
    """Dismiss a review object without saving any frames."""
    return DismissReviewResponse(
        **_post(client, f"objects/{object_id}/dismiss-review", {})
    )


def select_object_frames(
    client: Any,
    object_id: str,
    indices: List[int],
    common_tag: Optional[str] = None,
) -> SelectObjectFramesResponse:
    """Promote selected frames of a review object to completed objects."""
    request_data: Dict[str, Any] = {"indices": indices}
    if common_tag is not None:
        request_data["common_tag"] = common_tag
    return SelectObjectFramesResponse(
        **_post(client, f"objects/{object_id}/select-frames", request_data)
    )


def list_objects(
    client: Any, limit: Optional[int] = None, offset: Optional[int] = None
) -> ObjectsListResponse:
    """List the objects created by the authenticated user."""
    params: Dict[str, Any] = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    return ObjectsListResponse(**_get(client, "objects", params=params or None))


def get_object(client: Any, object_id: str) -> ObjectDetail:
    """Retrieve full details for a single object."""
    return ObjectDetail(**_get(client, f"objects/{object_id}"))


def delete_object(client: Any, object_id: str) -> Dict[str, Any]:
    """Delete an object and its associated data."""
    return _delete(client, f"objects/{object_id}")


def update_object_tags(client: Any, object_id: str, tags: List[str]) -> Dict[str, Any]:
    """Replace the tags on an object."""
    return _patch(client, f"objects/{object_id}/tags", {"tags": tags})
