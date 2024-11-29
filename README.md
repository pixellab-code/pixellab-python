# Pixel Lab Python SDK

Python client library for Pixel Lab. Designed to simplify and exemplify interaction with the developer API.

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
    image_size=dict(
        height=256,
        width=256,
    ),
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
