from __future__ import annotations

from pathlib import Path

import PIL.Image

import pixellab


def test_estimate_skeleton():
    client = pixellab.Client.from_env_file(".env.development.secrets")

    images_dir = Path("tests") / "images"
    test_image = PIL.Image.open(images_dir / "boy.png")

    response = client.estimate_skeleton(
        image=test_image,
    )

    assert isinstance(response.keypoints, list)
    assert len(response.keypoints) == 18
    for keypoint in response.keypoints:
        assert isinstance(keypoint.x, float)
        assert isinstance(keypoint.y, float)
        assert isinstance(keypoint.label, str)
        assert isinstance(keypoint.z_index, int)
