import shutil
import socket
import time

import psutil

from .intents import intent


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
    print(payload)
    path = payload.get("path", "/") if payload else "/"
    total, used, free = shutil.disk_usage(path)
    return f"Espaço em '{path}': {round(used / 1e9)}GB usados de {round(total / 1e9)}GB"


@intent("dominus", "system", keywords=["uptime", "tempo ligado"])
def get_uptime(payload=None):
    uptime = psutil.boot_time()
    delta = time.time() - uptime
    hours = int(delta // 3600)
    minutes = int((delta % 3600) // 60)
    return f"Tempo ligado: {hours}h {minutes}min"
