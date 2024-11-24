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


# client = pixellab.Client(secret="my-secret")
# client = pixellab.Client.from_env()
client = pixellab.Client.from_env_file(".env.secrets")

# create image
response = client.generate_image_v6()

response.pil_image()
```

## Development

```bash
poetry install
```

### Run tests

```bash
poetry run pytest -s
```
