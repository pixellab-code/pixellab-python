from __future__ import annotations

from pathlib import Path

import PIL.Image
import pytest

import pixellab


def test_rotate4_with_template_basic():
    client = pixellab.Client.from_env_file(".env.development.secrets")
    
    response = client.rotate4_with_template(
        description="cute wizard",
        image_size={"width": 48, "height": 48},
        text_guidance_scale=12.0,
    )
    
    # Check response structure
    assert hasattr(response, "images")
    assert hasattr(response, "usage")
    
    # Check that we got all 4 directions
    if isinstance(response.images, dict):
        assert "south" in response.images
        assert "west" in response.images
        assert "east" in response.images
        assert "north" in response.images
    else:
        assert hasattr(response.images, "south")
        assert hasattr(response.images, "west")
        assert hasattr(response.images, "east")
        assert hasattr(response.images, "north")
    
    # Save results
    results_dir = Path("tests") / "results" 
    results_dir.mkdir(exist_ok=True)
    
    if isinstance(response.images, dict):
        for direction, base64_img in response.images.items():
            img = base64_img.pil_image()
            img.save(results_dir / f"4rotations_basic_{direction}.png")
    else:
        response.images.south.pil_image().save(results_dir / "4rotations_basic_south.png")
        response.images.west.pil_image().save(results_dir / "4rotations_basic_west.png")
        response.images.east.pil_image().save(results_dir / "4rotations_basic_east.png")
        response.images.north.pil_image().save(results_dir / "4rotations_basic_north.png")


def test_rotate4_with_template_with_template():
    client = pixellab.Client.from_env_file(".env.development.secrets")
    
    response = client.rotate4_with_template(
        description="futuristic robot warrior",
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
    
    # Check response
    assert hasattr(response, "images")
    assert hasattr(response, "usage")
    
    # Save results
    results_dir = Path("tests") / "results"
    results_dir.mkdir(exist_ok=True)
    
    if isinstance(response.images, dict):
        for direction, base64_img in response.images.items():
            img = base64_img.pil_image()
            img.save(results_dir / f"4rotations_template_{direction}.png")


def test_rotate4_with_template_with_style():
    client = pixellab.Client.from_env_file(".env.development.secrets")
    
    response = client.rotate4_with_template(
        description="medieval knight warrior",
        image_size={"width": 64, "height": 64},
        text_guidance_scale=8.0,
        outline="medium",
        shading="soft",
        detail="high",
        view="low top-down",
    )
    
    assert hasattr(response, "images")
    assert hasattr(response, "usage")
    
    # Save results
    results_dir = Path("tests") / "results"
    results_dir.mkdir(exist_ok=True)
    
    if isinstance(response.images, dict):
        for direction, base64_img in response.images.items():
            img = base64_img.pil_image()
            img.save(results_dir / f"4rotations_styled_{direction}.png")


def test_rotate4_with_template_response_structure():
    """Test that response structure works correctly"""
    client = pixellab.Client.from_env_file(".env.development.secrets")
    
    response = client.rotate4_with_template(
        description="space astronaut",
        image_size={"width": 32, "height": 32},
        text_guidance_scale=8.0,
    )
    
    assert hasattr(response, "images")
    assert hasattr(response, "usage")
    
    # The response handler converts dict to RotationImages for consistency
    # Use the rotation_images property for backwards compatibility
    rotation_images = response.rotation_images
    assert hasattr(rotation_images, "south")
    assert hasattr(rotation_images, "west")
    assert hasattr(rotation_images, "east")
    assert hasattr(rotation_images, "north")
    
    # All images should be Base64Image objects
    assert rotation_images.south.pil_image().size == (32, 32)
    assert rotation_images.west.pil_image().size == (32, 32)