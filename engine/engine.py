from agents.dominus import Dominus
from agents.intents.dominus_intents import DominusIntents
from agents.lucia import Lucia
from engine.contracts import RESPONSE_PRIORITY, Response, Senders
from engine.policy import apply_policy
from router import Router


class Engine:
    def __init__(self, router: Router):
        self.router = router
        self.dominus = Dominus()
        self.lucia = Lucia()

        self.dominus_intents = DominusIntents()
        self.last_route = None

    def handle(self, text: str) -> list[Response]:
        route = self.router.route(text)
        self.last_route = route

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

        dominus_texts = []
        for act in unique_actions:
            if act["target"] == "dominus":
                dominus_texts.append(
                    self.dominus.respond(act["action"], act["payload"]).text
                )

        if dominus_texts:
            responses.append(
                Response(
                    sender=Senders.DOMINUS,
                    mode=self.dominus.respond(
                        unique_actions[0]["action"], unique_actions[0]["payload"]
                    ).mode,
                    text="\n".join(dominus_texts),
                )
            )

        for act in unique_actions:
            if act["target"] == "lucia":
                responses.append(self.lucia.respond(act["action"], act["payload"]))

        responses.sort(key=lambda r: RESPONSE_PRIORITY.get(r.sender, 99))
        return apply_policy(responses)
