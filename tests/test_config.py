"""Tests for config.py"""

import io
import os

from bareasgi_auth_server_ldap.config import Config


def test_can_expand_vars():
    text = """
app:
  host: ${APP_HOST}
  port: ${APP_PORT}
  tls:
    is_enabled: ${APP_TLS_IS_ENABLED}
    certfile: ${APP_TLS_CERTFILE}
    keyfile: ${APP_TLS_KEYFILE}
  path_prefix: ${APP_PATH_PREFIX}

cookie:
  name: ${COOKIE_NAME}
  domain: ${COOKIE_DOMAIN}
  path: ${COOKIE_PATH}
  expiry: ${COOKIE_EXPIRY}

jwt:
  secret: ${JWT_SECRET}
  issuer: ${JWT_ISSUER}
  expiry: ${JWT_EXPIRY}

ldap:
  url: ${LDAP_URL}
  base: ${LDAP_BASE}
  username: ${LDAP_USERNAME}
  password: ${LDAP_PASSWORD}

log:
  version: 1
  formatters:
    simple:
      format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  handlers:
    console:
      class: logging.StreamHandler
      formatter: simple
      stream: ext://sys.stdout
  loggers:
    bareasgi_auth_server:
      level: ${LOG_LEVEL}
      handlers:
        - console
      propagate: false
  root:
    level: ${LOG_ROOT_LEVEL}
    handlers:
      - console
"""

    env = {
        "APP_HOST": "0.0.0.0",
        "APP_PORT": "10001",
        "APP_TLS_IS_ENABLED": "true",
        "APP_TLS_CERTFILE": "~/.keys/server.crt",
        "APP_TLS_KEYFILE": "~/.keys/server.key",
        "APP_PATH_PREFIX": "/auth/api",
        "COOKIE_NAME": "bareasgi-auth-ldap",
        "COOKIE_DOMAIN": "example.com",
        "COOKIE_EXPIRY": "PT1H",
        "JWT_SECRET": "A secret of more than 15 characters",
        "JWT_ISSUER": "example.com",
        "JWT_EXPIRY": "P1D",
        "LDAP_URL": "ldaps://ldap.example.com",
        "LDAP_BASE": "dc=example,dc=org",
        "LDAP_USERNAME": "cn=admin,dc=example,dc=org",
        "LDAP_PASSWORD": "password",
        "LOG_LEVEL": "DEBUG",
        "LOG_ROOT_LEVEL": "INFO"
    }
    for key, value in env.items():
        os.environ[key] = value

    fp = io.StringIO(text)

    config = Config.load(fp)

    assert config is not None
