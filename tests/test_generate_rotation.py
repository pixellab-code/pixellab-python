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

def test_generate_rotation():
    client = pixellab.Client.from_env_file(".env.development.secrets")

    reference_image_data = encode_image_to_base64("tests/images/boy.png")

    response = client.generate_rotation(
        {
            "from_direction": "south",
            "from_view": "side",
            "to_direction": "east",
            "to_view": "side",
            "image_size": {"width": 16, "height": 16},
            "image_guidance_scale": 7.5,
            "from_image": {
                "type": "base64",
                "base64": reference_image_data,
            },
        }
    )


    response.image.pil_image()
