from __future__ import annotations

from pathlib import Path

import PIL.Image

import pixellab


def test_image_to_pixelart():
    """Test converting an image to pixel art."""
    client = pixellab.Client.from_env_file(".env.development.secrets")

    # Load the landscape test image
    images_dir = Path("tests") / "images"
    source_img = PIL.Image.open(images_dir / "landscape_non_pixel_art.png")

    # Resize to fit within max constraints (1280x1280 input, 320x320 output)
    # The image is 1536x1024, so we'll resize to 1280x820 (maintaining aspect ratio)
    source_img = source_img.resize((1280, 820))

    output_width = 320
    output_height = 204

    response = client.image_to_pixelart(
        image=source_img,
        image_size={"width": 1280, "height": 820},
        output_size={"width": output_width, "height": output_height},
    )

    # Verify response
    image = response.image.pil_image()
    assert isinstance(image, PIL.Image.Image)
    # Backend may adjust size slightly, so check it's close
    assert abs(image.size[0] - output_width) <= 1
    assert abs(image.size[1] - output_height) <= 1

    # Verify usage information
    assert response.usage.type == "usd"
    assert isinstance(response.usage.usd, float)
    assert response.usage.usd >= 0

    # Save result
    results_dir = Path("tests") / "results"
    results_dir.mkdir(exist_ok=True)
    image.save(results_dir / "image_to_pixelart.png")

