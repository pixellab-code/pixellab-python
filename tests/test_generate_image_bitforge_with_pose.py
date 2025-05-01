from __future__ import annotations

import json
import base64
from io import BytesIO
from pathlib import Path

import PIL.Image

import pixellab
from pixellab.models import Base64Image, ImageSize


def test_generate_image_bitforge():
    client = pixellab.Client.from_env_file(".env.development.secrets")

    images_dir = Path("tests") / "images"

    skeleton_points_dir = Path("tests") / "skeleton_points"
    with open(skeleton_points_dir / "walk.json", "r") as file:
        skeleton_keypoints = json.load(file)["pose_keypoints"]
        
    response = client.generate_image_bitforge(
        description="boy",
        image_size=dict(width=32, height=32),
        no_background=True,
        skeleton_keypoints=skeleton_keypoints[0],
        skeleton_guidance_scale=1.0
    )

    # Verify we got a valid image back
    image = response.image.pil_image()
    assert isinstance(image, PIL.Image.Image)
    assert image.size == (32, 32)

    # Create results directory using pathlib
    results_dir = Path("tests") / "results"
    results_dir.mkdir(exist_ok=True)

    # Save the generated image using pathlib
    image.save(results_dir / "bitforge_boy_from_keypoints.png")
