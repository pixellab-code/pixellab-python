from __future__ import annotations

import pixellab
from pixellab.characters import CharactersListResponse


def test_list_characters():
    """Listing characters is read-only and should return a paginated response."""
    client = pixellab.Client.from_env_file(".env.development.secrets")

    response = client.list_characters(limit=5)

    assert isinstance(response, CharactersListResponse)
    assert isinstance(response.total, int)
    assert isinstance(response.characters, list)
    assert len(response.characters) <= 5
    for character in response.characters:
        assert character.id
        assert character.name is not None


def test_get_character_roundtrip():
    """If the account has characters, fetching one returns full details."""
    client = pixellab.Client.from_env_file(".env.development.secrets")

    listing = client.list_characters(limit=1)
    if not listing.characters:
        return  # nothing to fetch on this account

    character_id = listing.characters[0].id
    detail = client.get_character(character_id)
    assert detail.id == character_id
    assert detail.prompt is not None
