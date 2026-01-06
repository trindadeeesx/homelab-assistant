from agents.intents.intents import INTENT_REGISTRY


class DominusIntents:
    def extract(self, text: str):
        actions = []
        text_l = text.lower()
        for intent in INTENT_REGISTRY:
            if any(k in text_l for k in intent["keywords"]):
                actions.append(
                    {
                        "target": intent["target"],
                        "action": intent["func"].__name__,
                        "payload": {},
                    }
                )

        return actions

    def execute(self, action_name: str, payload=None) -> str:
        for intent in INTENT_REGISTRY:
            if intent["func"].__name__ == action_name:
                return intent["func"](payload)
        return "Intent técnica não reconhecida."
