from agents.intents.dominus_intents import DominusIntents
from engine.contracts import Response, ResponseMode, Senders


class Dominus:
    def __init__(self):
        self.intents = DominusIntents()

    def respond(self, action: str, payload: dict) -> Response:
        text = self.intents.execute(action, payload)

        return Response(
            sender=Senders.DOMINUS, mode=ResponseMode.CODE, text=text.strip()
        )
