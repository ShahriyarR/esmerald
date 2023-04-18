import inspect
import os
import sys
from typing import Any, Optional

import click
from rich.console import Console
from rich.table import Table

from esmerald import Gateway
from esmerald.core.directives.constants import ESMERALD_DISCOVER_APP
from esmerald.core.directives.env import DirectiveEnv
from esmerald.core.terminal import OutputColour, Print, Terminal
from esmerald.enums import HttpMethod
from esmerald.utils.url import clean_path

printer = Print()
writer = Terminal()
console = Console()

DOCS_ELEMENTS = [
    "/swagger",
    "/redoc",
    "/openapi.json",
    "/openapi.yaml",
    "/openapi.yml",
    "/elements",
]


def get_http_verb(mapping: Any) -> str:
    if getattr(mapping, "get", None):
        return HttpMethod.GET.value
    elif getattr(mapping, "post", None):
        return HttpMethod.POST.value
    elif getattr(mapping, "put", None):
        return HttpMethod.PUT.value
    elif getattr(mapping, "patch", None):
        return HttpMethod.PATCH.value
    elif getattr(mapping, "delete", None):
        return HttpMethod.DELETE.value
    elif getattr(mapping, "header", None):
        return HttpMethod.HEAD.value


@click.option("-v", "--verbosity", default=1, type=int, help="Displays the files generated")
@click.command(name="show_urls")
def show_urls(env: DirectiveEnv, verbosity: int) -> None:
    """Shows the information regarding the urls of a given application

    How to run: `esmerald show_urls`

    Example: `esmerald show_urls`
    """
    if os.getenv(ESMERALD_DISCOVER_APP) is None and getattr(env, "app", None) is None:
        error = (
            "You cannot specify a custom directive without specifying the --app or setting "
            "ESMERALD_DEFAULT_APP environment variable."
        )
        printer.write_error(error)
        sys.exit(1)

    app = env.app
    table = Table(title=app.app_name)
    table = get_routes_table(app, table)
    printer.write(table)


def get_routes_table(app, table: Table) -> None:
    """Prints the routing system"""
    table.add_column("Path", style=OutputColour.GREEN, vertical="center")
    table.add_column("Path Parameters", style=OutputColour.BRIGHT_CYAN, vertical="center")
    table.add_column("Name", style=OutputColour.CYAN, vertical="center")
    table.add_column("Type", style=OutputColour.YELLOW, vertical="center")
    table.add_column("HTTP Methods", style=OutputColour.RED, vertical="center")

    def parse_routes(app, table: table, route: Optional[Any] = None, prefix: Optional[str] = ""):
        if not app.routes:
            return

        for route in app.routes:
            if isinstance(route, Gateway):
                # Path
                path = clean_path(prefix + route.path)

                if any(element in path for element in DOCS_ELEMENTS):
                    continue

                # Type
                if inspect.iscoroutinefunction(route.handler.fn):
                    fn_type = "async"
                else:
                    fn_type = "sync"

                # Http methods
                http_methods = ", ".join(sorted(route.methods))
                parameters = ", ".join(sorted(route.stringify_parameters))
                table.add_row(path, parameters, route.name, fn_type, http_methods)
                continue

            route_app = getattr(route, "app", None)
            if not route_app:
                continue

            path = clean_path(prefix + route.path)
            if any(element in path for element in DOCS_ELEMENTS):
                continue

            parse_routes(route, table, prefix=f"{path}")

    parse_routes(app, table)
    return table
