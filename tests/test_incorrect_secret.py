import pytest
import pixellab


def test_incorrect_secret_raises_meaningful_error():
    client = pixellab.Client(
        secret="clearly wrong secret",
        base_url="http://localhost:8000/v1",
    )

    with pytest.raises(ValueError) as exc_info:
        client.generate_image_pixflux(
            description="cute dragon",
        )
    
    # Verify the error message is helpful
    error_msg = str(exc_info.value)
    print(error_msg)
    assert "Invalid API token" in error_msg
