# Architecture changelog — public edition

This file records externally relevant changes to the public architecture contract. The complete original engineering decision history and operational reasoning are preserved in verified private retention.

## Version 1.0.0

- Defined 33 stable governing invariants covering human authority, component boundaries, validation, failure handling, and evidence-based completion.
- Established consistent schema identities for task, resource, work-intent, attempt, context, authorization-validation, and completion records.
- Clarified the distinction between strategic prioritization, durable task progression, policy authorization, bounded execution, and retrieval.
- Added explicit interoperability and reproducibility expectations for independent component validation.
- Formalized conservative treatment of ambiguous execution outcomes and the requirement for affirmative evidence before retry or promotion.
- Established public-safe evaluation boundaries for provider-neutral, capability-aware execution and synthetic workload evidence.

Detailed provider configurations, capacity/account handling, route selection, benchmark profiles, internal composition, and unpublished policy decisions remain private. The public [architecture](ARCHITECTURE.md), [schemas](schemas/), and [tests](tests/) are the reproducible publication surface. Validation of a public contract does not establish a deployed system or unrestricted autonomous authority.
