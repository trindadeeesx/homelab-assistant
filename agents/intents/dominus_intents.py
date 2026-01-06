import os

from agents.intents.intents import INTENT_REGISTRY


class DominusIntents:
    def extract(self, text: str):
        actions = []
        text_l = text.lower()

        parts = [p.strip() for p in text_l.split(" e ")]

        for p in parts:
            for intent in INTENT_REGISTRY:
                matched_keyword = next((k for k in intent["keywords"] if k in p), None)
                if matched_keyword:
                    payload = {}

                    if intent["func"].__name__ == "get_disk":
                        path = p.replace(matched_keyword, "").strip()

                        if path:
                            path = os.path.expanduser(path)
                            path = os.path.abspath(path)
                            payload["path"] = path

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
