from __future__ import annotations

from pathlib import Path

import PIL.Image

import pixellab


def test_remove_background():
    """Remove the background from a small pixel art image."""
    client = pixellab.Client.from_env_file(".env.development.secrets")

    source = PIL.Image.open(Path("tests") / "images" / "boy64.png").convert("RGBA")
    source = source.resize((64, 64))

    response = client.remove_background(
        image=source,
        image_size={"width": 64, "height": 64},
    )

    image = response.image.pil_image()
    assert isinstance(image, PIL.Image.Image)

    if response.usage is not None:
        assert response.usage.type == "usd"
        assert response.usage.usd >= 0

    results_dir = Path("tests") / "results"
    results_dir.mkdir(exist_ok=True)
    image.save(results_dir / "remove_background.png")
