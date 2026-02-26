from typing import Final

# Cookie names
STATE_COOKIE_NAME: Final[str] = "oauth_state"
ACCESS_TOKEN_COOKIE_NAME: Final[str] = "access_token"  # Legacy, for backwards compatibility
GOOGLE_ACCESS_TOKEN_COOKIE_NAME: Final[str] = "google_access_token"
YANDEX_ACCESS_TOKEN_COOKIE_NAME: Final[str] = "yandex_access_token"

# Cookie expiration times (in seconds)
STATE_COOKIE_MAX_AGE: Final[int] = 600  # 10 minutes
ACCESS_TOKEN_COOKIE_MAX_AGE: Final[int] = 3600  # 1 hour
