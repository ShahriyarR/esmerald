from starlette.middleware import Middleware as StarletteMiddleware

from esmerald import Gateway, JSONResponse, Request, get, settings
from esmerald.conf import settings
from esmerald.middleware import RequestSettingsMiddleware
from esmerald.testclient import create_client


def test_default_settings():

    with create_client([]) as client:
        assert client.app.settings.app_name == settings.app_name
        assert client.app.settings.environment == "testing"
        assert client.app.settings.debug == settings.debug
        assert client.app.settings.allowed_hosts == settings.allowed_hosts
        assert client.app.settings.enable_sync_handlers == settings.enable_sync_handlers
        assert client.app.settings.enable_openapi == settings.enable_openapi
        assert client.app.settings.allow_origins == settings.allow_origins
        assert client.app.settings.on_shutdown == settings.on_shutdown
        assert client.app.settings.on_startup == settings.on_startup
        assert client.app.settings.on_startup == settings.on_startup
        assert client.app.settings.lifespan == settings.lifespan
        assert client.app.settings.on_startup == settings.on_startup
        assert client.app.settings.version == settings.version
        assert client.app.settings.secret_key == settings.secret_key
        assert client.app.settings.response_class == settings.response_class
        assert client.app.settings.response_cookies == settings.response_cookies
        assert client.app.settings.tags == settings.tags
        assert client.app.settings.include_in_schema == settings.include_in_schema
        assert client.app.settings.scheduler_class == settings.scheduler_class
        assert client.app.settings.reload == settings.reload
        assert client.app.settings.password_hashers == settings.password_hashers
        assert client.app.settings.csrf_config == settings.csrf_config
        assert client.app.settings.async_exit_config == settings.async_exit_config
        assert client.app.settings.template_config == settings.template_config
        assert client.app.settings.static_files_config == settings.static_files_config
        assert client.app.settings.cors_config == settings.cors_config
        assert client.app.settings.session_config == settings.session_config
        assert client.app.settings.openapi_config == settings.openapi_config
        assert client.app.settings.middleware == settings.middleware
        assert client.app.settings.permissions == settings.permissions
        assert client.app.settings.dependencies == settings.dependencies
        assert client.app.settings.exception_handlers == settings.exception_handlers
        assert client.app.settings.redirect_slashes == settings.redirect_slashes


@get("/request-settings")
async def _request_settings(request: Request) -> str:
    return request.settings.app_name


@get("/app-settings")
async def _app_settings(request: Request) -> str:
    return request.app.settings.app_name


def test_settings_global():
    """
    Tests settings are setup properly
    """
    with create_client(
        app_name="my app",
        routes=[Gateway(handler=_request_settings), Gateway(handler=_app_settings)],
        middleware=[StarletteMiddleware(RequestSettingsMiddleware)],
    ) as client:
        request_settings = client.get("/request-settings")
        app_settings = client.get("/app-settings")

        assert settings.app_name == "my app"
        assert client.app.app_name == "my app"
        assert request_settings.json() == "my app"
        assert app_settings.json() == "my app"


def test_settings_global_without_parameters():
    with create_client(
        routes=[Gateway(handler=_request_settings), Gateway(handler=_app_settings)],
        middleware=[StarletteMiddleware(RequestSettingsMiddleware)],
    ) as client:
        request_settings = client.get("/request-settings")
        app_settings = client.get("/app-settings")

        assert settings.app_name == "test_client"
        assert client.app.app_name == "test_client"
        assert request_settings.json() == "test_client"
        assert app_settings.json() == "test_client"


def test_adding_middlewares():
    @get("/request-settings")
    async def _request_settings(request: Request) -> JSONResponse:
        return JSONResponse(
            {"middleware": [middleware.cls.__name__ for middleware in request.settings.middleware]}
        )

    @get("/app-settings")
    async def _app_settings(request: Request) -> str:
        return JSONResponse(
            {
                "middleware": [
                    middleware.cls.__name__ for middleware in request.app.settings.middleware
                ]
            }
        )

    with create_client(
        routes=[Gateway(handler=_request_settings), Gateway(handler=_app_settings)],
        middleware=[StarletteMiddleware(RequestSettingsMiddleware)],
    ) as client:
        request_settings = client.get("/request-settings")
        app_settings = client.get("/app-settings")

        assert RequestSettingsMiddleware == settings.middleware[0].cls
        assert RequestSettingsMiddleware == client.app.middleware[0].cls
        assert "RequestSettingsMiddleware" == request_settings.json()["middleware"][0]
        assert "RequestSettingsMiddleware" == app_settings.json()["middleware"][0]
