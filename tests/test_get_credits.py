import pixellab


def test_get_credits():
    client = pixellab.Client.from_env_file(".env.development.secrets")
    
    response = client.get_credits()
    
    print(f"Credits: {response.credits}")
    assert isinstance(response.credits, float)
    assert response.credits >= 0 