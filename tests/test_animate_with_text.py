from __future__ import annotations

from pathlib import Path

import PIL.Image

import pixellab


def test_animate_with_text():
    client = pixellab.Client.from_env_file(".env.development.secrets")

    images_dir = Path("tests") / "images"
    reference_image = PIL.Image.open(images_dir / "boy64.png").resize((64, 64))

    inpainting_images = [None, None, None, None]

    response = client.animate_with_text(
        character="pixel art boy",
        negative_description="",
        action="walking",
        view="side",
        direction="south",
        image_size={"width": 64, "height": 64},
        selected_reference_image=reference_image,
        inpainting_images=inpainting_images,
        n_frames=4,
    )

    assert len(response.images) == 4
    for i, image in enumerate(response.images):
        pil_image = image.pil_image()
        assert isinstance(pil_image, PIL.Image.Image)
        assert pil_image.size == (64, 64)

    results_dir = Path("tests") / "results"
    results_dir.mkdir(exist_ok=True)

    total_width = 64 * len(response.images)
    stacked_image = PIL.Image.new("RGBA", (total_width, 64))

    for i, image in enumerate(response.images):
        stacked_image.paste(image.pil_image(), (i * 64, 0))

    stacked_image.save(results_dir / "animation_text_frames.png")
