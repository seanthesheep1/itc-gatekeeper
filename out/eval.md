# Evaluation - 22/23 cases fully correct

Model: `nvidia/nemotron-3.5-lightning:free`

| Result | Case | What it tests | Category | Final | Route |
|---|---|---|---|---|---|
| PASS | C2 TM/2026/118 | 7-seater car for a consulting firm -> 17(5)(a) blocked | passenger_vehicle | BLOCKED | REVIEW |
| PASS | C3 TM/2026/119 | SAME car for a taxi operator -> exception applies (buyer changes the answer) | passenger_vehicle | ELIGIBLE | REVIEW |
| PASS | C2 BC/2026/0412 | cab hire with driver -> 17(5)(b)(i) hire limb | vehicle_hire | BLOCKED | REVIEW |
| PASS | C1 AC/1021 | factory canteen under Factories Act -> proviso (statutory obligation) | food_beverage | ELIGIBLE | REVIEW |
| PASS | C2 AC/1022 | SAME caterer, voluntary team lunch -> blocked | outdoor_catering | BLOCKED | REVIEW |
| PASS | C1 TM/2026/201 | goods carrier -> outside 17(5)(a); should auto-accept | goods_vehicle | ELIGIBLE | AUTO |
| PASS | C2 BG/2026/77 | club membership -> 17(5)(b)(ii) | club_membership | BLOCKED | REVIEW |
| PASS | C2 DL/88231 | laptops -> plain eligible | none_of_these | ELIGIBLE | AUTO |
| PASS | C2 RK/OCT26 | office rent -> plain eligible | none_of_these | ELIGIBLE | AUTO |
| PASS | C2 OS/5531 | valid invoice missing from GSTR-2B -> hold | none_of_these | HOLD_NOT_IN_2B | REVIEW |
| PASS | C1 HP/2026/033 | unpaid > 180 days -> reverse with interest | none_of_these | REVERSE_UNPAID_180_DAYS | REVIEW |
| PASS | C1 LT/24/889 | FY 2024-25 invoice past 30 Nov 2025 -> lapsed | none_of_these | LAPSED_16_4 | REVIEW |
| PASS | C2 TJ/MUM/5521 | hotel room + in-room dining -> must be split by human | accommodation | ELIGIBLE | REVIEW |
| PASS | C2 HC/SRV/301 | car service, seating not on invoice -> ask, don't guess | vehicle_insurance_repair_service | NEEDS_FACT | REVIEW |
| PASS | C3 MS/SRV/772 | taxi repair, 5 seater stated -> 17(5)(ab) exception | vehicle_insurance_repair_service | ELIGIBLE | REVIEW |
| PASS | C2 EV/2026/12 | vague description, no SAC -> unclear | unclear | NEEDS_REVIEW | REVIEW |
| PASS | C1 SB/INV/0045 | 2B invoice no formatted differently (SB-INV-45) -> normalised match | none_of_these | ELIGIBLE | AUTO |
| PASS | C2 GY/2026/09 | employee gym membership -> 17(5)(b)(ii) | health_fitness | BLOCKED | REVIEW |
| PASS | C1 SG/26/3 | FY 2025-26 invoice -> eligible, shows on 30 Nov 2026 deadline watch | none_of_these | ELIGIBLE | AUTO |
| PASS | C1 HC/26/71 | crane hire with operator -> must NOT be confused with vehicle hire | none_of_these | ELIGIBLE | AUTO |
| PASS | C2 GT/2026/44 | HARD: 'staff welfare' wording hides a vacation travel benefit -> 17(5)(b)(iii) | employee_travel_benefit | BLOCKED | REVIEW |
| **FAIL** | C2 TT/2026/15 | HARD: hire of a 17-seater (>13) is outside the hire limb -> should NOT be blocked | vehicle_hire | BLOCKED (exp ELIGIBLE) | REVIEW |
| PASS | C2 MI/2026/601 | HARD: group health insurance, not obligatory by law -> 17(5)(b)(i) | life_health_insurance | BLOCKED | REVIEW |
