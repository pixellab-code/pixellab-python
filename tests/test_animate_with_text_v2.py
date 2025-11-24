from __future__ import annotations

from pathlib import Path

import PIL.Image

import pixellab


def test_animate_with_text_v2():
    client = pixellab.Client.from_env_file(".env.development.secrets")

    images_dir = Path("tests") / "images"
    reference_image = PIL.Image.open(images_dir / "boy64.png")  # Already 64x64

    response = client.animate_with_text_v2(
        reference_image=reference_image,
        reference_image_size={"width": 64, "height": 64},
        action="walk",
        image_size={"width": 64, "height": 64},
    )

    assert len(response.images) > 0
    for i, image in enumerate(response.images):
        pil_image = image.pil_image()
        assert isinstance(pil_image, PIL.Image.Image)

    # Save results for visual inspection
    results_dir = Path("tests") / "results"
    results_dir.mkdir(exist_ok=True)

    total_width = 64 * len(response.images)
    stacked_image = PIL.Image.new("RGBA", (total_width, 64))

    for i, image in enumerate(response.images):
        pil_image = image.pil_image()
        if pil_image.size != (64, 64):
            pil_image = pil_image.resize((64, 64), PIL.Image.Resampling.NEAREST)
        stacked_image.paste(pil_image, (i * 64, 0))

    stacked_image.save(results_dir / "animation_text_v2_frames.png")
