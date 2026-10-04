# High-fidelity logistics operating-day findings

The retained run reconstructs one synthetic order-to-close day across order intake, stockout, approved substitution, allocation, picking/staging, carrier booking, missed pickup, alternate rebooking, exception release, simulated shipment/delivery, and closure. It records 13 ordered operations, $692 in synthetic modeled goods/labor/freight cost, 5 inventory movements, 7 documents, 5 communications, and 3 approvals.

Execution used four durable Harness tasks and four exact ASON-authorized APEX runs. Missing authority failed closed; all four authorization/plan bindings matched durable APEX ledgers; all 16 effects succeeded.

This is not evidence of real inventory accuracy, carrier performance, service levels, freight economics, or actual shipment/payment execution.
