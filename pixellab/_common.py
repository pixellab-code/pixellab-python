"""Shared helpers for the v2 endpoint wrappers.

Centralises the request/response plumbing that every endpoint module needs:
the ``Usage`` model, consistent HTTP error translation, thin ``requests``
wrappers, and background-job polling for the asynchronous endpoints.
"""

from __future__ import annotations

import time
from typing import Any, Dict, Literal, Optional

import requests
from pydantic import BaseModel


class Usage(BaseModel):
    type: Literal["usd"] = "usd"
    usd: float


class BackgroundJobResponse(BaseModel):
    """Status of an asynchronous job returned by ``GET /background-jobs/{id}``."""

    id: str
    status: str
    created_at: str
    last_response: Optional[Dict[str, Any]] = None
    usage: Optional[Usage] = None


# Job statuses that mean the work is done (success / failure).
_DONE_STATUSES = {"completed", "complete", "done", "success", "succeeded", "finished"}
_FAILED_STATUSES = {"failed", "error", "errored", "cancelled", "canceled"}


def raise_for_status(response: requests.Response) -> None:
    """Translate HTTP errors into ``ValueError`` with the API's ``detail`` message.

    Mirrors the error handling used across the existing endpoint modules so the
    new wrappers behave consistently for callers.
    """
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text or "Unknown error"

        status = response.status_code
        if status == 401:
            raise ValueError(f"Authentication failed: {detail}")
        if status == 402:
            raise ValueError(f"Payment required: {detail}")
        if status == 429:
            raise ValueError(f"Rate limit exceeded: {detail}")
        if status in (400, 403, 404, 409, 422):
            raise ValueError(detail)
        if status >= 500:
            raise ValueError(f"Server error: {detail}")
        raise


def post(client: Any, path: str, json: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post(
        f"{client.base_url}/v2/{path}",
        headers=client.headers(),
        json=json,
    )
    raise_for_status(response)
    return response.json()


def get(
    client: Any, path: str, params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    response = requests.get(
        f"{client.base_url}/v2/{path}",
        headers=client.headers(),
        params=params,
    )
    raise_for_status(response)
    return response.json()


def delete(client: Any, path: str) -> Dict[str, Any]:
    response = requests.delete(
        f"{client.base_url}/v2/{path}",
        headers=client.headers(),
    )
    raise_for_status(response)
    if response.content:
        try:
            return response.json()
        except ValueError:
            return {}
    return {}


def patch(client: Any, path: str, json: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.patch(
        f"{client.base_url}/v2/{path}",
        headers=client.headers(),
        json=json,
    )
    raise_for_status(response)
    return response.json()


def get_background_job(client: Any, job_id: str) -> BackgroundJobResponse:
    """Fetch the current status of a background job."""
    return BackgroundJobResponse(**get(client, f"background-jobs/{job_id}"))


def wait_for_background_job(
    client: Any,
    job_id: str,
    polling_interval: float = 5.0,
    max_polling_time: float = 500.0,
) -> BackgroundJobResponse:
    """Poll a background job until it completes, fails, or times out.

    Returns the final :class:`BackgroundJobResponse`. Raises ``ValueError`` if
    the job fails and ``TimeoutError`` if it does not finish in time.
    """
    start = time.time()
    while True:
        job = get_background_job(client, job_id)
        status = (job.status or "").lower()
        if status in _DONE_STATUSES:
            return job
        if status in _FAILED_STATUSES:
            last = job.last_response or {}
            message = last.get("detail") or last.get("error") or "Unknown error"
            raise ValueError(f"Background job {job_id} failed: {message}")
        if time.time() - start >= max_polling_time:
            raise TimeoutError(
                f"Background job {job_id} did not finish within {max_polling_time}s"
            )
        time.sleep(polling_interval)
