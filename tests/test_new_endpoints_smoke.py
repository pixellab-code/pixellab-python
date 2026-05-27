"""Smoke test: every new v2 endpoint is wired onto the client (no network)."""

from __future__ import annotations

import pixellab

NEW_METHODS = [
    # image operations
    "create_image_pixen",
    "remove_background",
    # animation / rotation (v3)
    "animate_with_text_v3",
    "generate_8_rotations_v3",
    # character management
    "create_character_with_4_directions",
    "create_character_with_8_directions",
    "create_character_pro",
    "create_character_v3",
    "create_character_state",
    "animate_character",
    "create_character_animation",
    "list_characters",
    "get_character",
    "delete_character",
    "update_character_tags",
    "download_character_zip",
    # object management
    "create_1_direction_object",
    "create_8_direction_object",
    "create_map_object",
    "animate_object",
    "create_object_state",
    "dismiss_object_review",
    "select_object_frames",
    "list_objects",
    "get_object",
    "delete_object",
    "update_object_tags",
    # tilesets / tiles
    "create_tileset_sidescroller",
    "create_tiles_pro",
    "list_tilesets",
    "get_tileset",
    "get_tiles_pro",
    "list_isometric_tiles",
    "get_isometric_tile",
    # background jobs
    "get_background_job",
    "wait_for_background_job",
]


def test_all_new_methods_present():
    client = pixellab.Client(secret="dummy-secret")
    missing = [name for name in NEW_METHODS if not callable(getattr(client, name, None))]
    assert not missing, f"Missing client methods: {missing}"
