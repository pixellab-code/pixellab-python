from __future__ import annotations

import json
from pathlib import Path

import PIL.Image

import pixellab


def test_generate_animation_skeleton():
    client = pixellab.Client.from_env_file(".env.development.secrets")

    images_dir = Path("tests") / "images"
    reference_image = PIL.Image.open(images_dir / "boy.png").resize((16, 16))
    freeze_mask = PIL.Image.open(images_dir / "freeze_mask.png").resize((16, 16))

    # Load key points from walk.json
    skeleton_points_dir = Path("tests") / "skeleton_points"
    with open(skeleton_points_dir / "walk.json", "r") as file:
        skeleton_keypoints = json.load(file)["pose_keypoints"]

    animation_images = [reference_image, None, None, None]
    mask_images = [freeze_mask, None, None, None]

    response = client.generate_animation_skeleton(
        view="side",
        direction="south",
        image_size={"width": 16, "height": 16},
        reference_image=reference_image,
        animation_images=animation_images,
        mask_images=mask_images,
        skeleton_keypoints=skeleton_keypoints,
    )

    assert len(response.images) == 4
    for i, image in enumerate(response.images):
        pil_image = image.pil_image()
        assert isinstance(pil_image, PIL.Image.Image)
        assert pil_image.size == (16, 16)

    results_dir = Path("tests") / "results"
    results_dir.mkdir(exist_ok=True)

    total_width = 16 * len(response.images)
    stacked_image = PIL.Image.new("RGBA", (total_width, 16))

    for i, image in enumerate(response.images):
        stacked_image.paste(image.pil_image(), (i * 16, 0))

    stacked_image.save(results_dir / "animation_skeleton_frames.png")
