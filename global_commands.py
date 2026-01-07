import os
import sys
import time
from getpass import getpass
from importlib import reload

from agents.intents import intents_definition
from agents.intents.dominus_intents import DominusIntents
from agents.intents.intents import INTENT_REGISTRY
from engine.engine import Engine
from ui.style import C


def handle_global_command(
    user_input: str, engine, admin_password: str, last_route=None, history=None
):
    """
    Retorna True se o comando foi global e já processado.
    Retorna False se deve continuar processando como intent normal.
    """
    cmd = user_input.lower().strip()

    # sair do terminal
    if cmd in [":q", ":quit", ":exit"]:
        return "exit"

    # ajuda
    elif cmd in [":h", ":help"]:
        print()
        print(f"{C.SYSTEM}Comandos disponíveis:{C.RESET}")
        print(":q / :quit / :exit - Sair do terminal")
        print(":h / :help - Mostrar ajuda")
        print(":reload - Recarregar intents do Dominus")
        print(":intents - Listar todas intents registradas (ADMIN)")
        print(":debug - Informações de debug do sistema (ADMIN)")
        print(":routes - Mostrar rotas do Router para a última entrada (ADMIN)")
        print(":clear - Limpa a tela")
        print(":history - Mostra histórico dos comandos")
        print(":version - Mostra versão do assistente")
        print(":reset - Reseta estado interno (fake)")
        print(":shutdown - Desliga o sistema (ADMIN)")
        print(":restart - Reinicia o sistema (ADMIN)")
        print(":reload_intents - Recarrega intents (ADMIN)")
        print(":snippet <lang> - Pede LLM para gerar snippet de código")
        print(":run <lang> <code> - Executa código em sandbox")
        print()
        return True

    # limpar tela
    elif cmd in [":clear"]:
        os.system("clear")
        return True

    # mostrar versão
    elif cmd in [":version"]:
        print(f"{C.SYSTEM}Dominus & Lucia — v0.9.0{C.RESET}")
        return True

    # histórico
    elif cmd in [":history"]:
        if history:
            print(f"{C.INFO}Histórico de comandos:{C.RESET}")
            for i, h in enumerate(history, 1):
                print(f"{i:02d}: {h}")
        else:
            print(f"{C.WARNING}Nenhum histórico disponível{C.RESET}")
        return True

    # reset fake
    elif cmd in [":reset"]:
        print(f"{C.WARNING}Estado interno resetado (fake){C.RESET}")
        return True

    # reload intents
    elif cmd in [":reload_intents", ":r"]:
        reload(intents_definition)
        engine.dominus.intents = DominusIntents()
        print(f"{C.SUCCESS}✅ Dominus intents recarregadas{C.RESET}")
        return True

    # comandos admin com senha
    elif cmd.startswith((":intents", ":debug", ":routes", ":shutdown", ":restart")):
        senha = getpass(f"{C.WARNING}Senha de ADMIN: {C.RESET}")
        if senha != admin_password:
            print(f"{C.ERROR}❌ Senha incorreta{C.RESET}")
            return True

        # intents
        if cmd.startswith(":intents"):
            args = cmd.split()[1:]
            if not args:
                categories = set(intent["category"] for intent in INTENT_REGISTRY)
                print(f"{C.INFO}Categorias de intents:{C.RESET}")
                for c in categories:
                    print(f" - {c}")
            elif args[0] in [intent["category"] for intent in INTENT_REGISTRY]:
                cat = args[0]
                print(f"{C.INFO}Intents da categoria {cat}:{C.RESET}")
                for intent in INTENT_REGISTRY:
                    if intent["category"] == cat:
                        kws = ", ".join(intent["keywords"])
                        print(f" - {intent['func'].__name__}\t\t{kws}")
            else:
                name = args[0]
                for intent in INTENT_REGISTRY:
                    if intent["func"].__name__ == name:
                        kws = ", ".join(intent["keywords"])
                        print(
                            f"{C.INFO}Intent {name}:{C.RESET} Categoria: {intent['category']} Keywords: {kws}"
                        )
                        break
            return True

        # debug
        elif cmd.startswith(":debug"):
            cpu = engine.dominus.intents.execute("get_cpu")
            mem = engine.dominus.intents.execute("get_memory")
            uptime = engine.dominus.intents.execute("get_uptime")
            print(f"{C.INFO}[CPU] {cpu}{C.RESET}")
            print(f"{C.INFO}[Memory] {mem}{C.RESET}")
            print(f"{C.INFO}[Uptime] {uptime}{C.RESET}")
            return True

        # routes
        elif cmd.startswith(":routes"):
            if last_route:
                print(f"{C.SYSTEM}Última rota do Router:{C.RESET} {last_route}")
            else:
                print(f"{C.WARNING}Nenhuma rota ainda{C.RESET}")
            return True

        # shutdown
        elif cmd.startswith(":shutdown"):
            print(f"{C.WARNING}Sistema será desligado...{C.RESET}")
            exit(0)

        # restart
        elif cmd.startswith(":restart"):
            print(f"{C.WARNING}Sistema será reiniciado...{C.RESET}")
            time.sleep(3)
            python = sys.executable
            os.execv(python, [python] + sys.argv)

    # snippet / run (LLM + sandbox)
    elif cmd.startswith(":snippet"):
        parts = cmd.split(maxsplit=1)
        if len(parts) < 2:
            print(f"{C.WARNING}Use :snippet <linguagem>{C.RESET}")
            return True
        lang = parts[1]
        print(f"{C.INFO}Gerando snippet em {lang} via LLM...{C.RESET}")
        # aqui você chamaria sua função de LLM
        return True

    elif cmd.startswith(":run"):
        parts = cmd.split(maxsplit=2)
        if len(parts) < 3:
            print(f"{C.WARNING}Use :run <linguagem> <código>{C.RESET}")
            return True
        lang, code = parts[1], parts[2]
        print(f"{C.INFO}Executando código em {lang}:{C.RESET}\n{code}")
        # aqui você chamaria sua função de execução sandbox
        return True

    return False
