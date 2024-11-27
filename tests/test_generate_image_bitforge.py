from __future__ import annotations
from pathlib import Path
import pixellab
import base64
import PIL.Image
from io import BytesIO
from pixellab.models import Base64Image, ImageSize


def encode_image_to_base64(file_path: Path | str) -> str:
    with open(file_path, "rb") as image_file:
        image = PIL.Image.open(image_file)
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")


def test_generate_image_bitforge():
    client = pixellab.Client.from_env_file(".env.development.secrets")

    # Use pathlib for file paths
    images_dir = Path("tests") / "images"
    inpainting_image_data = encode_image_to_base64(images_dir / "boy.png")
    style_image_data = encode_image_to_base64(images_dir / "boy.png")
    mask_image_data = encode_image_to_base64(images_dir / "mask.png")

    response = client.generate_image_bitforge(
        description="boy with wings",
        image_size=ImageSize(width=16, height=16),
        no_background=True,
        style_image=Base64Image(base64=style_image_data),
        inpainting_image=Base64Image(base64=inpainting_image_data),
        mask_image=Base64Image(base64=mask_image_data),
    )

    # Verify we got a valid image back
    image = response.image.pil_image()
    assert isinstance(image, PIL.Image.Image)
    assert image.size == (16, 16)

    # Create results directory using pathlib
    results_dir = Path("tests") / "results"
    results_dir.mkdir(exist_ok=True)

    # Save the generated image using pathlib
    image.save(results_dir / "bitforge_boy_with_wings.png")
