from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Optional

import requests
from pydantic import BaseModel

if TYPE_CHECKING:
    from .client import PixelLabClient


class Credits(BaseModel):
    type: Literal["usd"] = "usd"
    usd: float


class Subscription(BaseModel):
    type: Literal["generations"] = "generations"
    status: str
    plan: Optional[str] = None
    generations: float
    total: float


class BalanceResponse(BaseModel):
    credits: Credits
    subscription: Subscription


def get_balance(
    client: Any,
) -> BalanceResponse:
    """Get the current account balance.

    Args:
        client: The PixelLab client instance

    Returns:
        BalanceResponse with USD ``credits`` and ``subscription`` generation
        balance.

    Raises:
        ValueError: If authentication fails
        requests.exceptions.HTTPError: For other HTTP-related errors
    """
    try:
        response = requests.get(
            f"{client.base_url}/v2/balance",
            headers=client.headers(),
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            error_detail = response.json().get("detail", "Unknown error")
            raise ValueError(error_detail)
        raise

    return BalanceResponse(**response.json())
