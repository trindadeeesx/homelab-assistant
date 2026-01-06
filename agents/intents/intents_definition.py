import os
import platform
import shutil
import socket
import time

import psutil
from pygments.token import Keyword

from .intents import intent

"""

        DOMINUS

"""


# NETWORKS


@intent("dominus", "network", keywords=["ip", "meu ip", "endereço de ip", "addr"])
def get_ip(payload=None):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return f"IP atual: {ip}"
    except Exception:
        return "IP desconhecido"


@intent("dominus", "network", keywords=["hostname", "host"])
def get_hostname(payload=None):
    return f"Host: {socket.gethostname()}"


# ---------


# SYSTEM


@intent("dominus", "system", keywords=["cpu", "processador", "uso de cpu"])
def get_cpu(payload=None):
    usage = psutil.cpu_percent(interval=0.5)
    return f"Uso de CPU: {usage}%"


@intent("dominus", "system", keywords=["memoria", "ram", "uso de memória", "memory"])
def get_memory(payload=None):
    mem = psutil.virtual_memory()
    return f"Memória RAM: {round(mem.total / 1e9)}GB total, {round(mem.used / 1e9)}GB em uso"


@intent("dominus", "system", keywords=["disco", "espaco em disco", "disk"])
def get_disk(payload=None):
    path = payload.get("path", "/") if payload else "/"

    # Expande ~ e converte para absoluto
    path = os.path.expanduser(path)
    path = os.path.abspath(path)

    if not os.path.exists(path):
        return f"Caminho não encontrado: '{path}'"

    # Uso do disco (partição)
    total, used, free = shutil.disk_usage(path)

    # Uso da pasta específica
    folder_used = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            try:
                folder_used += os.path.getsize(os.path.join(root, f))
            except Exception:
                pass

    used_gb = round(used / 1e9)
    free_gb = round(free / 1e9)
    folder_used_gb = round(folder_used / 1e9, 2)

    return (
        f"Espaço em '{path}': {used_gb}GB usados de {round(total / 1e9)}GB. "
        f"Espaço livre: {free_gb}GB. "
        f"Uso real da pasta: {folder_used_gb}GB"
    )


@intent("dominus", "system", keywords=["uptime", "tempo ligado"])
def get_uptime(payload=None):
    uptime = psutil.boot_time()
    delta = time.time() - uptime
    hours = int(delta // 3600)
    minutes = int((delta % 3600) // 60)
    return f"Tempo ligado: {hours}h {minutes}min"


@intent("dominus", "system", keywords=["processos", "top cpu", "top memoria"])
def get_top_processes(payload=None):
    top_n = payload.get("n", 5) if payload else 5
    procs = sorted(
        psutil.process_iter(["pid", "name", "cpu_percent", "memory_info"]),
        key=lambda p: p.info["cpu_percent"],
        reverse=True,
    )[:top_n]
    lines = [
        f"{p.info['name']} (PID {p.info['pid']}): CPU {p.info['cpu_percent']}%, RAM {p.info['memory_info'].rss / 1e6:.1f}MB"
        for p in procs
    ]
    return "Top processos:\n" + "\n".join(lines)


@intent("dominus", "system", keywords=["os", "sistema"])
def get_system_info(payload=None):
    return f"{platform.system()} {platform.release()} ({platform.version()}) - {platform.machine()}"


"""

        LUCIA

"""
