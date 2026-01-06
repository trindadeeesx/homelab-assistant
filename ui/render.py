from enum import Enum

from rich.console import Console

from engine.contracts import Response, ResponseMode
from ui.style import C

console = Console()


def render(response: Response):
    color = {
        "dominus": C.DOMINUS,
        "lucia": C.LUCIA,
        "system": C.SYSTEM,
    }.get(response.sender, C.RESET)

    name = response.sender.capitalize()

    print(f"{color}{name}:{C.RESET} {response.text}")
