from __future__ import annotations

from pathlib import Path

import PIL.Image

import pixellab


def test_create_image_pixen():
    """Generate a small pixel art image with the Pixen model."""
    client = pixellab.Client.from_env_file(".env.development.secrets")

    response = client.create_image_pixen(
        description="cute dragon",
        image_size={"width": 64, "height": 64},
        seed=0,
    )

    image = response.image.pil_image()
    assert isinstance(image, PIL.Image.Image)

    if response.usage is not None:
        assert response.usage.type == "usd"
        assert response.usage.usd >= 0

    results_dir = Path("tests") / "results"
    results_dir.mkdir(exist_ok=True)
    image.save(results_dir / "create_image_pixen.png")
