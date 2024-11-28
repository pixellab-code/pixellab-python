from __future__ import annotations

import base64
from io import BytesIO
from pathlib import Path

import PIL.Image

import pixellab
from pixellab.models import Base64Image, ImageSize


def test_generate_image_bitforge():
    client = pixellab.Client.from_env_file(".env.development.secrets")

    images_dir = Path("tests") / "images"
    inpainting_image = PIL.Image.open(images_dir / "boy.png")
    style_image = PIL.Image.open(images_dir / "boy.png")
    mask_image = PIL.Image.open(images_dir / "mask.png")
    init_image = PIL.Image.open(images_dir / "boy.png")

    response = client.generate_image_bitforge(
        description="boy with wings",
        image_size=ImageSize(width=16, height=16),
        no_background=True,
        style_image=style_image,
        inpainting_image=inpainting_image,
        mask_image=mask_image,
        init_image=init_image,
        init_image_strength=250,
    )

    # Verify we got a valid image back
    image = response.image.pil_image()
    assert isinstance(image, PIL.Image.Image)
    assert image.size == (16, 16)

    # Create results directory using pathlib
    results_dir = Path("tests") / "results"
    results_dir.mkdir(exist_ok=True)

    # Save the generated image using pathlib
    image.save(results_dir / "bitforge_boy_with_wings.png")
