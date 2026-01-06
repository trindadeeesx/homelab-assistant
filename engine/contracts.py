from dataclasses import dataclass
from enum import Enum

RESPONSE_PRIORITY = {"system": 0, "dominus": 1, "lucia": 2}


class ResponseMode(str, Enum):
    CHAT = "chat"
    CODE = "code"
    SYSTEM = "system"


class Senders(str, Enum):
    DOMINUS = "Dominus"
    LUCIA = "Lucia"
    SYSTEM = "System"


@dataclass
class Response:
    sender: Senders
    mode: ResponseMode
    text: str
