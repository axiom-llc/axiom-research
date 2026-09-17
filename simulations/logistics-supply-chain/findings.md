# Findings

## Retained observations

- The synthetic order-to-close workflow executed through ASON→APEX with 14/14 recorded effects succeeding.
- Missing authority failed closed before APEX run creation.
- Live replay reused completed effects without rewriting produced files.
- Stockout/substitution and missed-pickup/rebooking are modeled exception paths, not operational service-level measurements.

## Limits

Inventory, carrier, shipment, booking, delivery, and customer state are synthetic. No real purchase, shipment, booking, or service commitment occurred.
