from agents.intents.intents import INTENT_REGISTRY


class DominusIntents:
    def extract(self, text: str):
        actions = []
        text_l = text.lower()

        for intent in INTENT_REGISTRY:
            for keyword in intent["keywords"]:
                if text_l.startswith(keyword):
                    rest = text[len(keyword) :].strip()
                    payload = {}

                    if rest:
                        payload["path"] = rest

                    actions.append(
                        {
                            "target": intent["target"],
                            "action": intent["func"].__name__,
                            "payload": payload,
                        }
                    )

        return actions

    def execute(self, action_name: str, payload=None) -> str:
        for intent in INTENT_REGISTRY:
            if intent["func"].__name__ == action_name:
                return intent["func"](payload)
        return "Intent técnica não reconhecida."
