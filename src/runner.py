from __future__ import annotations

import json
from pathlib import Path
from verdict_adapter import analyze, verdict_at_least

# -----------------------------------------------------------------------------
# runner.py
# -----------------------------------------------------------------------------
# Этот файл делает главный шаг: превращает набор кейсов в прогоняемый тестовый стенд.
#
# Что здесь происходит:
# 1. Читаем JSON-файл с кейсами.
# 2. Для каждого кейса берём ответ агента.
# 3. Гоним его через verdict engine.
# 4. Сравниваем с ожидаемым минимумом.
# 5. Возвращаем список результатов.
# -----------------------------------------------------------------------------


def load_cases(path: str) -> list[dict]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Файл кейсов должен содержать JSON-массив")
    return data


def run_cases(path: str) -> list[dict]:
    cases = load_cases(path)
    results: list[dict] = []

    for case in cases:
        case_id = case["id"]
        domain = case.get("domain", "general")
        response = case["agent_response"]
        expected_min = case.get("expected_min_verdict", "low")

        verdict_result = analyze(response, profile=domain)
        actual = verdict_result["verdict"]
        status = "PASS" if verdict_at_least(actual, expected_min) else "FAIL"

        results.append(
            {
                "id": case_id,
                "domain": domain,
                "scenario": case.get("scenario", ""),
                "expected_min_verdict": expected_min,
                "actual_verdict": actual,
                "status": status,
                "total_score": verdict_result["total_score"],
                "groups": verdict_result["groups"],
            }
        )

    return results
