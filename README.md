# ITC Gatekeeper — prototype

A monthly pre-filing check of purchase invoices for **GST input tax credit (ITC)** eligibility in India
(CGST Act 2017, **Section 16** conditions and **Section 17(5)** blocked credits).

**The LLM reads; code decides; a human signs.**
The LLM only maps a free-text invoice line to a closed category with a quoted piece of evidence. All legal rules, dates and amounts are in deterministic code driven by versioned clause cards. Anything touching a 17(5) clause goes to a CA.

> All data is **synthetic**: clients, suppliers, GSTINs, licence numbers and invoices are made up.

## Run it

```bash
pip install -r requirements.txt
python run.py --offline --model nvidia/nemotron-3.5-lightning:free   # replays cached LLM replies, no API key needed
python eval.py                                                       # scores against tests/expected.csv
```

Live LLM calls: copy `.env.example` to `.env`, add an OpenRouter key, then run `python run.py --model nvidia/nemotron-3.5-lightning:free`.
Lines that are already cached aren't re-sent.

**Model used:** `nvidia/nemotron-3.5-lightning:free` via OpenRouter (temperature 0, prompt `v1`).
The first choice, `google/gemma-4-31b-it:free`, returned HTTP 429 (free-tier rate limit) on every call. The pipeline failed safe: every line became `unclear` and went to human review.

Outputs land in `out/`:
- `itc_register.csv`: one row per line with category, evidence, Section 16 status, rule path, clause, route, plus audit fields (model, prompt version, clause-card version, profile version, reviewer)
- `report.md`: review queue, auto-accepted lines, s.16(4) deadline watch, per-line rule paths
- `eval.md`: test results

## Layout

```
data/clients.yaml        client profiles (business type, flags, statutory obligations) with evidence
data/invoices.csv        23 synthetic purchase invoice lines across 3 clients
data/gstr2b.csv          synthetic GSTR-2B
data/payments.csv        supplier payment dates
rules/clause_cards.yaml  the law: 17(5)(a), (ab), (b)(i), (b)(ii), (b)(iii) with exceptions, effective dates, verification
rules/hints.yaml         HSN/SAC hint table + tripwire words (cross-checks on the LLM)
itc/section16.py         Stage A  - 2B match, 180-day payment rule, s.16(4) time limit (code)
itc/classifier.py        Stage B  - LLM classification + output validation
itc/rules_engine.py      Stage C  - category + profile + clause card -> ELIGIBLE / BLOCKED / NEEDS_FACT (code)
itc/router.py            Stage D  - auto-accept vs. human review (code)
tests/expected.csv       expected category / outcome / route per case
```

## Test cases and results: 22 / 23 correct

Scored on three things per line: LLM category, final recommendation, and route (AUTO vs REVIEW). Full table in `out/eval.md`.

| Group | Cases | Result |
|---|---|---|
| Same invoice, different buyer (car for consultant vs taxi operator; caterer for voluntary lunch vs statutory factory canteen) | 4 | 4/4 opposite outcomes, correct |
| Section 16 traps (not in 2B, unpaid >180 days, FY 2024-25 lapsed, 2B invoice-number format mismatch) | 4 | 4/4 |
| Don't guess (car service with seating not on invoice → asks for RC seating) | 1 | 1/1 |
| Look-alikes (goods carrier, crane hire with operator) | 2 | 2/2 kept outside 17(5) |
| Other blocked categories (club, gym, cab hire, hotel with dining) | 4 | 4/4 |
| Plain eligible / vague | 5 | 5/5 |
| **Harder cases added after the first 20/20 run** | 3 | **2/3** |

## Where it fails / what this does NOT show (honest)

1. **Real failure: my clause card is wrong, not the LLM.** `TT/2026/15`, "Tempo Traveller **17-seater** hire". The LLM correctly extracted seating = 17. But the `CGST-17-5-b-i-hire` card has no `≤13 seats` condition, so the engine blocked it. A human-encoded rule bug produces a *confident, wrong, well-cited* answer. It was still routed to review (every 17(5) hit is), so a CA would catch it. Fix: add `requires_fact`/`blocked_if` seating to that card (one YAML change).
2. **The first 20 cases were written by the same person who wrote the rules,** so 20/20 mostly proves the plumbing works. When I deliberately tried to break it, the 3 harder cases found a bug in one of them.
3. **The risky lines are the auto-accepted ones** (6 of 23). They pass only when the LLM says "outside 17(5)" *and* HSN/SAC agrees *and* no tripwire word appears. None of the tests attacks this path with disguised descriptions (e.g. "business promotion expenses" that is actually a dinner). That's the next test set to build.
4. **Hotel line:** the LLM chose `accommodation` (not blocked). The engine alone would let the in-room dining through. Only the `review_always` rule saves it. Splitting mixed invoices isn't automated.
5. **One model, one run, temperature 0.** No measurement of run-to-run variance or of other models.
6. **Simplifications in Section 16:** the annual-return-date branch of 16(4) is ignored; 180-day exemptions (e.g. reverse charge) aren't modelled; 2B near-matches are only flagged.
7. **HSN/SAC hint table is illustrative**; the codes need checking against the current schedule.
8. **The law summaries in clause cards were self-checked against the bare Act by a non-CA** and are marked for CA re-verification.
