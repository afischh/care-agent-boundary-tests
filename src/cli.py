from __future__ import annotations

import argparse
import json
from runner import run_cases


def print_summary(summary: dict) -> None:
    print("СВОДКА")
    print("------")
    print(f"Всего кейсов: {summary['total_cases']}")
    print(f"PASS: {summary['by_status'].get('PASS', 0)}")
    print(f"FAIL: {summary['by_status'].get('FAIL', 0)}")
    print()

    print("По доменам:")
    for key, value in sorted(summary["by_domain"].items()):
        print(f"  - {key}: {value}")
    print()

    print("По verdict-уровням:")
    for key, value in sorted(summary["by_verdict"].items()):
        print(f"  - {key}: {value}")
    print()

    print("По группам сигналов:")
    for key, value in sorted(summary["by_group_hits"].items()):
        print(f"  - {key}: {value}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="care-agent-boundary-tests — пакетный прогон кейсов через verdict engine"
    )
    parser.add_argument("--cases", required=True, help="Путь к JSON-файлу с кейсами")
    parser.add_argument("--json", action="store_true", help="Вывести результат в JSON")
    args = parser.parse_args()

    report = run_cases(args.cases)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    print("care-agent-boundary-tests")
    print("=========================")
    print_summary(report["summary"])

    print("КЕЙСЫ")
    print("-----")
    for r in report["results"]:
        print(f"- {r['id']} [{r['domain']}] -> {r['status']}")
        print(f"  ожидаемый минимум: {r['expected_min_verdict']}")
        print(f"  фактический verdict: {r['actual_verdict']}")
        print(f"  score: {r['total_score']:.2f}")
        print(f"  сценарий: {r['scenario']}")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
