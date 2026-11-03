"""Stage B - LLM classifier. The ONLY probabilistic step.

The LLM gets the line description, HSN/SAC and supplier name (no GSTINs, no amounts, no client identity)
and must return one category from a closed list plus an exact quote as evidence.
It never outputs eligibility, a clause number or an amount; validate() enforces that.
"""
import hashlib
import json
import os
import re
import time

import requests

PROMPT_VERSION = "v1"
DEFAULT_MODEL = "google/gemma-4-31b-it:free"

CATEGORIES = {
    "passenger_vehicle": "purchase of a motor vehicle meant to carry people (car, SUV, MUV, van)",
    "goods_vehicle": "purchase of a vehicle meant to carry goods (truck, pickup, goods carrier)",
    "vehicle_hire": "renting, leasing or hiring a passenger motor vehicle (cab hire, car rental, with or without driver)",
    "vehicle_insurance_repair_service": "insurance, servicing, repair or maintenance of a motor vehicle",
    "food_beverage": "food or drinks: meals, restaurant bills, snacks, canteen food, in-room dining",
    "outdoor_catering": "catering services for an event or function",
    "accommodation": "hotel or guest-house room stay",
    "club_membership": "membership or subscription of a club",
    "health_fitness": "gym, health or fitness centre membership",
    "health_service": "medical or health services",
    "beauty_cosmetic": "beauty treatment, salon, spa, cosmetic or plastic surgery",
    "life_health_insurance": "life insurance or health insurance premium",
    "employee_travel_benefit": "holiday or leave travel provided to employees (LTC/vacation travel)",
    "none_of_these": "anything else (raw materials, equipment, rent, IT, professional services, non-passenger equipment hire)",
    "unclear": "the text is too vague to tell",
}

SYSTEM_PROMPT = """You classify ONE line from an Indian purchase invoice into exactly one category.
You do NOT decide tax eligibility. You only say what was bought.

Categories:
{cats}

Rules:
- "evidence" must be copied EXACTLY from the description (a short substring), no paraphrase.
- "seating_capacity": an integer ONLY if a seating number is written in the description; otherwise null. Never guess from a car model name.
- If the line could fit two categories, pick the one that describes most of the spend and lower your confidence.
- If the description is vague, use "unclear".
Reply with ONLY a JSON object:
{{"category": "...", "evidence": "...", "seating_capacity": null, "confidence": 0.0, "reason": "one short sentence"}}"""


def _system_prompt():
    return SYSTEM_PROMPT.format(cats="\n".join(f"- {k}: {v}" for k, v in CATEGORIES.items()))


def _user_prompt(line: dict) -> str:
    return json.dumps({"description": line["description"], "hsn_sac": line["hsn_sac"] or None,
                       "supplier_name": line["supplier_name"]}, ensure_ascii=False)


def _cache_key(model: str, line: dict) -> str:
    raw = f"{model}|{PROMPT_VERSION}|{_user_prompt(line)}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def _call_openrouter(model: str, line: dict) -> str:
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY not set (put it in prototype/.env)")
    for attempt in range(4):
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}"},
            json={"model": model, "temperature": 0,
                  "messages": [{"role": "system", "content": _system_prompt()},
                               {"role": "user", "content": _user_prompt(line)}]},
            timeout=90,
        )
        if resp.status_code in (429, 500, 502, 503):
            time.sleep(5 * (attempt + 1))
            continue
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    raise RuntimeError(f"OpenRouter kept failing ({resp.status_code})")


def _parse(raw: str) -> dict:
    m = re.search(r"\{.*\}", raw, re.S)
    if not m:
        raise ValueError("no JSON object in reply")
    return json.loads(m.group())


def validate(out: dict, line: dict) -> tuple[dict, list]:
    """Enforce the contract. Anything that breaks it is downgraded to 'unclear', never trusted."""
    problems = []
    cat = out.get("category")
    if cat not in CATEGORIES:
        problems.append(f"category '{cat}' not in closed list")
        cat = "unclear"
    evidence = str(out.get("evidence") or "")
    if evidence and evidence.lower() not in line["description"].lower():
        problems.append(f"evidence '{evidence}' is not a quote from the invoice")
        evidence = ""
    seats = out.get("seating_capacity")
    if seats is not None:
        try:
            seats = int(seats)
        except (TypeError, ValueError):
            seats = None
        # A fact only counts if the number is actually written on the invoice
        if seats is not None and not re.search(rf"\b{seats}\b", line["description"]):
            problems.append(f"seating_capacity {seats} not stated on invoice - dropped")
            seats = None
    try:
        conf = max(0.0, min(1.0, float(out.get("confidence", 0))))
    except (TypeError, ValueError):
        conf = 0.0
    if problems:
        conf = min(conf, 0.5)
    return {"category": cat, "evidence": evidence, "seating_capacity": seats,
            "confidence": conf, "reason": str(out.get("reason", ""))[:200]}, problems


def classify(line: dict, model: str, cache: dict, offline: bool) -> dict:
    key = _cache_key(model, line)
    raw = cache.get(key)
    if raw is None:
        if offline:
            return {"category": "unclear", "evidence": "", "seating_capacity": None, "confidence": 0.0,
                    "reason": "offline and not cached", "llm_problems": ["no cached LLM output"]}
        raw = _call_openrouter(model, line)
        cache[key] = raw
        time.sleep(3)  # stay under free-tier rate limits
    try:
        parsed = _parse(raw)
    except (ValueError, json.JSONDecodeError) as e:
        return {"category": "unclear", "evidence": "", "seating_capacity": None, "confidence": 0.0,
                "reason": "unparseable LLM reply", "llm_problems": [str(e)]}
    out, problems = validate(parsed, line)
    out["llm_problems"] = problems
    return out
