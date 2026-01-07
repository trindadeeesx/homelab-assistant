import os
from collections import deque

from dotenv import load_dotenv

from engine.engine import Engine
from global_commands import handle_global_command
from router import Router
from ui.render import render
from ui.style import C

load_dotenv()

admin_password = str(os.getenv("ADMIN_PASSWORD"))


def start():
    engine = Engine(Router())
    last_route = None
    history = deque(maxlen=50)

    os.system("clear")
    print(f"{C.SYSTEM}Dominus & Lucia — Terminal{C.RESET}")
    print(f"{C.SYSTEM}Digite ':q' para sair ou ':h' para ajuda.{C.RESET}\n")

    while True:
        try:
            user_input = input(f"{C.PROMPT}>>> {C.RESET}").strip()
        except KeyboardInterrupt:
            print()
            continue

        if not user_input:
            continue

        history.append(user_input)

        res = handle_global_command(
            user_input, engine, admin_password, last_route, history
        )
        if res == "exit":
            break
        elif res:
            continue

        responses = engine.handle(user_input)

        for r in responses:
            render(r)
