#%%
import pixellab

client = pixellab.Client.from_env_file(".env.development.secrets")

# create image
response = client.generate_image_pixflux(
    {
        "description": "cute dragon",
        "negative_description": "",
        "image_size": {"width": 64, "height": 64},
        "no_background": True,
        "text_guidance_scale": 7.5,
    }
)

response.image.pil_image()

# %%
import pixellab
import base64
import PIL.Image
from io import BytesIO

client = pixellab.Client.from_env_file(".env.development.secrets")

with open("tests/images/boy.png", "rb") as image_file:
    image = PIL.Image.open(image_file)
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    reference_image_data = base64.b64encode(buffered.getvalue()).decode("utf-8")

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

# %%
import pixellab
import base64
import PIL.Image
from io import BytesIO

client = pixellab.Client.from_env_file(".env.development.secrets")

def encode_image_to_base64(file_path: str) -> str:
    with open(file_path, "rb") as image_file:
        image = PIL.Image.open(image_file)
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

inpainting_image_data = encode_image_to_base64("tests/images/boy.png")
style_image_data = encode_image_to_base64("tests/images/boy.png")
mask_image_data = encode_image_to_base64("tests/images/mask.png")

response = client.generate_image_v5(
    {
        "description": "boy with wings",
        "image_size": {"width": 16, "height": 16},
        "no_background": True,
        "style_image": {
            "type": "base64",
            "base64": style_image_data,
        },
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

response.image.pil_image()

# %%
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

# %%
import pixellab
import base64
import PIL.Image
from io import BytesIO

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

response.image.pil_image()
# %%
