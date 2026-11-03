"""ITC Gatekeeper prototype - monthly pre-filing check of purchase invoices for GST input tax credit.

    python run.py                 # calls the LLM for uncached lines, then writes out/
    python run.py --offline       # uses only cached LLM replies (no API key needed)

The LLM reads; code decides; a human signs.
"""
import argparse
import csv
import json
import os
from datetime import date
from pathlib import Path

import yaml

from itc import classifier, router, rules_engine, section16

ROOT = Path(__file__).parent
CACHE_FILE = ROOT / "cache" / "llm_cache.json"


def load_env():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def read_csv(name):
    with open(ROOT / "data" / name, newline="") as f:
        return list(csv.DictReader(f))


def load_inputs():
    invoices = read_csv("invoices.csv")
    for r in invoices:
        r["invoice_date"] = date.fromisoformat(r["invoice_date"])
        r["gst_amount"] = float(r["gst_amount"])
    gstr2b = read_csv("gstr2b.csv")
    for r in gstr2b:
        r["gst_amount"] = float(r["gst_amount"])
    payments = {(r["client_id"], r["invoice_no"]): date.fromisoformat(r["paid_on"]) for r in read_csv("payments.csv")}
    clients = yaml.safe_load(open(ROOT / "data" / "clients.yaml"))["clients"]
    rules = yaml.safe_load(open(ROOT / "rules" / "clause_cards.yaml"))
    hints = yaml.safe_load(open(ROOT / "rules" / "hints.yaml"))
    return invoices, gstr2b, payments, clients, rules, hints


def run(as_of: date, model: str, offline: bool):
    invoices, gstr2b, payments, clients, rules, hints = load_inputs()
    cards = rules["cards"]
    blocked_cats = rules_engine.blocked_categories(cards)
    cfg = {**hints, "review_always": rules.get("review_always", {})}
    cache = json.loads(CACHE_FILE.read_text()) if CACHE_FILE.exists() else {}

    register = []
    try:
        for i, line in enumerate(invoices, 1):
            cid = line["client_id"]
            profile = clients[cid]
            s16 = section16.check(line, [r for r in gstr2b if r["client_id"] == cid],
                                  payments.get((cid, line["invoice_no"])), as_of)
            cls = classifier.classify(line, model, cache, offline)
            rule = rules_engine.decide(cls["category"], {"seating_capacity": cls["seating_capacity"]}, profile, cards)
            route, reasons = router.route(line, cls, s16, rule, blocked_cats, cfg)

            final = s16["s16_status"] if s16["s16_status"] in (
                section16.LAPSED, section16.REVERSE_180, section16.NOT_IN_2B) else rule["recommendation"]
            register.append({
                "client_id": cid, "invoice_no": line["invoice_no"], "invoice_date": line["invoice_date"].isoformat(),
                "supplier": line["supplier_name"], "description": line["description"], "hsn_sac": line["hsn_sac"],
                "gst_amount": line["gst_amount"],
                "category": cls["category"], "confidence": cls["confidence"], "evidence": cls["evidence"],
                "seating_capacity": cls["seating_capacity"], "llm_reason": cls["reason"],
                "s16_status": s16["s16_status"], "s16_notes": " | ".join(s16["s16_notes"]),
                "rule_recommendation": rule["recommendation"], "clause": rule["clause"],
                "rule_path": " -> ".join(rule["rule_path"]), "question_for_reviewer": rule["question"],
                "final_recommendation": final, "route": route, "review_reasons": " | ".join(reasons),
                "itc_claimable_if_approved": line["gst_amount"] if final == "ELIGIBLE" else 0.0,
                "deadline_16_4": s16["deadline"].isoformat(), "days_to_deadline": s16["days_to_deadline"],
                # audit trail
                "model": model, "prompt_version": classifier.PROMPT_VERSION,
                "cards_version": rules["cards_version"], "profile_version": profile["profile_version"],
                "reviewer": "", "reviewer_decision": "", "reviewed_at": "",
            })
            print(f"[{i:02d}/{len(invoices)}] {cid} {line['invoice_no']:<14} {cls['category']:<32} "
                  f"{final:<24} {route}")
    finally:
        CACHE_FILE.parent.mkdir(exist_ok=True)
        CACHE_FILE.write_text(json.dumps(cache, indent=1))

    out = ROOT / "out"
    out.mkdir(exist_ok=True)
    with open(out / "itc_register.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(register[0]))
        w.writeheader()
        w.writerows(register)
    (out / "report.md").write_text(render_report(register, clients, as_of, model))
    print(f"\nWrote {out/'itc_register.csv'} and {out/'report.md'}")
    return register


def render_report(reg, clients, as_of, model):
    L = [f"# ITC pre-filing check - as of {as_of}", "",
         f"Model: `{model}` (classification only). All data synthetic.", ""]
    auto = [r for r in reg if r["route"] == "AUTO"]
    review = [r for r in reg if r["route"] == "REVIEW"]
    L += [f"- Lines checked: **{len(reg)}**  |  auto-accepted: **{len(auto)}**  |  sent to reviewer: **{len(review)}**", ""]

    L += ["## Review queue (CA sign-off required)", "",
          "| Client | Invoice | Description | AI category (evidence) | Recommendation | Clause | Why review | Question |",
          "|---|---|---|---|---|---|---|---|"]
    for r in review:
        L.append(f"| {r['client_id']} | {r['invoice_no']} | {r['description']} | {r['category']} "
                 f"(\"{r['evidence']}\", {r['confidence']:.2f}) | **{r['final_recommendation']}** | {r['clause']} | "
                 f"{r['review_reasons']} | {r['question_for_reviewer']} |")

    L += ["", "## Auto-accepted (spot-check sample)", "",
          "| Client | Invoice | Description | AI category | ITC |", "|---|---|---|---|---|"]
    for r in auto:
        L.append(f"| {r['client_id']} | {r['invoice_no']} | {r['description']} | {r['category']} | {r['itc_claimable_if_approved']:,.0f} |")

    fy = [r for r in reg if r["days_to_deadline"] >= 0 and r["days_to_deadline"] <= 60]
    L += ["", "## s.16(4) deadline watch (credit lapses permanently after the deadline)", ""]
    if fy:
        L += ["| Client | Invoice | Deadline | Days left | Status | ITC at stake |", "|---|---|---|---|---|---|"]
        for r in fy:
            L.append(f"| {r['client_id']} | {r['invoice_no']} | {r['deadline_16_4']} | {r['days_to_deadline']} | "
                     f"{r['final_recommendation']} / {r['route']} | {r['gst_amount']:,.0f} |")
    else:
        L.append("No lines within 60 days of their deadline.")

    L += ["", "## Per-line rule paths (audit trail)", ""]
    for r in reg:
        L.append(f"- **{r['client_id']} {r['invoice_no']}** - {r['final_recommendation']}: {r['rule_path']}"
                 + (f"; s.16: {r['s16_notes']}" if r["s16_notes"] else ""))
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--as-of", default="2026-11-03")
    ap.add_argument("--model", default=os.environ.get("ITC_MODEL", classifier.DEFAULT_MODEL))
    ap.add_argument("--offline", action="store_true")
    a = ap.parse_args()
    load_env()
    run(date.fromisoformat(a.as_of), a.model, a.offline)
