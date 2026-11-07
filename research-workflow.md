# AXIOM Research Pipeline — Public Interface

## Scope

The public `research-queue.json` contains disclosure-safe research prompts,
identifiers, ordering, state, and externally reviewable references. The complete
historical internal research intake is retained in verified private AXIOM
storage. Private or proprietary research details must not be introduced into
this public queue or its pull-request history.

## Public research workflow

1. Validate the queue using `python3 research_queue_check.py research-queue.json`.
2. Select the highest-ranked eligible `QUEUED` item by ascending priority,
   descending value score, creation date, then lexical identifier.
3. Research using publicly available evidence and synthetic examples.
4. Distinguish source evidence, interpretation, uncertainty, and hypotheses.
5. Produce a reviewable public research summary or demonstrated validation asset.
6. Publish only after [disclosure review](PUBLICATION.md) and successful
   repository checks.

`ISSUED` indicates a prompt was prepared, without asserting model delivery.
`COMPLETE` indicates a recorded accepted artifact, not validated implementation
or production deployment.

## Authority

The queue cannot authorize repository mutation, branch/PR merge, autonomous
external operations, provider spend, deployment, external contact, or changes
to existing agent access. The owning agent and repository permission policies
govern any such action independently.

Internal workflow diagrams, detailed prompt strategies, operational schedules,
system-specific routing/evaluation policies, and hosted-runtime observations
are withheld from the public edition.
