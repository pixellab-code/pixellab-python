from __future__ import annotations

import pixellab
from pixellab.objects import ObjectsListResponse


def test_list_objects():
    """Listing objects is read-only and should return a paginated response."""
    client = pixellab.Client.from_env_file(".env.development.secrets")

    response = client.list_objects(limit=5)

    assert isinstance(response, ObjectsListResponse)
    assert isinstance(response.total, int)
    assert isinstance(response.objects, list)
    assert len(response.objects) <= 5


def test_get_object_roundtrip():
    """If the account has objects, fetching one returns full details."""
    client = pixellab.Client.from_env_file(".env.development.secrets")

    listing = client.list_objects(limit=1)
    if not listing.objects:
        return

    object_id = listing.objects[0].id
    detail = client.get_object(object_id)
    assert detail.id == object_id
