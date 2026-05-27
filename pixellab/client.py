from __future__ import annotations

from pydantic import BaseModel

from .settings import settings


class PixelLabClient(BaseModel):
    secret: str
    base_url: str = "https://api.pixellab.ai"

    @classmethod
    def from_env(cls) -> PixelLabClient:
        return cls(**settings(env_file=None).model_dump(exclude_none=True))

    @classmethod
    def from_env_file(cls, env_file: str) -> PixelLabClient:
        return cls(**settings(env_file=env_file).model_dump(exclude_none=True))

    def auth_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token()}",
        }

    def headers(self):
        return {"Authorization": f"Bearer {self.secret}"}

    from .animate_with_skeleton import animate_with_skeleton
    from .animate_with_text import animate_with_text
    from .animate_with_text_v2 import animate_with_text_v2
    from .edit_image import edit_image
    from .edit_images_v2 import edit_images_v2
    from .edit_animation_v2 import edit_animation_v2
    from .estimate_skeleton import estimate_skeleton
    from .generate_image_bitforge import generate_image_bitforge
    from .generate_image_pixflux import generate_image_pixflux
    from .generate_image_v2 import generate_image_v2
    from .generate_ui_v2 import generate_ui_v2
    from .generate_with_style_v2 import generate_with_style_v2
    from .generate_8_rotations_v2 import generate_8_rotations_v2
    from .rotate4_with_template import rotate4_with_template
    from .rotate8_with_template import rotate8_with_template
    from .animate_with_template import animate_with_template
    from .generate_tileset import generate_tileset
    from .get_balance import get_balance
    from .inpaint import inpaint
    from .inpaint_v3 import inpaint_v3
    from .interpolation_v2 import interpolation_v2
    from .transfer_outfit_v2 import transfer_outfit_v2
    from .rotate import rotate
    from .generate_isometric_tile import generate_isometric_tile
    from .resize import resize
    from .image_to_pixelart import image_to_pixelart

    # --- New v2 endpoints ---
    from ._common import get_background_job, wait_for_background_job

    # Image operations
    from .create_image_pixen import create_image_pixen
    from .remove_background import remove_background

    # Animation / rotation (v3, async)
    from .animate_with_text_v3 import animate_with_text_v3
    from .generate_8_rotations_v3 import generate_8_rotations_v3

    # Character management
    from .characters import (
        create_character_with_4_directions,
        create_character_with_8_directions,
        create_character_pro,
        create_character_v3,
        create_character_state,
        animate_character,
        create_character_animation,
        list_characters,
        get_character,
        delete_character,
        update_character_tags,
        download_character_zip,
    )

    # Object management
    from .objects import (
        create_1_direction_object,
        create_8_direction_object,
        create_map_object,
        animate_object,
        create_object_state,
        dismiss_object_review,
        select_object_frames,
        list_objects,
        get_object,
        delete_object,
        update_object_tags,
    )

    # Tilesets / isometric tiles / tiles-pro
    from .tilesets import (
        create_tileset_sidescroller,
        create_tiles_pro,
        list_tilesets,
        get_tileset,
        get_tiles_pro,
        list_isometric_tiles,
        get_isometric_tile,
    )
