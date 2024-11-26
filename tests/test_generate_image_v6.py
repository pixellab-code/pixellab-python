import pixellab


def test_generate_image_v6():
    client = pixellab.Client.from_env_file(".env.development.secrets")

    response = client.generate_image_v6(
        {
            "description": "cute dragon",
            "image_size": {"width": 64, "height": 64},
            "no_background": False,
            "text_guidance_scale": 7.5,
        }
    )

    response.image.pil_image()
