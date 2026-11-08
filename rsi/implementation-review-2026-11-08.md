# RSI Research candidate — independent implementation review

**Review date:** November 8, 2026  
**Candidate:** `rsi-5eb9510f0e1482978aa3`  
**Owning source:** `research_queue_check.py`, blob `ddf5829ad24829a593d80e23b77c10c1654b0ba2`  
**Acceptance baseline:** `main@a7e05f566d8c92475ff56e388e5f58fcc6b2197e`  
**Decision:** `REVIEW_COMPLETE / HOLD_IMPLEMENTATION`. No candidate patch applied.

## Exact proposed transformation

```diff
-        missing = REQUIRED - set(item)
+        missing = REQUIRED.difference(item)
```

### Code and correctness review — PASS (current scope)

The validator first requires each `item` to be a dictionary. On these inputs,
`set(item)` collects the dictionary's keys, while
`REQUIRED.difference(item)` iterates the same keys. Both produce the same
set of missing field names. The surrounding `sorted(missing)` diagnostic,
error paths, canonical queue policy and runtime interface remain unchanged.

The independently executed acceptance code compiled baseline and candidate
from the exact pinned source without writing either to the repository.
The real 19-record `research-queue.json` yielded identical result envelopes.
Four negative holdouts preserved exception class and message:
missing title, invalid target, duplicate ID and invalid policy. The canonical
queue and the original validator blob are unchanged.

The original `rsi.test_native` suite also tests exact `git apply`,
`git apply -R` and byte-for-byte source restoration; both Python matrix
jobs and the Architecture and Public publication gate workflows passed.

### Independent current-queue machine evidence — PASS (bounded)

[Post-merge acceptance workflow #42462897915](https://github.com/axiom-llc/axiom-research/actions/runs/42462897915)
completed successfully at the same source revision. The two
downloaded, independently ZIP-SHA-256-checked receipts agree on candidate
ID, source revision and canonical queue digest
`7644d68dcfff24f46c3a8a682343fdf8ea4186a45a15086524e47180e09baf55`.
Each contains 15 alternated-order paired samples × 75 validations on the
real current queue; all four behavioral holdouts passed.

| Python | Artifact ID | ZIP SHA-256 | Baseline median | Candidate median | Gain | Faster pairs |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| 3.11 | `13610162434` | `0a4d020c096cea86e52005b196750ee18665f9ece281e2b09a87bda6a0760c6c` | 107.281 μs | 104.323 μs | +2.757% | 14/15 |
| 3.12 | `13609949303` | `45211073fae1e01cef5788b01a30e55cd0f11ce9e2327b2981577ee40baf01bd` | 169.633 μs | 162.340 μs | +4.299% | 14/15 |

This is measured machine-side efficiency for **the current real public queue**.
It is not a universal production workload distribution, an SLA or monetary
ROI estimate. Human attendance data are not required for these measured
machine-side improvements. No extrapolated speedup is claimed.

### Implementation/release review — HOLD

1. **Generator saturation:** The existing `rsi/generators.json` registers
   precisely this source anchor. Applying the candidate causes the native
   generator to return `NO_APPLICABLE_RULE`, while existing native tests
   expect exactly one candidate and the federated ZIP verifier expects
   `GENERATED`. Updating a source line alone would regress registered
   source-coverage/CI acceptance. A separately reviewed retirement/saturation
   transaction must preserve exact-head source registration, testing and
   historical evidence without fabricating a new optimization.
2. **Scope expansion:** Only 19 current real records were measured, not
   worst-case future queue size/distribution. A larger representative input
   distribution and separate behavior/regression validation are required
   before general workload claims or implementation approval.
3. **Authorization:** This engineering review is not an Owner-authored
   approval of an implementation PR. The candidate remains
   `promotion_authorized=false`, `mutation_authority=false` and unapplied.
   A separate exact patch implementation PR, independent CI, explicit
   implementation review and applicable Owner authorization remain required.

**Next action:** Resolve the saturation-safe registry transition and
recheck the candidate against representative future queue shapes; then
obtain explicit reviewed approval for the exact implementation. Do not
merge a source-only optimization or start a production release from these
measurements.
