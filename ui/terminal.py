import os
from getpass import getpass

from dotenv import load_dotenv

from agents.intents import intents_definition
from agents.intents.dominus_intents import DominusIntents
from agents.intents.intents import INTENT_REGISTRY
from engine.engine import Engine
from router import Router
from ui.render import render
from ui.style import C

load_dotenv()

admin_password = os.getenv("ADMIN_PASSWORD")


def start():
    engine = Engine(Router())
    last_route = None

    print(f"{C.SYSTEM}Dominus & Lucia — Terminal{C.RESET}")
    print(f"{C.SYSTEM}Digite ':q' para sair.{C.RESET}\n")
    print(f"{C.SYSTEM}Digite ':h' para mostrar ajuda.{C.RESET}\n")

    while True:
        try:
            user_input = input(f"{C.PROMPT}>>> {C.RESET}").strip()
        except KeyboardInterrupt:
            print()
            continue

        if not user_input:
            continue

        if user_input.lower() in [":q", ":quit", ":exit"]:
            break

        elif user_input.lower() in [":h", ":help"]:
            print()
            print(f"{C.SYSTEM}Comandos disponíveis:{C.RESET}")
            print(":q / :quit / :exit - Sair do terminal")
            print(":h / :help - Mostrar ajuda")
            print(":reload - Recarregar intents do Dominus")
            print(":intents - Listar todas intents registradas (ADMIN)")
            print(":debug - Informações de debug do sistema (ADMIN)")
            print(":routes - Mostrar rotas do Router para a última entrada (ADMIN)")
            print()
            continue

        elif user_input.lower() in [":r", ":reload"]:
            from importlib import reload

            from agents.intents import intents_definition

            reload(intents_definition)
            engine.dominus.intents = DominusIntents()
            print(f"{C.SUCCESS}✅ Dominus intents recarregadas{C.RESET}")
            continue

        elif user_input.lower() in [":intents", ":debug", ":routes"]:
            senha = getpass(f"{C.WARNING}Senha de ADMIN: {C.RESET}")
            if senha != admin_password:
                print(f"{C.ERROR}❌ Senha incorreta{C.RESET}")
                continue

            if user_input.lower() == ":intents":
                print(f"{C.SYSTEM}Intents registradas:{C.RESET}")
                for intent in INTENT_REGISTRY:
                    kws = ", ".join(intent["keywords"])
                    print(
                        f"[{intent['target']}][{intent['category']}]: {intent['func'].__name__} (keywords: {kws})"
                    )
                continue

            if user_input.lower() == ":debug":
                print(f"{C.SYSTEM}Debug Dominus:{C.RESET}")
                # exibe info básica de memória/CPU/uptime etc
                cpu = engine.dominus.intents.execute("get_cpu")
                mem = engine.dominus.intents.execute("get_memory")
                uptime = engine.dominus.intents.execute("get_uptime")
                print(f"{C.INFO}[CPU] {cpu}{C.RESET}")
                print(f"{C.INFO}[Memory] {mem}{C.RESET}")
                print(f"{C.INFO}[Uptime] {uptime}{C.RESET}")
                continue

            if user_input.lower() == ":routes":
                if last_route:
                    print(f"{C.SYSTEM}Última rota do Router:{C.RESET} {last_route}")
                else:
                    print(f"{C.WARNING}Nenhuma rota ainda{C.RESET}")
                    continue

        responses = engine.handle(user_input)

        for r in responses:
            render(r)
