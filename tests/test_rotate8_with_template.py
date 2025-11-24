from __future__ import annotations

from pathlib import Path

import PIL.Image
import pytest

import pixellab


def test_rotate8_with_template_basic():
    client = pixellab.Client.from_env_file(".env.development.secrets")
    
    response = client.rotate8_with_template(
        description="fantasy wizard character",
        image_size={"width": 48, "height": 48},
        text_guidance_scale=8.0,
    )
    
    # Check response structure
    assert hasattr(response, "images")
    assert hasattr(response, "usage")
    
    # Check that we got all 8 directions
    expected_directions = [
        "south", "south_east", "east", "north_east",
        "north", "north_west", "west", "south_west"
    ]
    
    if isinstance(response.images, dict):
        # API returns hyphenated keys, check for both
        for direction in expected_directions:
            assert direction in response.images or direction.replace("_", "-") in response.images
    else:
        for direction in expected_directions:
            assert hasattr(response.images, direction)
    
    # Save results
    results_dir = Path("tests") / "results"
    results_dir.mkdir(exist_ok=True)
    
    if isinstance(response.images, dict):
        for direction, base64_img in response.images.items():
            img = base64_img.pil_image()
            filename = direction.replace("-", "_")
            img.save(results_dir / f"8rotations_basic_{filename}.png")
    else:
        for direction in expected_directions:
            img = getattr(response.images, direction).pil_image()
            img.save(results_dir / f"8rotations_basic_{direction}.png")


def test_rotate8_with_template_with_template():
    client = pixellab.Client.from_env_file(".env.development.secrets")
    
    response = client.rotate8_with_template(
        description="cyberpunk hacker character",
        image_size={"width": 64, "height": 64},
        text_guidance_scale=8.0,
        reference={
            "type": "template",
            "template_id": "humanoid-1",
            "to_index": 650,
            "augmented_to_index": 400,
            "use_raw_depth": True,
            "outpaint_raw_depth": True,
        }
    )
    
    assert hasattr(response, "images")
    assert hasattr(response, "usage")
    
    # Save results
    results_dir = Path("tests") / "results"
    results_dir.mkdir(exist_ok=True)
    
    if isinstance(response.images, dict):
        for direction, base64_img in response.images.items():
            img = base64_img.pil_image()
            filename = direction.replace("-", "_")
            img.save(results_dir / f"8rotations_template_{filename}.png")


def test_rotate8_with_template_with_style():
    client = pixellab.Client.from_env_file(".env.development.secrets")
    
    response = client.rotate8_with_template(
        description="pirate captain character",
        image_size={"width": 48, "height": 48},
        text_guidance_scale=10.0,
        outline="thick",
        shading="hard",
        detail="medium",
        isometric=False,
    )
    
    assert hasattr(response, "images")
    assert hasattr(response, "usage")
    
    # Test the backwards compatibility property
    rotation_images = response.rotation_images
    assert hasattr(rotation_images, "south")
    assert hasattr(rotation_images, "north")
    assert hasattr(rotation_images, "east")
    assert hasattr(rotation_images, "west")
    assert hasattr(rotation_images, "south_east")
    assert hasattr(rotation_images, "north_east")
    assert hasattr(rotation_images, "south_west")
    assert hasattr(rotation_images, "north_west")
    
    # Save results
    results_dir = Path("tests") / "results"
    results_dir.mkdir(exist_ok=True)
    
    # Save using the rotation_images property
    rotation_images.south.pil_image().save(results_dir / "8rotations_styled_south.png")
    rotation_images.north.pil_image().save(results_dir / "8rotations_styled_north.png")
    rotation_images.east.pil_image().save(results_dir / "8rotations_styled_east.png")
    rotation_images.west.pil_image().save(results_dir / "8rotations_styled_west.png")