# ITC pre-filing check - as of 2026-11-03

Model: `nvidia/nemotron-3.5-lightning:free` (classification only). All data synthetic.

- Lines checked: **23**  |  auto-accepted: **6**  |  sent to reviewer: **17**

## Review queue (CA sign-off required)

| Client | Invoice | Description | AI category (evidence) | Recommendation | Clause | Why review | Question |
|---|---|---|---|---|---|---|---|
| C2 | TM/2026/118 | Toyota Innova Crysta 2.4 VX, 7-seater, for use of director | passenger_vehicle ("Toyota Innova Crysta 2.4 VX, 7-seater, for use of director", 0.95) | **BLOCKED** | CGST Act 2017, s.17(5)(a) | touches a s.17(5) clause - human sign-off required |  |
| C3 | TM/2026/119 | Toyota Innova Crysta 2.4 GX, 7-seater, fleet addition | passenger_vehicle ("7-seater", 0.95) | **ELIGIBLE** | CGST Act 2017, s.17(5)(a) | touches a s.17(5) clause - human sign-off required |  |
| C2 | BC/2026/0412 | Innova hire with driver for client visits, Pune, 4 days | vehicle_hire ("Innova hire with driver", 0.95) | **BLOCKED** | CGST Act 2017, s.17(5)(b)(i) - leasing/renting/hiring of motor vehicles | touches a s.17(5) clause - human sign-off required | Rent-a-cab with driver vs. passenger transport is contested ground; reviewer confirms. |  |
| C1 | AC/1021 | Canteen catering for factory workers - October 2026 | food_beverage ("Canteen catering for factory workers", 0.95) | **ELIGIBLE** | CGST Act 2017, s.17(5)(b)(i) | touches a s.17(5) clause - human sign-off required |  |
| C2 | AC/1022 | Lunch buffet for team Diwali offsite, 40 pax | outdoor_catering ("Lunch buffet for team Diwali offsite", 0.95) | **BLOCKED** | CGST Act 2017, s.17(5)(b)(i) | touches a s.17(5) clause - human sign-off required |  |
| C2 | BG/2026/77 | Annual corporate membership fee FY 2026-27 | club_membership ("Annual corporate membership fee", 0.95) | **BLOCKED** | CGST Act 2017, s.17(5)(b)(ii) | touches a s.17(5) clause - human sign-off required |  |
| C2 | OS/5531 | Printer toner cartridges HP 88A x 20 | none_of_these ("Printer toner cartridges HP 88A x 20", 0.95) | **HOLD_NOT_IN_2B** |  | s.16: HOLD_NOT_IN_2B |  |
| C1 | HP/2026/033 | Spare seals and valves for 200T hydraulic press | none_of_these ("Spare seals and valves for 200T hydraulic press", 0.90) | **REVERSE_UNPAID_180_DAYS** |  | s.16: REVERSE_UNPAID_180_DAYS |  |
| C1 | LT/24/889 | Carbide inserts for CNC lathe | none_of_these ("Carbide inserts for CNC lathe", 0.95) | **LAPSED_16_4** |  | s.16: LAPSED_16_4 |  |
| C2 | TJ/MUM/5521 | Room charges 2 nights + in-room dining, client meeting trip | accommodation ("Room charges 2 nights", 0.80) | **ELIGIBLE** |  | Hotel invoices often bundle rooms (not blocked) with food and beverages (blocked, 17(5)(b)(i)); the invoice must be split. | tripwire words ['dining', 'room'] but LLM placed it outside s.17(5) |  |
| C2 | HC/SRV/301 | Periodic service and brake pad replacement - company Honda City MH12AB1234 | vehicle_insurance_repair_service ("Periodic service and brake pad replacement", 0.95) | **NEEDS_FACT** | CGST Act 2017, s.17(5)(ab) | touches a s.17(5) clause - human sign-off required | NEEDS_FACT | What is the approved seating capacity (incl. driver) on the vehicle's RC? |
| C3 | MS/SRV/772 | Accident repair, Swift Dzire taxi (5 seater) MH12CD5678 | vehicle_insurance_repair_service ("Accident repair, Swift Dzire taxi (5 seater)", 0.95) | **ELIGIBLE** | CGST Act 2017, s.17(5)(ab) | touches a s.17(5) clause - human sign-off required |  |
| C2 | EV/2026/12 | Misc expenses - event | unclear ("Misc expenses - event", 0.00) | **NEEDS_REVIEW** |  | NEEDS_REVIEW | LLM confidence 0.00 < 0.8 |  |
| C2 | GY/2026/09 | Employee gym membership - quarterly, 10 staff | health_fitness ("Employee gym membership", 1.00) | **BLOCKED** | CGST Act 2017, s.17(5)(b)(ii) | touches a s.17(5) clause - human sign-off required |  |
| C2 | GT/2026/44 | Staff welfare - Goa trip for employees and families, 3 nights | employee_travel_benefit ("Goa trip for employees and families", 0.90) | **BLOCKED** | CGST Act 2017, s.17(5)(b)(iii) | touches a s.17(5) clause - human sign-off required |  |
| C2 | TT/2026/15 | Tempo Traveller 17-seater hire with driver for team outing | vehicle_hire ("Tempo Traveller 17-seater hire with driver", 1.00) | **BLOCKED** | CGST Act 2017, s.17(5)(b)(i) - leasing/renting/hiring of motor vehicles | touches a s.17(5) clause - human sign-off required | Rent-a-cab with driver vs. passenger transport is contested ground; reviewer confirms. |  |
| C2 | MI/2026/601 | Group mediclaim policy - 60 employees, FY 2026-27 | life_health_insurance ("Group mediclaim policy", 1.00) | **BLOCKED** | CGST Act 2017, s.17(5)(b)(i) | touches a s.17(5) clause - human sign-off required |  |

## Auto-accepted (spot-check sample)

| Client | Invoice | Description | AI category | ITC |
|---|---|---|---|---|
| C1 | TM/2026/201 | Tata Ace Gold goods carrier for finished goods dispatch | goods_vehicle | 168,000 |
| C2 | DL/88231 | Dell Latitude 5450 laptops x 5 | none_of_these | 72,000 |
| C2 | RK/OCT26 | Office rent - October 2026, Baner, Pune | none_of_these | 27,000 |
| C1 | SB/INV/0045 | Ball bearings 6205 ZZ x 500 | none_of_these | 7,200 |
| C1 | SG/26/3 | Industrial safety gloves x 1000 | none_of_these | 6,000 |
| C1 | HC/26/71 | Hydra crane hire with operator for machine shifting | none_of_these | 6,300 |

## s.16(4) deadline watch (credit lapses permanently after the deadline)

| Client | Invoice | Deadline | Days left | Status | ITC at stake |
|---|---|---|---|---|---|
| C1 | HP/2026/033 | 2026-11-30 | 27 | REVERSE_UNPAID_180_DAYS / REVIEW | 45,000 |
| C1 | SG/26/3 | 2026-11-30 | 27 | ELIGIBLE / AUTO | 6,000 |

## Per-line rule paths (audit trail)

- **C2 TM/2026/118** - BLOCKED: 'passenger_vehicle' falls under CGST-17-5-a -> seating_capacity=7 <= 13 -> no exception in client profile
- **C3 TM/2026/119** - ELIGIBLE: 'passenger_vehicle' falls under CGST-17-5-a -> seating_capacity=7 <= 13 -> exception: used for transportation of passengers [profile evidence: Outward supply: passenger transport by taxi, SAC 9964 (synthetic GSTR-1 summary FY 2025-26)]
- **C2 BC/2026/0412** - BLOCKED: 'vehicle_hire' falls under CGST-17-5-b-i-hire -> no exception in client profile; s.16: Unpaid; 151 days left before 180-day reversal
- **C1 AC/1021** - ELIGIBLE: 'food_beverage' falls under CGST-17-5-b-i -> exception: proviso: obligatory for employer under any law [profile evidence: Factories Act 1948, s.46 - canteen required where more than 250 workers are employed | Factory licence MH/FL/2023/0457 (synthetic); headcount register Oct 2026: 312]
- **C2 AC/1022** - BLOCKED: 'outdoor_catering' falls under CGST-17-5-b-i -> no exception in client profile
- **C1 TM/2026/201** - ELIGIBLE: 'goods_vehicle' not covered by in-scope s.17(5) clauses
- **C2 BG/2026/77** - BLOCKED: 'club_membership' falls under CGST-17-5-b-ii -> no exception in client profile
- **C2 DL/88231** - ELIGIBLE: 'none_of_these' not covered by in-scope s.17(5) clauses
- **C2 RK/OCT26** - ELIGIBLE: 'none_of_these' not covered by in-scope s.17(5) clauses
- **C2 OS/5531** - HOLD_NOT_IN_2B: 'none_of_these' not covered by in-scope s.17(5) clauses; s.16: Not in GSTR-2B - credit cannot be taken yet; follow up with supplier
- **C1 HP/2026/033** - REVERSE_UNPAID_180_DAYS: 'none_of_these' not covered by in-scope s.17(5) clauses; s.16: Unpaid 233 days after invoice (>180) - reverse credit with interest; re-avail on payment
- **C1 LT/24/889** - LAPSED_16_4: 'none_of_these' not covered by in-scope s.17(5) clauses; s.16: s.16(4) deadline 2025-11-30 passed - credit lapsed permanently
- **C2 TJ/MUM/5521** - ELIGIBLE: 'accommodation' not covered by in-scope s.17(5) clauses
- **C2 HC/SRV/301** - NEEDS_FACT: 'vehicle_insurance_repair_service' falls under CGST-17-5-ab -> required fact 'seating_capacity' not on invoice
- **C3 MS/SRV/772** - ELIGIBLE: 'vehicle_insurance_repair_service' falls under CGST-17-5-ab -> seating_capacity=5 <= 13 -> exception: vehicle used for transportation of passengers [profile evidence: Outward supply: passenger transport by taxi, SAC 9964 (synthetic GSTR-1 summary FY 2025-26)]
- **C2 EV/2026/12** - NEEDS_REVIEW: category unclear; s.16: Unpaid; 166 days left before 180-day reversal
- **C1 SB/INV/0045** - ELIGIBLE: 'none_of_these' not covered by in-scope s.17(5) clauses; s.16: 2B matched after normalising 'SB-INV-45' -> 'SB/INV/0045'
- **C2 GY/2026/09** - BLOCKED: 'health_fitness' falls under CGST-17-5-b-ii -> no exception in client profile
- **C1 SG/26/3** - ELIGIBLE: 'none_of_these' not covered by in-scope s.17(5) clauses
- **C1 HC/26/71** - ELIGIBLE: 'none_of_these' not covered by in-scope s.17(5) clauses
- **C2 GT/2026/44** - BLOCKED: 'employee_travel_benefit' falls under CGST-17-5-b-iii -> no exception in client profile
- **C2 TT/2026/15** - BLOCKED: 'vehicle_hire' falls under CGST-17-5-b-i-hire -> no exception in client profile
- **C2 MI/2026/601** - BLOCKED: 'life_health_insurance' falls under CGST-17-5-b-i -> no exception in client profile
