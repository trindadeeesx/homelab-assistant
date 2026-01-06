from engine.contracts import Response, ResponseMode, Senders


class Lucia:
    def respond(self, action: str, payload: dict) -> Response:
        """
        TODO: IMPLEMENTAR LLM
        """
        text = ""

        if action == "light_off":
            room = payload.get("room", "local desconhecido")
            text = f"Luz do {room} desligada."

        return Response(sender=Senders.LUCIA, mode=ResponseMode.CHAT, text=text.strip())
