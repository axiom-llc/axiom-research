# Research-source optimization (RSI) — bounded engineering experiment

This directory contains a **source-anchored candidate generator, regression tests, and comparative measurements**, not an autonomously deployed research or code-modification service.

## What the experiment demonstrates

- A registered Python transformation proposes replacing `REQUIRED - set(item)` with `REQUIRED.difference(item)` in `research_queue_check.py` without altering the tracked source.
- The generator binds the candidate to the exact source identity, emits a unified diff, and evaluates a synthetic 300-record fixture, invalid-input holdouts, and paired benchmark observations.
- The [November 8 implementation review](implementation-review-2026-11-08.md) reports additional real-queue paired measurements: **2.757% median improvement on Python 3.11** and **4.299% on Python 3.12** under the recorded workload and environment. These are measured machine-side results, not generalized production gains.

## Status and limitations

**Review complete; implementation held.** The source change has **not** been applied. The existing generator would become saturated after applying its only registered transformation; the review requires a compatible registry transition, broader workload validation, and a separately authorized implementation. No deployed agent, externally executed research, revenue result, or uninterrupted production optimization is claimed.

## Inspect

- [Generator](native.py) and [registered rule](generators.json)
- [Generator tests](test_native.py), [representative test](test_representative.py), and [benchmark](benchmark.py)
- [Complete independent review and measured limitations](implementation-review-2026-11-08.md)

Treat the recorded results as a narrow engineering example of source-bound experimentation, review, and explicit non-promotion—not as a proven general optimization framework.
