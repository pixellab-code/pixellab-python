"""Character management endpoints (v2).

Most create/animate endpoints are asynchronous: they return a
``background_job_id`` (and ``character_id``) and process in the background.
Poll with ``client.wait_for_background_job(job_id)`` and then fetch the
finished character with ``client.get_character(character_id)``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

import PIL.Image
import requests
from pydantic import BaseModel, ConfigDict

from ._common import Usage, delete as _delete, get as _get, patch as _patch, post as _post
from .models import Base64Image, ImageSize

if TYPE_CHECKING:
    from .client import PixelLabClient


def _img(image: Optional[PIL.Image.Image]) -> Optional[Dict[str, Any]]:
    return Base64Image.from_pil_image(image).model_dump() if image is not None else None


class CharacterJobResponse(BaseModel):
    """Async acknowledgement for character create/edit endpoints."""

    background_job_id: str
    character_id: str
    status: str = "processing"
    usage: Optional[Usage] = None


class CreateCharacterAnimationResponse(BaseModel):
    background_job_ids: List[str]
    directions: List[str]
    status: str = "processing"


class CharacterSummary(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str
    prompt: str
    size: Dict[str, int]
    directions: int
    created_at: str
    animation_count: int
    template_id: str
    preview_url: str
    view: Optional[str] = None
    tags: List[str] = []
    group_id: Optional[str] = None


class CharactersListResponse(BaseModel):
    characters: List[CharacterSummary]
    total: int
    usage: Optional[Usage] = None


class CharacterDetail(BaseModel):
    """Full character details. Extra fields are preserved as-is."""

    model_config = ConfigDict(extra="allow")

    id: str
    name: str
    prompt: str
    size: Dict[str, int]
    directions: int
    created_at: str
    animation_count: int
    template_id: str
    rotation_urls: Dict[str, Any]
    view: Optional[str] = None
    tags: List[str] = []
    animations: List[Dict[str, Any]] = []


def create_character_with_4_directions(
    client: Any,
    description: str,
    image_size: Union[ImageSize, Dict[str, int]],
    text_guidance_scale: float = 8.0,
    outline: Optional[str] = None,
    shading: Optional[str] = None,
    detail: Optional[str] = None,
    view: Optional[str] = None,
    isometric: bool = False,
    color_image: Optional[PIL.Image.Image] = None,
    force_colors: bool = False,
    proportions: Optional[Dict[str, Any]] = None,
    template_id: Optional[str] = None,
    directions: Optional[Dict[str, Any]] = None,
    seed: Optional[int] = None,
    async_mode: bool = True,
) -> CharacterJobResponse:
    """Generate a character facing the 4 cardinal directions (async)."""
    request_data: Dict[str, Any] = {
        "description": description,
        "image_size": image_size,
        "text_guidance_scale": text_guidance_scale,
        "isometric": isometric,
        "force_colors": force_colors,
        "async_mode": async_mode,
    }
    for key, value in {
        "outline": outline,
        "shading": shading,
        "detail": detail,
        "view": view,
        "proportions": proportions,
        "template_id": template_id,
        "directions": directions,
        "seed": seed,
        "color_image": _img(color_image),
    }.items():
        if value is not None:
            request_data[key] = value

    return CharacterJobResponse(
        **_post(client, "create-character-with-4-directions", request_data)
    )


def create_character_with_8_directions(
    client: Any,
    description: str,
    image_size: Union[ImageSize, Dict[str, int]],
    mode: str = "standard",
    text_guidance_scale: float = 8.0,
    outline: Optional[str] = None,
    shading: Optional[str] = None,
    detail: Optional[str] = None,
    view: Optional[str] = None,
    isometric: bool = False,
    color_image: Optional[PIL.Image.Image] = None,
    force_colors: bool = False,
    proportions: Optional[Dict[str, Any]] = None,
    template_id: Optional[str] = None,
    directions: Optional[Dict[str, Any]] = None,
    seed: Optional[int] = None,
    async_mode: bool = True,
) -> CharacterJobResponse:
    """Generate a character facing the 8 directions (async)."""
    request_data: Dict[str, Any] = {
        "description": description,
        "image_size": image_size,
        "mode": mode,
        "text_guidance_scale": text_guidance_scale,
        "isometric": isometric,
        "force_colors": force_colors,
        "async_mode": async_mode,
    }
    for key, value in {
        "outline": outline,
        "shading": shading,
        "detail": detail,
        "view": view,
        "proportions": proportions,
        "template_id": template_id,
        "directions": directions,
        "seed": seed,
        "color_image": _img(color_image),
    }.items():
        if value is not None:
            request_data[key] = value

    return CharacterJobResponse(
        **_post(client, "create-character-with-8-directions", request_data)
    )


def create_character_pro(
    client: Any,
    description: str,
    image_size: Union[ImageSize, Dict[str, int]],
    method: str = "create_with_style",
    view: str = "low top-down",
    template_id: str = "mannequin",
    concept_image: Optional[PIL.Image.Image] = None,
    reference_image: Optional[PIL.Image.Image] = None,
    style_description: Optional[str] = None,
    no_background: bool = True,
    seed: Optional[int] = None,
) -> CharacterJobResponse:
    """Create a high-quality character with Pro mode (8 directions, async)."""
    request_data: Dict[str, Any] = {
        "description": description,
        "image_size": image_size,
        "method": method,
        "view": view,
        "template_id": template_id,
        "no_background": no_background,
    }
    for key, value in {
        "concept_image": _img(concept_image),
        "reference_image": _img(reference_image),
        "style_description": style_description,
        "seed": seed,
    }.items():
        if value is not None:
            request_data[key] = value

    return CharacterJobResponse(**_post(client, "create-character-pro", request_data))


def create_character_v3(
    client: Any,
    description: str,
    reference_image: Optional[PIL.Image.Image] = None,
    image_size: Optional[Union[ImageSize, Dict[str, int]]] = None,
    view: str = "low top-down",
    template_id: str = "mannequin",
    name: Optional[str] = None,
    no_background: bool = True,
    outline: Optional[str] = None,
    detail: Optional[str] = None,
    seed: Optional[int] = None,
) -> CharacterJobResponse:
    """Create a character with the v3 model (8 rotations, async)."""
    request_data: Dict[str, Any] = {
        "description": description,
        "view": view,
        "template_id": template_id,
        "no_background": no_background,
    }
    for key, value in {
        "reference_image": _img(reference_image),
        "image_size": image_size,
        "name": name,
        "outline": outline,
        "detail": detail,
        "seed": seed,
    }.items():
        if value is not None:
            request_data[key] = value

    return CharacterJobResponse(**_post(client, "create-character-v3", request_data))


def create_character_state(
    client: Any,
    character_id: str,
    edit_description: str,
    no_background: bool = True,
    use_color_palette_from_reference: bool = False,
    seed: Optional[int] = None,
) -> CharacterJobResponse:
    """Apply a text edit to a character, producing a new variant (async)."""
    request_data: Dict[str, Any] = {
        "character_id": character_id,
        "edit_description": edit_description,
        "no_background": no_background,
        "use_color_palette_from_reference": use_color_palette_from_reference,
    }
    if seed is not None:
        request_data["seed"] = seed

    return CharacterJobResponse(**_post(client, "create-character-state", request_data))


def _animation_request(
    character_id: str,
    animation_name: Optional[str],
    description: Optional[str],
    action_description: Optional[str],
    mode: Optional[str],
    template_animation_id: Optional[str],
    frame_count: int,
    text_guidance_scale: float,
    outline: Optional[str],
    shading: Optional[str],
    detail: Optional[str],
    directions: Optional[List[str]],
    isometric: bool,
    color_image: Optional[PIL.Image.Image],
    force_colors: bool,
    seed: Optional[int],
    async_mode: bool,
) -> Dict[str, Any]:
    request_data: Dict[str, Any] = {
        "character_id": character_id,
        "frame_count": frame_count,
        "text_guidance_scale": text_guidance_scale,
        "isometric": isometric,
        "force_colors": force_colors,
        "async_mode": async_mode,
    }
    for key, value in {
        "animation_name": animation_name,
        "description": description,
        "action_description": action_description,
        "mode": mode,
        "template_animation_id": template_animation_id,
        "outline": outline,
        "shading": shading,
        "detail": detail,
        "directions": directions,
        "seed": seed,
        "color_image": _img(color_image),
    }.items():
        if value is not None:
            request_data[key] = value
    return request_data


def animate_character(
    client: Any,
    character_id: str,
    animation_name: Optional[str] = None,
    description: Optional[str] = None,
    action_description: Optional[str] = None,
    mode: Optional[str] = None,
    template_animation_id: Optional[str] = None,
    frame_count: int = 8,
    text_guidance_scale: float = 8.0,
    outline: Optional[str] = None,
    shading: Optional[str] = None,
    detail: Optional[str] = None,
    directions: Optional[List[str]] = None,
    isometric: bool = False,
    color_image: Optional[PIL.Image.Image] = None,
    force_colors: bool = False,
    seed: Optional[int] = None,
    async_mode: bool = True,
) -> CreateCharacterAnimationResponse:
    """Add an animation sequence to an existing character (async)."""
    request_data = _animation_request(
        character_id, animation_name, description, action_description, mode,
        template_animation_id, frame_count, text_guidance_scale, outline, shading,
        detail, directions, isometric, color_image, force_colors, seed, async_mode,
    )
    return CreateCharacterAnimationResponse(
        **_post(client, "animate-character", request_data)
    )


def create_character_animation(
    client: Any,
    character_id: str,
    animation_name: Optional[str] = None,
    description: Optional[str] = None,
    action_description: Optional[str] = None,
    mode: Optional[str] = None,
    template_animation_id: Optional[str] = None,
    frame_count: int = 8,
    text_guidance_scale: float = 8.0,
    outline: Optional[str] = None,
    shading: Optional[str] = None,
    detail: Optional[str] = None,
    directions: Optional[List[str]] = None,
    isometric: bool = False,
    color_image: Optional[PIL.Image.Image] = None,
    force_colors: bool = False,
    seed: Optional[int] = None,
    async_mode: bool = True,
) -> CreateCharacterAnimationResponse:
    """Create a character animation via ``POST /characters/animations`` (async)."""
    request_data = _animation_request(
        character_id, animation_name, description, action_description, mode,
        template_animation_id, frame_count, text_guidance_scale, outline, shading,
        detail, directions, isometric, color_image, force_colors, seed, async_mode,
    )
    return CreateCharacterAnimationResponse(
        **_post(client, "characters/animations", request_data)
    )


def list_characters(
    client: Any, limit: Optional[int] = None, offset: Optional[int] = None
) -> CharactersListResponse:
    """List the characters created by the authenticated user."""
    params: Dict[str, Any] = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    return CharactersListResponse(**_get(client, "characters", params=params or None))


def get_character(client: Any, character_id: str) -> CharacterDetail:
    """Retrieve full details for a single character."""
    return CharacterDetail(**_get(client, f"characters/{character_id}"))


def delete_character(client: Any, character_id: str) -> Dict[str, Any]:
    """Delete a character and its associated data."""
    return _delete(client, f"characters/{character_id}")


def update_character_tags(
    client: Any, character_id: str, tags: List[str]
) -> Dict[str, Any]:
    """Replace the tags on a character."""
    return _patch(client, f"characters/{character_id}/tags", {"tags": tags})


def download_character_zip(client: Any, character_id: str) -> bytes:
    """Download a character (rotations + animations) as a ZIP archive.

    Returns the raw ZIP bytes; write them to a ``.zip`` file to save.
    """
    response = requests.get(
        f"{client.base_url}/v2/characters/{character_id}/zip",
        headers=client.headers(),
    )
    response.raise_for_status()
    return response.content
