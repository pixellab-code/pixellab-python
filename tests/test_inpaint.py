from __future__ import annotations

from pathlib import Path

import PIL.Image

import pixellab


def test_inpaint():
    client = pixellab.Client.from_env_file(".env.development.secrets")

    images_dir = Path("tests") / "images"
    inpainting_image = PIL.Image.open(images_dir / "boy.png").resize((16, 16))
    mask_image = PIL.Image.open(images_dir / "mask.png").resize((16, 16))

    response = client.inpaint(
        description="boy with wings",
        image_size={"width": 16, "height": 16},
        no_background=True,
        inpainting_image=inpainting_image,
        mask_image=mask_image,
        text_guidance_scale=3.0,
    )

    image = response.image.pil_image()
    assert isinstance(image, PIL.Image.Image)
    assert image.size == (16, 16)

    results_dir = Path("tests") / "results"
    results_dir.mkdir(exist_ok=True)

    image.save(results_dir / "inpainting_boy_with_wings.png")
