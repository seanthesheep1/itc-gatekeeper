"""Stage A - Section 16 gate. Pure date and lookup logic; no AI.

Checks, per invoice:
  1. Present in GSTR-2B (s.16(2)(aa))
  2. Supplier paid within 180 days, else credit must be reversed with interest (2nd proviso to s.16(2))
  3. Claimed within the s.16(4) time limit: 30 November after the end of the financial year
     (or the annual return date if earlier; this prototype assumes the annual return is not filed early)
"""
import re
from datetime import date, timedelta

PASS = "PASS"
NOT_IN_2B = "HOLD_NOT_IN_2B"
POSSIBLE_2B = "REVIEW_POSSIBLE_2B_MATCH"
REVERSE_180 = "REVERSE_UNPAID_180_DAYS"
LAPSED = "LAPSED_16_4"


def normalize_invoice_no(inv: str) -> str:
    """'SB/INV/0045' and 'SB-INV-45' both become 'SBINV45'."""
    s = re.sub(r"[^A-Z0-9]", "", inv.upper())
    return re.sub(r"\d+", lambda m: str(int(m.group())), s)


def fy_deadline(invoice_date: date) -> date:
    fy_end_year = invoice_date.year + 1 if invoice_date.month >= 4 else invoice_date.year
    return date(fy_end_year, 11, 30)


def check(inv: dict, gstr2b_rows: list, paid_on: date | None, as_of: date) -> dict:
    notes = []
    inv_date = inv["invoice_date"]

    # 1. GSTR-2B presence: exact on supplier GSTIN + normalised invoice no, amount within Rs 1
    same_supplier = [r for r in gstr2b_rows if r["supplier_gstin"] == inv["supplier_gstin"]]
    exact = [r for r in same_supplier
             if normalize_invoice_no(r["invoice_no"]) == normalize_invoice_no(inv["invoice_no"])
             and abs(r["gst_amount"] - inv["gst_amount"]) <= 1]
    near = [r for r in same_supplier if r not in exact and abs(r["gst_amount"] - inv["gst_amount"]) <= 1]
    if exact:
        in_2b = "yes"
        if exact[0]["invoice_no"] != inv["invoice_no"]:
            notes.append(f"2B matched after normalising '{exact[0]['invoice_no']}' -> '{inv['invoice_no']}'")
    elif near:
        in_2b = "near"
        notes.append(f"2B has same supplier+amount but invoice no '{near[0]['invoice_no']}' - never auto-matched")
    else:
        in_2b = "no"
        notes.append("Not in GSTR-2B - credit cannot be taken yet; follow up with supplier")

    # 2. 180-day payment rule
    age = (as_of - inv_date).days
    reverse = False
    if paid_on is None:
        if age > 180:
            reverse = True
            notes.append(f"Unpaid {age} days after invoice (>180) - reverse credit with interest; re-avail on payment")
        else:
            notes.append(f"Unpaid; {180 - age} days left before 180-day reversal")
    elif (paid_on - inv_date).days > 180:
        notes.append("Paid after 180 days - credit re-availed on payment (s.16(4) limit does not apply to re-availment)")

    # 3. s.16(4) time limit
    deadline = fy_deadline(inv_date)
    days_left = (deadline - as_of).days
    lapsed = days_left < 0
    if lapsed:
        notes.append(f"s.16(4) deadline {deadline} passed - credit lapsed permanently")

    if lapsed:
        status = LAPSED
    elif reverse:
        status = REVERSE_180
    elif in_2b == "no":
        status = NOT_IN_2B
    elif in_2b == "near":
        status = POSSIBLE_2B
    else:
        status = PASS

    return {"s16_status": status, "in_2b": in_2b, "deadline": deadline,
            "days_to_deadline": days_left, "s16_notes": notes}
