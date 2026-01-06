from engine.contracts import Response


def apply_policy(responses: list[Response]):
    has_dominus = any(r.sender == "dominus" for r in responses)

    filtered = []
    for r in responses:
        if r.sender == "lucia" and has_dominus:
            continue
        filtered.append(r)

    return filtered
