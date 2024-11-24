import pixellab


def test_generate_image_v6():
    client = pixellab.Client.from_env_file(".env.development.secrets")

    response = client.generate_image_v6(prompt="A beautiful landscape")

    response.image.pil_image()
