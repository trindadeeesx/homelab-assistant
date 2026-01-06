from agents.intents.intents import INTENT_REGISTRY


class DominusIntents:
    def extract(self, text: str):
        actions = []
        text_l = text.lower()
        for intent in INTENT_REGISTRY:
            if any(k in text_l for k in intent["keywords"]):
                payload = {}

                if intent["func"].__name__ == "get_disk":
                    for kw in intent["keywords"]:
                        if kw in text_l:
                            after = text_l.split(kw)[-1].strip()
                            if after:
                                payload["path"] = after
                            break

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
