
import pixellab
import dotenv


def test_client_from_env_file():
    client = pixellab.Client.from_env_file(".env.development.secrets")

    assert client.secret is not None


def test_client_from_env():
    dotenv.load_dotenv(".env.development.secrets")

    client = pixellab.Client.from_env()

    assert client.secret is not None
