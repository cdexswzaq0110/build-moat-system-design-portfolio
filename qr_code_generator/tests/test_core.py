from datetime import datetime, timedelta, timezone

import pytest

from app.repository import is_expired
from app.token_gen import generate_token
from app.url_validator import validate_url


def test_generate_token_is_url_safe() -> None:
    token = generate_token()

    assert len(token) == 8
    assert token.isalnum()


def test_validate_url_normalizes_fragment() -> None:
    assert validate_url("https://example.com/path#top") == "https://example.com/path"


def test_validate_url_blocks_localhost() -> None:
    with pytest.raises(ValueError):
        validate_url("http://localhost:8000/admin")


def test_expired_link_returns_true() -> None:
    link = {"expires_at": (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()}

    assert is_expired(link) is True
