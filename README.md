# Pixel Lab Python SDK

[![PyPI version](https://badge.fury.io/py/pixellab.svg)](https://badge.fury.io/py/pixellab)
[![Python](https://img.shields.io/pypi/pyversions/pixellab.svg)](https://pypi.org/project/pixellab/)

This Python client simplifies interaction with the [Pixel Lab developer API](http://api.pixellab.ai/v1).

Create characters and items, animate them, and generate rotated views. Useful for game development and other pixel art projects.

For questions or discussions, join us on [Discord](https://discord.gg/pBeyTBF8T7).

## Features

- **Generate Image (Pixflux)**: Create characters, items, and environments from text descriptions
- **Generate Image (Bitforge)**: Use reference images to match a specific art style
- **Animation with Text**: Animate with text prompts
- **Animation with Templates**: Generate animations using pre-made templates for consistent character movements
- **Animation with Skeletons**: Animate bi-pedal and quadrupedal characters and monsters with skeleton-based animations
- **Estimate Skeleton**: Estimate skeletons from images
- **Inpainting**: Edit existing pixel art
- **Rotation**: Generate rotated views of characters and objects
- **Generate Tileset**: Create cohesive tilesets for game environments
- **Generate 4 Rotations**: Generate 4 directional views (north, south, east, west) of characters
- **Generate 8 Rotations**: Generate 8 directional views including diagonals

## Installation

Use your preferred package manager:

```bash
pip install pixellab
```

or

```bash
poetry add pixellab
```

## Usage

```python
import pixellab

client = pixellab.Client.from_env_file(".env.development.secrets")
# client = pixellab.Client.from_env()
# client = pixellab.Client(secret="my-secret")

# create image
response = client.generate_image_pixflux(
    description="cute dragon",
    image_size = {"width": 64, "height": 64},
)

response.image.pil_image()

# animate with template
animation_response = client.animate_with_template(
    description="wizard character",
    action="walk",
    image_size={"width": 64, "height": 64},
    reference={
        "type": "template",
        "template_id": "humanoid-1",
    },
    template_animation_id="walking-432",
)

# save animation frames
for i, frame in enumerate(animation_response.images):
    frame.pil_image().save(f"wizard_walk_{i}.png")
```

See more client usage examples in the [Pixel Lab API Docs](https://api.pixellab.ai/v1/docs).

## Development

### Install Dependencies

```bash
poetry install
```

### Run Tests

```bash
poetry run pytest -s
```

## Support

- Documentation: [api.pixellab.ai/v1/docs](https://api.pixellab.ai/v1/docs)
- Discord Community: [Join us](https://discord.gg/pBeyTBF8T7)
- Issues: Please report any SDK issues on our GitHub repository
