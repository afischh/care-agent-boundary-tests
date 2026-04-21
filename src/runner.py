from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from verdict_adapter import analyze, verdict_at_least

# -----------------------------------------------------------------------------
# runner.py
# -----------------------------------------------------------------------------
# Этот файл превращает набор кейсов в прогоняемый тестовый стенд.
#
# Что здесь происходит:
# 1. Читаем JSON-файл с кейсами.
# 2. Для каждого кейса берём ответ агента.
# 3. Гоним его через verdict engine.
# 4. Сравниваем с ожидаемым минимумом.
# 5. Строим не только список результатов, но и агрегированные сводки.
# -----------------------------------------------------------------------------


def load_cases(path: str) -> list[dict]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Файл кейсов должен содержать JSON-массив")
    return data


def run_cases(path: str) -> dict:
    cases = load_cases(path)
    results: list[dict] = []
    by_domain: Counter[str] = Counter()
    by_verdict: Counter[str] = Counter()
    by_status: Counter[str] = Counter()
    by_group_hits: Counter[str] = Counter()

    for case in cases:
        case_id = case["id"]
        domain = case.get("domain", "general")
        response = case["agent_response"]
        expected_min = case.get("expected_min_verdict", "low")

        verdict_result = analyze(response, profile=domain)
        actual = verdict_result["verdict"]
        status = "PASS" if verdict_at_least(actual, expected_min) else "FAIL"

        by_domain[domain] += 1
        by_verdict[actual] += 1
        by_status[status] += 1

        for group_name, group_info in verdict_result["groups"].items():
            if group_info["count"] > 0:
                by_group_hits[group_name] += 1

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

    summary = {
        "total_cases": len(results),
        "by_status": dict(by_status),
        "by_domain": dict(by_domain),
        "by_verdict": dict(by_verdict),
        "by_group_hits": dict(by_group_hits),
    }

    return {
        "summary": summary,
        "results": results,
    }
