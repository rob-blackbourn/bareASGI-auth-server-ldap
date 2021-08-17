"""
Application
"""

from bareasgi import Application
from bareasgi_cors import CORSMiddleware
from bareasgi_auth_common import JwtAuthenticator
from bareasgi_auth_common import TokenManager
from bareasgi_auth_server.auth_controller import AuthController
from .ldap_auth_service import LdapAuthService
from .config import Config


def make_application(config: Config) -> Application:
    cors_middleware = CORSMiddleware()

    app = Application(middlewares=[cors_middleware])

    auth_service = LdapAuthService(
        config.ldap.url,
        config.ldap.username,
        config.ldap.password,
        config.ldap.base
    )
    token_manager = TokenManager(
        config.token.secret,
        config.token.lease_expiry,
        config.token.issuer,
        config.cookie.name,
        config.cookie.domain,
        config.cookie.path,
        config.token.session_expiry
    )

    token_renewal_path = config.app.path_prefix + config.token.renewal_path
    authenticator = JwtAuthenticator(token_renewal_path, token_manager)

    auth_controller = AuthController(
        config.app.path_prefix,
        authenticator,
        auth_service,
    )

    auth_controller.add_routes(app)

    return app
