# AXIOM Reproducible Technical Review Target

## Purpose and scope

This is a bounded future-reviewer packet, not an audit, certification, assurance report, security review, or independent validation. It does not imply a favorable conclusion. Current source, tests, and CI outrank this packet.

The packet covers only the stated revisions and boundaries. It requires no provider call, production deployment, credential, package release, or external engagement.

## Canonical revisions

| Repository | Revision | Boundary |
| --- | --- | --- |
| ASON | `d6bc46c6cc22b14b7b807d045d1c6eb61752f337` | Policy validation and APEX submission. |
| APEX | `ec108abf8bcc6d78f09504ab9bffbea87c62cf6d` | Effect recovery, retries, RSI candidate isolation. |
| RAG | `42d7bda52fb70e0b724a24a9f91333f242bb3aad` | Persistence recovery, ownership, HTTP boundary. |
| Infra | `ee36d8350bf9d059bcc960a8aad735414748f495` | Compose topology and portfolio validation. |

```bash
git -C axiom-ason rev-parse HEAD
git -C axiom-apex rev-parse HEAD
git -C axiom-rag rev-parse HEAD
git -C axiom-infra rev-parse HEAD
```

## ASON policy boundary

**Demonstrated scope.** `ason.validator.validate` validates the complete caller-supplied plan before `ASONExecutor.submit` sends an APEX request. The adapter preserves tool order, names, and JSON arguments, adding only fixed APEX envelope fields and a terminal halt; it does not send APEX a planning `task`.

| Evidence | Expected result | Falsification |
| --- | --- | --- |
| `axiom-ason/ason/validator.py`, `ason/executor.py` | Validation precedes a `plan` submission. | Policy violation sends a request or submitted tool data changes. |
| `ason/tests/test_apex_integration.py::test_approved_plan_runs_exactly_once`, `::test_recorded_approved_plan_replays_without_replanning` | One submission, equal recorded plan/events, no replanning. | Planner is called or replay changes plan. |
| `::test_policy_blocks_before_http`, `::test_later_policy_violation_blocks_earlier_effect`, `::test_apex_rejects_invalid_args_before_earlier_write` | Later policy/schema failure prevents earlier effects. | Earlier effect or history transition occurs. |
| `ason/tests/test_rollback.py::test_write_file_requires_manual_review`, `::test_mixed_history_returns_no_partial_plan` | No automatic `write_file` or partial rollback plan. | Automatic inverse appears without required contracts. |
| `axiom-ason/.github/workflows/ci.yml`; [ASON CI 34779235479](https://github.com/axiom-llc/axiom-ason/actions/runs/34779235479) | Python 3.11/3.12 matching wheels, revision record, installed-runtime tests pass. | Declared workflow path is absent or fails. |

**Assumption/operational requirement.** Trusted application code selects policy and prevents callers from directly using the APEX credential/API. ASON does not establish that deployment boundary.

**Unsupported.** Durable ASON approval-identity binding to APEX recovery, architectural prevention of direct APEX bypass, automatic compensation, and stronger external-effect guarantees.

## APEX effect ambiguity and recovery

**Demonstrated scope.** APEX validates a complete plan and durably stores accepted plan/digest plus all intents before dispatch. Same-run recovery uses `INTENT_RECORDED`, `DISPATCHING`, `SUCCEEDED`, and `FAILED_UNKNOWN` conservatively.

| Evidence | Expected result | Falsification |
| --- | --- | --- |
| `axiom-apex/apex/history.py`, `apex/core/loop.py`, `apex/core/planner.py` | Binding/intents precede dispatch; complete validation precedes effects. | Dispatch occurs first or invalid later step permits an earlier effect. |
| `tests/test_effect_ledger.py::test_binding_and_intents_are_committed_before_dispatch`, `::test_invalid_later_step_blocks_direct_python_execution` | SQLite sees binding/intents before dispatch; invalid plan dispatches nothing. | Ordering or no-effect check fails. |
| `::test_process_crash_and_repeated_recovery`, `::test_recovery_rejects_binding_changes`, `::test_tool_cannot_mutate_bound_arguments` | Successes reuse results; `DISPATCHING` blocks; altered binding fails. | Uncertain dispatch retries, success re-runs, or changed plan succeeds. |
| `::test_observed_error_does_not_mean_no_effect`, `::test_outcome_storage_failure_blocks_recovery` | Unknown outcome becomes `FAILED_UNKNOWN`; recovery blocks. | Unknown effect is replayed. |
| `tests/test_tool_retries.py`; `test_effect_ledger.py::test_restart_during_retry_safe_delay_is_still_blocked` | Only explicit `retry_safe` tools retry in uninterrupted run; restart blocks ambiguity. | Unsafe tool or restart retries uncertainty. |
| `axiom-apex/.github/workflows/ci.yml`; [APEX CI 34757540895](https://github.com/axiom-llc/axiom-apex/actions/runs/34757540895) | Matching RAG, offline suite, build, installed smoke pass. | Declared path is absent or fails. |

**Unsupported.** Exactly-once external effects, provider reconciliation, submission deduplication, host-power-loss atomicity, distributed recovery, and automatic compensation/reconciliation. `SUCCEEDED` means acceptable tool JSON, not remote business commit proof.

## APEX RSI candidate isolation

**Demonstrated scope.** Isolation applies only to the RSI candidate/evaluation path, not ordinary APEX tools. CI exercises Bubblewrap namespaces, delegated cgroups, bounded candidate storage, and descriptor/socket controls.

| Evidence | Expected result | Falsification |
| --- | --- | --- |
| `axiom-apex/apex/_rsi_sandbox.py` | Candidate isolation is separate from ordinary tool execution. | Ordinary tools implicitly use this boundary or failed setup executes code. |
| `tests/test_rsi_isolation.py::test_files_environment_network_and_fds`, `::test_descendants_die_with_evaluation`, `::test_isolation_failure_never_runs_candidate`, `::test_runtime_readonly_privileges_and_unix_socket` | Tested candidate boundaries and fail-closed setup hold. | Candidate observes prohibited state or runs after setup failure. |
| `tests/test_rsi_resources.py::test_cpu_workers_share_quota`, `::test_memory_limit_is_aggregate_across_workers`, `::test_nested_namespace_cannot_rewrite_cgroup_limits`, `::test_limit_setup_failure_executes_nothing` | Tested resource controls are aggregate and fail closed. | Limits are bypassed or setup failure executes candidate. |
| `axiom-apex/.github/workflows/ci.yml`; [APEX CI 34757540895](https://github.com/axiom-llc/axiom-apex/actions/runs/34757540895) | Ubuntu 24.04 installs Bubblewrap, authorizes namespaces, delegates controllers, and runs probes. | Required controls are absent or probes fail. |

**Requirements.** Real probes require Linux, Bubblewrap, permitted user namespaces, AppArmor setup, and delegated `cpu`, `memory`, and `pids` cgroups; use CI where unavailable.

**Unsupported.** Sandbox coverage for every runtime tool, arbitrary host environments, or external effects beyond the candidate process.

## RAG persistence, ownership, and HTTP boundary

**Demonstrated scope.** RAG uses one cooperating owner per root, retained Chroma client, serialized supported access, journaled replacement, and process-crash recovery. The versioned server owns root/namespace/space/provider configuration; the client makes one request, refuses redirects, and has no direct-Chroma fallback.

| Evidence | Expected result | Falsification |
| --- | --- | --- |
| `axiom-rag/rag/store.py`, `rag/persistence.py`, `rag/space.py` | Advisory lock, retained owner/client, journal, exact space/vector validation. | Supported second owner acquires root, partial replacement appears, or invalid input mutates. |
| `tests/test_recovery.py::test_replacement_process_crash_recovers_exact_generation`, `::test_recovery_itself_can_be_interrupted`, `::test_ambiguous_journal_blocks_without_cleanup`, `::test_second_owner_excluded_and_sigkill_releases_lock`, `::test_supported_reads_wait_for_complete_replacement` | Tested recovery works; ambiguous journal fails closed; second cooperating owner excluded. | Stated recovery assertions fail. |
| `server/app.py`, `server/compat.py`, `rag/http_client.py`, `rag/remote.py`; `tests/test_http_compat.py::test_startup_inspection_creation_and_legacy`, `::test_raw_identity_metadata_and_replacement`, `::test_http_failure_recovery_outcome`, `::test_redirect_is_not_followed`, `::test_client_protocol_failures_never_retry`, `::test_client_import_does_not_load_store` | Exact namespace/space required; post-dispatch error is `unknown`; no retry/redirect/owner import/fallback. | Caller retries/follows redirect/opens Chroma, or server accepts unauthorized namespace/space. |
| `tests/test_remote.py::test_unmapped_config_never_dispatches`, `::test_settings_and_failure_are_single_attempt`, `::test_separate_owner_cli`; `test_http_compat.py::test_separate_owner_client_crash_recovery` | Unmapped calls do not dispatch; client attempts once and does not import owner storage. | Failed or unmapped call falls back or retries. |
| `axiom-infra/docker-compose.yml`, `README.md`, `.github/workflows/portfolio.yml`; [Infra CI 34775139347](https://github.com/axiom-llc/axiom-infra/actions/runs/34775139347) | RAG alone owns `rag_data` and provider credential; APEX uses `http://rag:8000` plus HTTP token/config assertion; dummy-credential Compose passes. | Caller receives persistence/provider credential, topology differs, or job fails. |
| `axiom-rag/.github/workflows/ci.yml`; [RAG CI 34773141533](https://github.com/axiom-llc/axiom-rag/actions/runs/34773141533) | RAG suite passes on Python 3.11/3.12. | Declared suite fails. |

**Requirements.** Crash tests cover local Linux filesystems and cooperating callers. Compose uses dummy credentials with no live provider call. Versioned clients require explicit URL, namespace, and embedding-space assertion; non-loopback bind requires token.

**Unsupported.** Host-power-loss/kernel-panic atomicity across Chroma SQLite/HNSW, distributed writers, non-cooperating direct Chroma writers, exactly-once HTTP effects, provider-key validity, production provenance, and evaluator migration.

## Reproduction procedure

Use clean sibling checkouts at recorded revisions with declared development dependencies. The focused commands require no paid/live provider access and must pass; do not substitute stale PyPI AXIOM packages.

```bash
(cd axiom-ason && python -m pytest ason/tests/test_apex_integration.py ason/tests/test_rollback.py -q)
(cd axiom-apex && python -m pytest tests/test_effect_ledger.py tests/test_tool_retries.py -q)
(cd axiom-rag && python -m pytest tests/test_recovery.py tests/test_http_compat.py tests/test_remote.py tests/test_store.py -q)
```

For installed-wheel ASON provenance, real Linux isolation, and Compose topology, use the cited existing workflows rather than weakening environment prerequisites. Do not create deployments or modify non-temporary persistence data.

## Acceptance, falsification, and output contract

Mark **VERIFIED within stated scope** only where revision, implementation, and reproductions agree and no listed falsifier occurs. Otherwise use only **PARTIALLY VERIFIED**, **NOT REPRODUCED**, **CONTRADICTED**, **OUT OF SCOPE**, or **INSUFFICIENT EVIDENCE**.

Any contradiction, failed test, revision mismatch, or missing environment control must include command, revision, environment, output, and affected claim. Passing tests do not establish broader properties.

Reviewer output must include revisions/environment, commands/results, one allowed classification per domain, assumptions, exclusions, deviations/contradictions, and recommended next evidence only. It must not claim certification, independent assurance, or production readiness.

## External-evidence gaps

This packet cannot establish independent review, production operation, live provider behavior, customer outcomes, real-world external-effect reconciliation, or deployment-specific credential/host controls. Those require separately authorized external or production evidence. It also cannot prove absence of defects outside reviewed source and tests.
