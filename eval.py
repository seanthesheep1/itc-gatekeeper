"""Compare out/itc_register.csv against tests/expected.csv and write out/eval.md.

Expected values may list alternatives separated by '|' (e.g. food_beverage|outdoor_catering).
"""
import csv
from pathlib import Path

ROOT = Path(__file__).parent


def ok(actual, expected):
    return actual in expected.split("|")


def main():
    reg = {(r["client_id"], r["invoice_no"]): r for r in csv.DictReader(open(ROOT / "out" / "itc_register.csv"))}
    exp = list(csv.DictReader(open(ROOT / "tests" / "expected.csv")))
    rows, n_pass = [], 0
    for e in exp:
        r = reg[(e["client_id"], e["invoice_no"])]
        c = ok(r["category"], e["expected_category"])
        f = ok(r["final_recommendation"], e["expected_final"])
        t = ok(r["route"], e["expected_route"])
        passed = c and f and t
        n_pass += passed
        rows.append(f"| {'PASS' if passed else '**FAIL**'} | {e['client_id']} {e['invoice_no']} | {e['what_it_tests']} | "
                    f"{r['category']}{'' if c else ' (exp ' + e['expected_category'] + ')'} | "
                    f"{r['final_recommendation']}{'' if f else ' (exp ' + e['expected_final'] + ')'} | "
                    f"{r['route']}{'' if t else ' (exp ' + e['expected_route'] + ')'} |")
    md = [f"# Evaluation - {n_pass}/{len(exp)} cases fully correct", "",
          f"Model: `{next(iter(reg.values()))['model']}`", "",
          "| Result | Case | What it tests | Category | Final | Route |", "|---|---|---|---|---|---|", *rows]
    (ROOT / "out" / "eval.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
