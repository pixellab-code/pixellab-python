# Pixel Lab Python SDK

This Python client simplifies interaction with the [Pixel Lab developer API](http://api.pixellab.ai/v1).

Create characters and items, animate them, and generate rotated views. Useful for game development and other pixel art projects.

For questions or discussions, join us on [Discord](https://discord.gg/pBeyTBF8T7).

## Features

- **Generate Image (Pixflux)**: Create characters, items, and environments from text descriptions
- **Generate Image (Bitforge)**: Use reference images to match a specific art style
- **Animation**: Animate bi-pedal and quadrupedal characters and monsters with skeleton-based animations
- **Inpainting**: Edit existing pixel art
- **Rotation**: Generate rotated views of characters and objects

With much more functionality coming soon.

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
