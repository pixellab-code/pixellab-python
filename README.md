# Pixel Lab Python SDK

[Pixel Lab](http://www.pixellab.ai) is a pixel art extension for Aseprite designed to provide artists and game developers with controllable AI tools that integrate into their workflow. This Python client simplifies interaction with the [Pixel Lab developer API](http://api.pixellab.ai/v1).

For questions or discussions, feel free to join us at [Discord](https://discord.gg/pBeyTBF8T7).

## Supported models

- **Generate Image Bitforge**: Apply custom art styles using reference images.
- **Generate Image Pixflux**: Generate pixel art from text descriptions.
- **Animate (skeleton)**: Generate 4 frames of an animation from skeleton poses.
- **Inpaint**: Edit and modify existing pixel art.
- **Rotate**: Rotate an object or a character.

## Install

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

## Development

### Install dependencies

```bash
poetry install
```

### Run tests

```bash
poetry run pytest -s
```
