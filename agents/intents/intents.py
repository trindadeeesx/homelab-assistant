INTENT_REGISTRY = []


def intent(target: str, category: str, keywords=None):
    keywords = keywords or []

    def decorator(func):
        # registra a função com todas as infos
        INTENT_REGISTRY.append(
            {"target": target, "category": category, "keywords": keywords, "func": func}
        )
        return func

    return decorator
