import json
from pathlib import Path

from app.agent import run_agent


def main() -> None:
    cases = json.loads((Path(__file__).parent / "cases.json").read_text(encoding="utf-8"))
    passed = 0
    for case in cases:
        result = run_agent(case["message"], session_id=f"eval-{case['id']}")
        called = {event["name"] for event in result["tool_calls"] if event["ok"]}
        answer = result["answer"].lower()
        checks = {
            "expected_tools": set(case["expected_tools"]).issubset(called),
            "forbidden_tools": not (set(case.get("forbidden_tools", [])) & called),
            "answer_signal": any(term.lower() in answer for term in case["must_contain_any"]),
            "handoff": result["handoff"] is case["expect_handoff"],
        }
        case_passed = all(checks.values())
        passed += int(case_passed)
        usage = result["usage"]
        print(f"{'PASS' if case_passed else 'FAIL'} {case['id']} {checks} latency_ms={result['latency_ms']} tokens={usage['prompt_tokens']}+{usage['completion_tokens']}")
    print(f"\nPass rate: {passed}/{len(cases)} ({passed / len(cases):.0%})")
    if passed != len(cases):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
