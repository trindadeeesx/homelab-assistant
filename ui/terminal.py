from agents.intents import intents_definition
from engine.engine import Engine
from router import Router
from ui.render import render
from ui.style import C


def start():
    engine = Engine(Router())

    print(f"{C.SYSTEM}Dominus & Lucia — terminal{C.RESET}")
    print(f"{C.SYSTEM}Digite ':q' para sair{C.RESET}\n")

    while True:
        try:
            user_input = input(f"{C.PROMPT}>>> {C.RESET}").strip()
        except KeyboardInterrupt:
            print()
            break

        if user_input == ":q":
            break

        responses = engine.handle(user_input)

        for r in responses:
            render(r)
