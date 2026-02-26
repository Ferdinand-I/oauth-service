import secrets
from typing import Annotated

from fastapi import Query, Depends, HTTPException

from api.deps.auth import state_cookie_scheme


def validate_oauth_state(
    query_state: Annotated[str, Query(alias="state")],
    cookie_state: Annotated[str, Depends(state_cookie_scheme)],
) -> None:
    """Validate OAuth state parameter against cookie to prevent CSRF attacks."""

    if not secrets.compare_digest(query_state, cookie_state):
        raise HTTPException(status_code=400, detail="Invalid state")


validate_google_oauth_state = validate_oauth_state
validate_yandex_oauth_state = validate_oauth_state
