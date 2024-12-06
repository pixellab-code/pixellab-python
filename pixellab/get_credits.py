from __future__ import annotations

from typing import TYPE_CHECKING, Any

import requests
from pydantic import BaseModel

if TYPE_CHECKING:
    from .client import PixelLabClient


class CreditsResponse(BaseModel):
    credits: float


def get_credits(
    client: Any,
) -> CreditsResponse:
    """Get the current credit balance.

    Args:
        client: The PixelLab client instance

    Returns:
        CreditsResponse containing the current credit balance

    Raises:
        ValueError: If authentication fails
        requests.exceptions.HTTPError: For other HTTP-related errors
    """
    try:
        response = requests.get(
            f"{client.base_url}/credits",
            headers=client.headers(),
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            error_detail = response.json().get("detail", "Unknown error")
            raise ValueError(error_detail)
        raise

    return CreditsResponse(**response.json()) 