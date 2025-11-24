from __future__ import annotations

from pathlib import Path

import PIL.Image

import pixellab


def test_resize():
    """Test resizing a pixel art image from 32x32 to 64x64."""
    client = pixellab.Client.from_env_file(".env.development.secrets")

    # Create a simple test image or use existing test image
    images_dir = Path("tests") / "images"

    # Try to use an existing test image, or create a simple one
    if (images_dir / "boy.png").exists():
        source_img = PIL.Image.open(images_dir / "boy.png").resize((32, 32))
    else:
        # Create a simple test image if no test images exist
        source_img = PIL.Image.new("RGBA", (32, 32), (255, 0, 0, 255))

    response = client.resize(
        description="boy",
        reference_image=source_img,
        reference_image_size={"width": 32, "height": 32},
        target_size={"width": 64, "height": 64},
    )

    # Verify response
    image = response.image.pil_image()
    assert isinstance(image, PIL.Image.Image)
    assert image.size == (64, 64)

    # Verify usage information
    assert response.usage.type == "usd"
    assert isinstance(response.usage.usd, float)
    assert response.usage.usd >= 0

    # Save result
    results_dir = Path("tests") / "results"
    results_dir.mkdir(exist_ok=True)
    image.save(results_dir / "resize_32x32_to_64x64.png")


def test_resize_with_optional_params():
    """Test resizing with optional parameters like direction and no_background."""
    client = pixellab.Client.from_env_file(".env.development.secrets")

    images_dir = Path("tests") / "images"

    if (images_dir / "boy.png").exists():
        source_img = PIL.Image.open(images_dir / "boy.png").resize((32, 32))
    else:
        source_img = PIL.Image.new("RGBA", (32, 32), (0, 255, 0, 255))

    response = client.resize(
        description="boy",
        reference_image=source_img,
        reference_image_size={"width": 32, "height": 32},
        target_size={"width": 48, "height": 48},
        direction="south",
        no_background=True,
        seed=42,
    )

    image = response.image.pil_image()
    assert isinstance(image, PIL.Image.Image)
    assert image.size == (48, 48)

    results_dir = Path("tests") / "results"
    results_dir.mkdir(exist_ok=True)
    image.save(results_dir / "resize_with_options.png")

