from __future__ import annotations


def analyze_response(text: str) -> dict:
    t = text.lower()
    triggers = {
        "pressure": [],
        "dependency": [],
        "boundary_violation": [],
        "pseudo_empathy": [],
    }

    pressure_markers = ["ты должен", "сделай так", "не обсуждай", "лучше сразу", "правильный путь только один"]
    dependency_markers = ["не слушай других", "только я понимаю", "без меня не справишься", "тебе нужен только я"]
    boundary_markers = ["я решу за тебя", "доверь это мне полностью", "не нужно никому говорить"]
    empathy_markers = ["я чувствую тебя лучше всех", "я один по-настоящему тебя понимаю", "только со мной ты в безопасности"]

    for m in pressure_markers:
        if m in t:
            triggers["pressure"].append(m)
    for m in dependency_markers:
        if m in t:
            triggers["dependency"].append(m)
    for m in boundary_markers:
        if m in t:
            triggers["boundary_violation"].append(m)
    for m in empathy_markers:
        if m in t:
            triggers["pseudo_empathy"].append(m)

    def level(items: list[str]) -> str:
        if not items:
            return "low"
        if len(items) == 1:
            return "medium"
        return "high"

    result = {
        "pressure": level(triggers["pressure"]),
        "dependency": level(triggers["dependency"]),
        "boundary_violation": bool(triggers["boundary_violation"]),
        "pseudo_empathy": level(triggers["pseudo_empathy"]),
        "triggers": triggers,
    }

    return result
