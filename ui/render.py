from rich.console import Console
from rich.syntax import Syntax

from engine.contracts import Response, ResponseMode
from ui.style import C

console = Console()


def render(response: Response):
    sender = response.sender.lower()
    text = response.text
    mode = response.mode

    color = {
        "dominus": C.DOMINUS,
        "lucia": C.LUCIA,
        "system": C.SYSTEM,
    }.get(sender, C.RESET)

    if mode == ResponseMode.CODE:
        lang = "python"

        # remover marcação ``` se houver
        if text.startswith("```"):
            lines = text.splitlines()
            lang = lines[0].replace("```", "").lower()

            lines = lines[1:]
            if lines and lines[-1].strip().startswith("```"):
                lines = lines[:-1]

            text = "\n".join(lines)

        syntax = Syntax(
            text,
            lexer=lang,
            tab_size=2,
            line_numbers=False,
            background_color=None,
        )
        console.print(syntax)
    else:
        console.print(f"{color}{sender}: {C.RESET}{text}")
