import pixellab


def test_get_credits():
    client = pixellab.Client.from_env_file(".env.development.secrets")
    
    response = client.get_balance()
    
    print(f"Balance: {response.usd}")
    assert isinstance(response.usd, float)
    assert response.usd >= 0
