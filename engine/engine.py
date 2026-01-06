from agents.dominus import Dominus
from agents.intents.dominus_intents import DominusIntents
from agents.lucia import Lucia
from engine.contracts import RESPONSE_PRIORITY, Response
from engine.policy import apply_policy
from router import Router


class Engine:
    def __init__(self, router: Router):
        self.router = router
        self.dominus = Dominus()
        self.lucia = Lucia()

        self.dominus_intents = DominusIntents()

    def handle(self, text: str) -> list[Response]:
        route = self.router.route(text)

        actions = []
        responses: list[Response] = []

        if "dominus" in route["targets"]:
            actions += self.dominus_intents.extract(text)

        unique_actions = []
        seen = set()

        for a in actions:
            key = (a["target"], a["action"])
            if key not in seen:
                seen.add(key)
                unique_actions.append(a)

        for act in unique_actions:
            if act["target"] == "dominus":
                responses.append(self.dominus.respond(act["action"], act["payload"]))

            if act["target"] == "lucia":
                responses.append(self.lucia.respond(act["action"], act["payload"]))

        responses.sort(key=lambda r: RESPONSE_PRIORITY.get(r.sender, 99))
        return apply_policy(responses)
