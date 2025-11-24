from __future__ import annotations

from pathlib import Path

import PIL.Image
import pytest

import pixellab


def test_generate_tileset_basic():
    client = pixellab.Client.from_env_file(".env.development.secrets")
    
    response = client.generate_tileset(
        inner_description="grass field",
        outer_description="forest",
        image_size={"width": 32, "height": 32},
        tile_size={"width": 8, "height": 8},
        transition_description="edge between grass and trees",
        transition_size=0.0,
        text_guidance_scale=8.0,
        view="high top-down",
        seed=0,
    )
    
    # Check response structure
    assert hasattr(response, "image")
    assert hasattr(response, "usage")
    
    # Check that image is a Base64Image
    assert hasattr(response.image, "base64")
    assert hasattr(response.image, "format")
    
    # Save result
    results_dir = Path("tests") / "results" 
    results_dir.mkdir(exist_ok=True)
    
    img = response.image.pil_image()
    assert img.size == (32, 32)
    img.save(results_dir / "tileset_basic.png")


def test_generate_tileset_with_style():
    client = pixellab.Client.from_env_file(".env.development.secrets")
    
    response = client.generate_tileset(
        inner_description="water",
        outer_description="sand beach",
        image_size={"width": 64, "height": 64},
        tile_size={"width": 16, "height": 16},
        transition_description="waves and foam",
        transition_size=0.2,
        text_guidance_scale=10.0,
        outline="single color outline",
        shading="flat shading",
        detail="medium detail",
        view="low top-down",
    )
    
    # Check response
    assert hasattr(response, "image")
    assert hasattr(response, "usage")
    
    # Save result
    results_dir = Path("tests") / "results"
    results_dir.mkdir(exist_ok=True)
    
    img = response.image.pil_image()
    assert img.size == (64, 64)
    img.save(results_dir / "tileset_styled.png")


def test_generate_tileset_minimal():
    """Test with minimal parameters"""
    client = pixellab.Client.from_env_file(".env.development.secrets")
    
    response = client.generate_tileset(
        inner_description="stone floor",
        outer_description="dirt path",
        image_size={"width": 32, "height": 32},
    )
    
    # Check response
    assert hasattr(response, "image")
    assert hasattr(response, "usage")
    
    # Should use the specified size
    img = response.image.pil_image()
    assert img.size == (32, 32)
    
    # Save result
    results_dir = Path("tests") / "results"
    results_dir.mkdir(exist_ok=True)
    img.save(results_dir / "tileset_minimal.png")


def test_generate_tileset_seamless():
    """Test seamless tileset generation"""
    client = pixellab.Client.from_env_file(".env.development.secrets")
    
    response = client.generate_tileset(
        inner_description="lava",
        outer_description="volcanic rock",
        image_size={"width": 64, "height": 64},
        tile_size={"width": 16, "height": 16},
        transition_description="cooling lava and cracks",
        transition_size=0.3,
        text_guidance_scale=12.0,
        seed=42,
    )
    
    # Check response
    assert hasattr(response, "image")
    assert hasattr(response, "usage")
    
    img = response.image.pil_image()
    assert img.size == (64, 64)
    
    # Save result
    results_dir = Path("tests") / "results"
    results_dir.mkdir(exist_ok=True)
    img.save(results_dir / "tileset_seamless.png")