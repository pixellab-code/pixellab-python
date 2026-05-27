import pixellab


def test_get_credits():
    client = pixellab.Client.from_env_file(".env.development.secrets")

    response = client.get_balance()

    assert response.credits.type == "usd"
    assert isinstance(response.credits.usd, float)
    assert response.credits.usd >= 0

    assert isinstance(response.subscription.generations, float)
    assert isinstance(response.subscription.total, float)
    assert isinstance(response.subscription.status, str)

    print(
        f"Credits: ${response.credits.usd} | "
        f"Generations: {response.subscription.generations}/{response.subscription.total}"
    )
