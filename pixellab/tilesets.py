"""Tileset, isometric-tile and tiles-pro endpoints (v2).

The create endpoints are asynchronous (HTTP 202): they return a
``background_job_id`` together with the id of the resource being built
(``tileset_id`` / ``tile_id``). Poll with
``client.wait_for_background_job(job_id)`` and then fetch the finished
resource with the matching getter (``get_tileset`` / ``get_tiles_pro``).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional, Union

import PIL.Image
from pydantic import BaseModel, ConfigDict

from ._common import Usage, get as _get, post as _post
from .models import Base64Image

if TYPE_CHECKING:
    from .client import PixelLabClient

TileSize = Union[Dict[str, int], Any]


def _img(image: Optional[PIL.Image.Image]) -> Optional[Dict[str, Any]]:
    return Base64Image.from_pil_image(image).model_dump() if image is not None else None


class CreateTilesetBackgroundResponse(BaseModel):
    background_job_id: str
    tileset_id: str
    status: str = "processing"
    usage: Optional[Usage] = None


class CreateTilesProBackgroundResponse(BaseModel):
    background_job_id: str
    tile_id: str
    status: str = "processing"
    usage: Optional[Usage] = None


class GetTilesProResponse(BaseModel):
    storage_urls: Dict[str, Any]
    usage: Optional[Usage] = None


class GetIsometricTileResponse(BaseModel):
    image: Base64Image
    usage: Optional[Usage] = None


class TilesetSummary(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    lower_description: str
    upper_description: str
    created_at: str
    status: str
    name: Optional[str] = None
    tile_size: Optional[Dict[str, int]] = None
    view: Optional[str] = None


class TilesetsListResponse(BaseModel):
    tilesets: List[TilesetSummary]
    total: int
    usage: Optional[Usage] = None


class IsometricTileSummary(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    description: str
    created_at: str
    status: str
    name: Optional[str] = None
    size: Optional[int] = None
    tile_shape: Optional[str] = None


class IsometricTilesListResponse(BaseModel):
    tiles: List[IsometricTileSummary]
    total: int
    usage: Optional[Usage] = None


# Detailed tileset payload (returned by GET /tilesets/{id}); kept permissive
# so it stays compatible with the generate_tileset response model.
class TilesetDetailResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    tileset: Dict[str, Any]
    metadata: Dict[str, Any]
    usage: Optional[Usage] = None


def _tileset_request(
    lower_description: str,
    upper_description: Optional[str],
    transition_description: str,
    tile_size: TileSize,
    text_guidance_scale: float,
    outline: Optional[str],
    shading: Optional[str],
    detail: Optional[str],
    view: Optional[str],
    tile_strength: float,
    tileset_adherence_freedom: float,
    tileset_adherence: float,
    transition_size: float,
    lower_base_tile_id: Optional[str],
    upper_base_tile_id: Optional[str],
    lower_reference_image: Optional[PIL.Image.Image],
    upper_reference_image: Optional[PIL.Image.Image],
    transition_reference_image: Optional[PIL.Image.Image],
    color_image: Optional[PIL.Image.Image],
    seed: Optional[int],
) -> Dict[str, Any]:
    request_data: Dict[str, Any] = {
        "lower_description": lower_description,
        "transition_description": transition_description,
        "tile_size": tile_size,
        "text_guidance_scale": text_guidance_scale,
        "tile_strength": tile_strength,
        "tileset_adherence_freedom": tileset_adherence_freedom,
        "tileset_adherence": tileset_adherence,
        "transition_size": transition_size,
    }
    for key, value in {
        "upper_description": upper_description,
        "view": view,
        "outline": outline,
        "shading": shading,
        "detail": detail,
        "lower_base_tile_id": lower_base_tile_id,
        "upper_base_tile_id": upper_base_tile_id,
        "lower_reference_image": _img(lower_reference_image),
        "upper_reference_image": _img(upper_reference_image),
        "transition_reference_image": _img(transition_reference_image),
        "color_image": _img(color_image),
        "seed": seed,
    }.items():
        if value is not None:
            request_data[key] = value
    return request_data


def create_tileset_sidescroller(
    client: Any,
    lower_description: str,
    transition_description: str = "",
    tile_size: Optional[TileSize] = None,
    text_guidance_scale: float = 8.0,
    outline: Optional[str] = None,
    shading: Optional[str] = None,
    detail: Optional[str] = None,
    tile_strength: float = 1.0,
    tileset_adherence_freedom: float = 500.0,
    tileset_adherence: float = 100.0,
    transition_size: float = 0.0,
    lower_base_tile_id: Optional[str] = None,
    lower_reference_image: Optional[PIL.Image.Image] = None,
    transition_reference_image: Optional[PIL.Image.Image] = None,
    color_image: Optional[PIL.Image.Image] = None,
    seed: Optional[int] = None,
) -> CreateTilesetBackgroundResponse:
    """Create a sidescroller platform tileset (async)."""
    if tile_size is None:
        tile_size = {"width": 16, "height": 16}
    request_data = _tileset_request(
        lower_description, None, transition_description, tile_size,
        text_guidance_scale, outline, shading, detail, None, tile_strength,
        tileset_adherence_freedom, tileset_adherence, transition_size,
        lower_base_tile_id, None, lower_reference_image, None,
        transition_reference_image, color_image, seed,
    )
    return CreateTilesetBackgroundResponse(
        **_post(client, "create-tileset-sidescroller", request_data)
    )


def create_tiles_pro(
    client: Any,
    description: str,
    tile_type: str = "isometric",
    tile_size: int = 32,
    tile_height: Optional[int] = None,
    tile_view: str = "low top-down",
    tile_view_angle: Optional[float] = None,
    tile_depth_ratio: Optional[float] = None,
    style_images: Optional[List[Dict[str, Any]]] = None,
    style_options: Optional[Dict[str, bool]] = None,
    seed: Optional[int] = None,
) -> CreateTilesProBackgroundResponse:
    """Create multiple tile variations by type (async)."""
    request_data: Dict[str, Any] = {
        "description": description,
        "tile_type": tile_type,
        "tile_size": tile_size,
        "tile_view": tile_view,
    }
    for key, value in {
        "tile_height": tile_height,
        "tile_view_angle": tile_view_angle,
        "tile_depth_ratio": tile_depth_ratio,
        "style_images": style_images,
        "style_options": style_options,
        "seed": seed,
    }.items():
        if value is not None:
            request_data[key] = value

    return CreateTilesProBackgroundResponse(
        **_post(client, "create-tiles-pro", request_data)
    )


def list_tilesets(
    client: Any, limit: Optional[int] = None, offset: Optional[int] = None
) -> TilesetsListResponse:
    """List the tilesets created by the authenticated user."""
    params: Dict[str, Any] = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    return TilesetsListResponse(**_get(client, "tilesets", params=params or None))


def get_tileset(client: Any, tileset_id: str) -> TilesetDetailResponse:
    """Retrieve a completed tileset by id."""
    return TilesetDetailResponse(**_get(client, f"tilesets/{tileset_id}"))


def get_tiles_pro(client: Any, tile_id: str) -> GetTilesProResponse:
    """Retrieve a completed tiles-pro set by id."""
    return GetTilesProResponse(**_get(client, f"tiles-pro/{tile_id}"))


def list_isometric_tiles(
    client: Any, limit: Optional[int] = None, offset: Optional[int] = None
) -> IsometricTilesListResponse:
    """List the isometric tiles created by the authenticated user."""
    params: Dict[str, Any] = {}
    if limit is not None:
        params["limit"] = limit
    if offset is not None:
        params["offset"] = offset
    return IsometricTilesListResponse(
        **_get(client, "isometric-tiles", params=params or None)
    )


def get_isometric_tile(client: Any, tile_id: str) -> GetIsometricTileResponse:
    """Retrieve a completed isometric tile by id."""
    return GetIsometricTileResponse(**_get(client, f"isometric-tiles/{tile_id}"))
