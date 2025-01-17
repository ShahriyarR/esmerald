from typing import List

from starlette.middleware import Middleware as StarletteMiddleware

from esmerald import Esmerald, EsmeraldAPISettings
from esmerald.middleware import HTTPSRedirectMiddleware
from esmerald.types import Middleware

routes = [...]

# Option one
middleware = [StarletteMiddleware(HTTPSRedirectMiddleware)]

app = Esmerald(routes=routes, middleware=middleware)


# Option two - Using the settings module
# Running the application with your custom settings -> ESMERALD_SETTINGS_MODULE
class AppSettings(EsmeraldAPISettings):
    @property
    def middleware(self) -> List["Middleware"]:
        # There is no need to wrap in a StarletteMiddleware here.
        # Esmerald automatically will do it once the application is up and running.
        return [HTTPSRedirectMiddleware]
