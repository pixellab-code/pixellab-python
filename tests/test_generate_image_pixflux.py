from __future__ import annotations

import base64
from io import BytesIO
from pathlib import Path

import PIL.Image

import pixellab


def test_generate_image_pixflux():
    client = pixellab.Client.from_env_file(".env.development.secrets")

    images_dir = Path("tests") / "images"
    init_image = PIL.Image.open(images_dir / "boy.png").resize((32, 32))

    response = client.generate_image_pixflux(
        description="cute dragon boy",
        image_size={"width": 32, "height": 32},
        init_image=init_image,
        init_image_strength=250,
        view="low top-down",
        direction="south",
        no_background=True,
        text_guidance_scale=7.5,
    )

    image = response.image.pil_image()
    assert isinstance(image, PIL.Image.Image)
    assert image.size == (32, 32)

    results_dir = Path("tests") / "results"
    results_dir.mkdir(exist_ok=True)

    image.save(results_dir / "pixflux_cute_dragon_boy.png")
