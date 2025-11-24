from __future__ import annotations

from pathlib import Path

import PIL.Image
import pytest

import pixellab


def test_animate_with_template_basic():
    client = pixellab.Client.from_env_file(".env.development.secrets")
    
    response = client.animate_with_template(
        description="human warrior",
        action="walk",
        image_size={"width": 32, "height": 32},
        n_frames=4,  # Explicitly set to 4
        text_guidance_scale=8.0,
        view="low top-down",
        direction="south",
        seed=0,
    )
    
    # Check response structure
    assert hasattr(response, "images")
    assert hasattr(response, "frame_count")
    assert hasattr(response, "spritesheet")
    assert hasattr(response, "usage")
    
    # Check that images is a list
    assert isinstance(response.images, list)
    assert len(response.images) == response.frame_count
    assert response.frame_count == 4
    
    # Save results
    results_dir = Path("tests") / "results" 
    results_dir.mkdir(exist_ok=True)
    
    # Save individual frames
    for i, base64_img in enumerate(response.images):
        img = base64_img.pil_image()
        assert img.size == (32, 32)
        img.save(results_dir / f"animation_basic_frame_{i}.png")
    
    # Save spritesheet if present
    if response.spritesheet:
        spritesheet = response.spritesheet.pil_image()
        spritesheet.save(results_dir / "animation_basic_spritesheet.png")


def test_animate_with_template_with_template_reference():
    client = pixellab.Client.from_env_file(".env.development.secrets")
    
    # Test with template reference
    response = client.animate_with_template(
        description="wizard walking",
        action="walk",
        image_size={"width": 48, "height": 48},
        n_frames=None,  # Let it match the template frame count
        text_guidance_scale=10.0,
        view="low top-down",
        direction="south",
        reference={
            "type": "template",
            "template_id": "humanoid-1",
            "to_index": 650,
            "augmented_to_index": 400,
        },
        template_animation_id="walking-432",  # Try a different walking animation
    )
    
    # Check response
    assert hasattr(response, "images")
    assert hasattr(response, "frame_count")
    assert hasattr(response, "usage")
    
    assert isinstance(response.images, list)
    assert len(response.images) == response.frame_count
    assert response.frame_count >= 1  # Template determines frame count
    
    # Save results
    results_dir = Path("tests") / "results"
    results_dir.mkdir(exist_ok=True)
    
    for i, base64_img in enumerate(response.images):
        img = base64_img.pil_image()
        assert img.size == (48, 48)
        img.save(results_dir / f"animation_template_frame_{i}.png")