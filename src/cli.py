from __future__ import annotations

import json
import sys
from analyzer import analyze_response


def main() -> int:
    if len(sys.argv) < 2:
        print("Использование: python src/cli.py '<ответ агента>'")
        return 1
    text = sys.argv[1]
    print(json.dumps(analyze_response(text), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
