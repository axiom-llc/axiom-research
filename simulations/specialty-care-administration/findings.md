# Findings

## Retained observations

- The synthetic referral-to-administrative-close workflow executed through ASON→APEX with 13/13 recorded effects succeeding.
- Missing authority failed closed before APEX run creation.
- Live replay reused completed effects without rewriting produced files.
- Missing-record and payer-information delays are modeled administrative exceptions only.

## Limits

All patient, payer, scheduling, and encounter data are synthetic. No diagnosis, treatment selection, prescribing, real scheduling, clinical judgment, compliance, or patient outcome is represented or validated.
