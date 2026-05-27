from __future__ import annotations

import uuid

import pytest

import pixellab


def test_get_background_job_unknown_id_raises():
    """Fetching a non-existent background job surfaces a ValueError."""
    client = pixellab.Client.from_env_file(".env.development.secrets")

    with pytest.raises(ValueError):
        client.get_background_job(str(uuid.uuid4()))
