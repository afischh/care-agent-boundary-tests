from __future__ import annotations

import argparse
import json
from runner import run_cases


def main() -> int:
    parser = argparse.ArgumentParser(
        description="care-agent-boundary-tests — пакетный прогон кейсов через verdict engine"
    )
    parser.add_argument("--cases", required=True, help="Путь к JSON-файлу с кейсами")
    parser.add_argument("--json", action="store_true", help="Вывести результат в JSON")
    args = parser.parse_args()

    results = run_cases(args.cases)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0

    print("care-agent-boundary-tests")
    print("=========================")
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = total - passed
    print(f"Всего кейсов: {total}")
    print(f"PASS: {passed}")
    print(f"FAIL: {failed}")
    print()

    for r in results:
        print(f"- {r['id']} [{r['domain']}] -> {r['status']}")
        print(f"  ожидаемый минимум: {r['expected_min_verdict']}")
        print(f"  фактический verdict: {r['actual_verdict']}")
        print(f"  score: {r['total_score']:.2f}")
        print(f"  сценарий: {r['scenario']}")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
