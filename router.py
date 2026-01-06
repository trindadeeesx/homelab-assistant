import re
from typing import List


class Router:
    HOME_KEYWORDS = [
        "luz",
        "lampada",
        "apaga",
        "liga",
        "quarto",
        "sala",
        "cozinha",
        "casa",
        "janela",
        "tv",
        "ar",
        "ventilador",
    ]
    SOCIAL_KEYWORDS = [
        "oi",
        "ola",
        "bom dia",
        "boa noite",
        "como vai",
        "tudo bem",
        "obrigado",
    ]

    def route(self, text: str) -> dict:
        text_l = text.lower()
        words = self._tokenize(text_l)

        targets = set()
        intent_parts = []

        # Dominus agora pega todas as intents via INTENT_REGISTRY
        if any(w for w in words):  # só assume que se é texto, Dominus pode processar
            targets.add("dominus")
            intent_parts.append("technical")

        if self._match(words, self.HOME_KEYWORDS):
            targets.add("lucia")
            intent_parts.append("home")

        if self._match(words, self.SOCIAL_KEYWORDS) and "lucia" not in targets:
            targets.add("lucia")
            intent_parts.append("social")

        if not targets:
            targets.add("lucia")
            intent_parts.append("fallback")

        return {"targets": list(targets), "intent": "_".join(intent_parts)}

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\b\w+\b", text)

    def _match(self, words: List[str], keywords: List[str]) -> bool:
        return any(k in words for k in keywords)
