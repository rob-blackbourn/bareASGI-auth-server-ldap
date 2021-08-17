"""Configuration"""

import os
from typing import Optional

from .utils import parse_duration


def _expand_path(path: Optional[str]) -> Optional[str]:
    return None if path is None else os.path.expanduser(path)


class AppConfig:

    def __init__(self) -> None:
        self.host = os.environ['APP_HOST']
        self.port = os.environ['APP_PORT']
        self.path_prefix = os.environ['APP_PATH_PREFIX']


class TlsConfig:

    def __init__(self) -> None:
        self.is_enabled = os.environ['APP_TLS_IS_ENABLED'].lower() in (
            'true', 'yes')
        self.certfile = _expand_path(os.environ.get('APP_TLS_CERTFILE'))
        self.keyfile = _expand_path(os.environ.get('APP_TLS_KEYFILE'))


class CookieConfig:

    def __init__(self) -> None:
        self.name = os.environ['COOKIE_NAME']
        self.domain = os.environ['COOKIE_DOMAIN']
        self.path = os.environ['COOKIE_PATH']


class TokenConfig:

    def __init__(self) -> None:
        self.secret = os.environ['TOKEN_SECRET']
        self.issuer = os.environ['TOKEN_ISSUER']
        self.lease_expiry = parse_duration(
            os.environ['TOKEN_LEASE_EXPIRY']
        )
        self.session_expiry = parse_duration(
            os.environ['TOKEN_SESSION_EXPIRY']
        )
        self.renewal_path = os.environ['TOKEN_RENEWAL_PATH']


class LdapConfig:

    def __init__(self) -> None:
        self.url = os.environ['LDAP_URL']
        self.base = os.environ['LDAP_BASE']
        self.username = os.environ['LDAP_USERNAME']
        self.password = os.environ['LDAP_PASSWORD']


class Config:

    def __init__(self) -> None:
        self.app = AppConfig()
        self.tls = TlsConfig()
        self.cookie = CookieConfig()
        self.token = TokenConfig()
        self.ldap = LdapConfig()
