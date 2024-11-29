from __future__ import annotations

import base64
from io import BytesIO
from pathlib import Path

import PIL.Image

import pixellab
from pixellab.models import Base64Image, ImageSize


def test_generate_image_pixflux():
    client = pixellab.Client.from_env_file(".env.development.secrets")

    response = client.generate_image_pixflux(
        description = "cute dragon",
        image_size = {"width": 64, "height": 64},
        no_background = False,
        text_guidance_scale = 8.0,
    )

    image = response.image.pil_image()
    assert isinstance(image, PIL.Image.Image)
    assert image.size == (64, 64)

    results_dir = Path("tests") / "results"
    results_dir.mkdir(exist_ok=True)

    image.save(results_dir / "pixeflux_cute_dragon.png")

