from __future__ import annotations

import pixellab
from pixellab.tilesets import IsometricTilesListResponse, TilesetsListResponse


def test_list_tilesets():
    """Listing tilesets is read-only and should return a paginated response."""
    client = pixellab.Client.from_env_file(".env.development.secrets")

    response = client.list_tilesets(limit=5)

    assert isinstance(response, TilesetsListResponse)
    assert isinstance(response.total, int)
    assert isinstance(response.tilesets, list)
    assert len(response.tilesets) <= 5


def test_list_isometric_tiles():
    """Listing isometric tiles is read-only."""
    client = pixellab.Client.from_env_file(".env.development.secrets")

    response = client.list_isometric_tiles(limit=5)

    assert isinstance(response, IsometricTilesListResponse)
    assert isinstance(response.total, int)
    assert isinstance(response.tiles, list)
    assert len(response.tiles) <= 5
