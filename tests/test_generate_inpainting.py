import pixellab
import base64
import PIL.Image
from io import BytesIO

def encode_image_to_base64(file_path: str) -> str:
    with open(file_path, "rb") as image_file:
        image = PIL.Image.open(image_file)
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

def test_generate_image_v5():
    client = pixellab.Client.from_env_file(".env.development.secrets")

    def encode_image_to_base64(file_path: str) -> str:
        with open(file_path, "rb") as image_file:
            image = PIL.Image.open(image_file)
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode("utf-8")

    inpainting_image_data = encode_image_to_base64("tests/images/boy.png")
    mask_image_data = encode_image_to_base64("tests/images/mask.png")

    response = client.generate_image_v5(
        {
            "description": "boy with wings",
            "image_size": {"width": 16, "height": 16},
            "no_background": True,
            "inpainting_image": {
                "type": "base64",
                "base64": inpainting_image_data,
            },
            "mask_image": {
                "type": "base64",
                "base64": mask_image_data,
            },
        }
    )
