from agents.intents.dominus_intents import DominusIntents
from agents.llm_handler import LLMHandler
from engine.contracts import Response, ResponseMode, Senders


class Dominus:
    def __init__(self):
        self.intents = DominusIntents()
        self.llm = LLMHandler()

    def respond(self, action: str, payload: dict) -> Response:
        if action in [i["func"].__name__ for i in self.intents.INTENT_REGISTRY]:
            text = self.intents.execute(action, payload)
        elif action.startswith("llm_code"):
            language = payload.get("language", "python")
            prompt = payload.get("prompt", "")

            text = self.llm.generate_code(prompt, language)

        else:
            text = "Intent técnica não reconhecida."

        return Response(
            sender=Senders.DOMINUS, mode=ResponseMode.CODE, text=text.strip()
        )
