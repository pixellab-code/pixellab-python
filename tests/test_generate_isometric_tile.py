from __future__ import annotations

import base64
from io import BytesIO
from pathlib import Path

import PIL.Image

import pixellab
from pixellab.models import Base64Image, ImageSize


def test_generate_isometric_tile():
    client = pixellab.Client.from_env_file(".env.development.secrets")

    response = client.generate_isometric_tile(
        description="grass on top of dirt",
        image_size={"width": 32, "height": 32},
        text_guidance_scale=8.0,
        isometric_tile_size=32,
        isometric_tile_shape="thick tile",
    )

    image = response.image.pil_image()
    assert isinstance(image, PIL.Image.Image)
    assert image.size == (32, 32)

    results_dir = Path("tests") / "results"
    results_dir.mkdir(exist_ok=True)

    image.save(results_dir / "isometric_tile_grass_dirt.png")

def test_generate_isometric_tile_with_reference_shape():
    client = pixellab.Client.from_env_file(".env.development.secrets")

    images_dir = Path("tests") / "images"
    reference_shape = PIL.Image.open(images_dir / "isometric_tile.png")  # Already 32x32
    response = client.generate_isometric_tile(
        description="lake on top of dirt",
        image_size={"width": 32, "height": 32},
        text_guidance_scale=8.0,
        isometric_tile_size=32,
        isometric_tile_shape="reference shape",
        reference_shape=reference_shape,
        reference_shape_strength=300,
    )

    image = response.image.pil_image()
    assert isinstance(image, PIL.Image.Image)
    assert image.size == (32, 32)

    results_dir = Path("tests") / "results"
    results_dir.mkdir(exist_ok=True)

    image.save(results_dir / "isometric_tile_with_reference_shape.png")
