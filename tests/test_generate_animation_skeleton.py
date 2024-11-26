import pixellab
import base64
import PIL.Image
import json
from io import BytesIO

def encode_image_to_base64(file_path: str) -> str:
    with open(file_path, "rb") as image_file:
        image = PIL.Image.open(image_file)
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

def test_generate_animation_skeleton():
    client = pixellab.Client.from_env_file(".env.development.secrets")

    reference_image_data = encode_image_to_base64("tests/images/boy.png")
    freeze_mask_data = encode_image_to_base64("tests/images/freeze_mask.png")

    # Load key points from walk.json
    with open("tests/skeleton_points/walk.json", "r") as file:
        skeleton_keypoints = json.load(file)["pose_keypoints"]

    response = client.generate_animation_skeleton(
        {
            "view": "side",
            "direction": "south",
            "image_size": {"width": 16, "height": 16},
            "reference_image": {
                "type": "base64",
                "base64": reference_image_data,
            },
            "animation_images": [
                {
                    "type": "base64",
                    "base64": reference_image_data,
                },
                None,
                None,
                None
            ],
            "mask_images": [
                {
                    "type": "base64",
                    "base64": freeze_mask_data,
                },
                None,
                None,
                None
            ],
            "skeleton_keypoints": skeleton_keypoints,  # Add key points to the request
        }
    )

    for image in response.images:
        image.pil_image()
