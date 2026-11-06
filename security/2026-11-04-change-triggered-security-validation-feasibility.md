# Change-triggered security validation — feasibility and `ship` specification

**Evaluated:** 2026-11-04  
**Disposition:** `ACCEPT_WITH_FOLLOWUP` — high-priority cross-repository capability candidate  
**Owner:** Research evidence in `axiom-research/security/`; implementation repository not selected  
**Status:** Evaluation only. No workflows, security settings, secrets, scanners, deployments, or production targets were changed.

## Original claim and evidence assessment

Claim: "Commits on GitHub have surged this year. Most teams still pentest once a year. Aikido pentests what changed, as you deploy."

| Component | Classification | Assessment |
| --- | --- | --- |
| GitHub-wide commit activity increased | **Verified aggregate fact** | GitHub's 2026 Octoverse reports **34.3 billion commits** for Oct 2025–Sep 2026, versus **12.9 billion** for the prior comparable year. Includes public and private GitHub repositories; it does **not** establish growth for any particular team or AXIOM repository. |
| “Most teams pentest once a year” | **Rejected as a general majority claim** | Cobalt's 2025 survey reports **27% annually**, **30% quarterly**, **18% monthly**, **15% semi-annually**, and **8% continuously** (other category roughly 1%). Its surveyed cohort is not a census of all software teams. The claim that most teams use annual-only testing is unsupported. |
| Periodic assessment can miss recently introduced regressions | **Plausible reasoning; workload-dependent** | A security assessment at one point in time cannot guarantee that subsequent code/configuration changes remain safe; its utility does not prove a prevalence statistic. |
| Triggering scanning from changes | **Verified existing capability** | GitHub CodeQL supports PR/push scanning and code-scanning findings; GitHub Advanced Security availability varies by repository visibility, ownership, plan, and Code Security entitlement. GitHub recommends default setup before advanced customization where eligible. |
| “Pentest what changed, as you deploy” | **Marketing-style proposal, not an established equivalence** | Automated SAST/SCA/secret checks can be run when changes are proposed; they are not the same as an adversarial manual penetration test. No verified evidence was supplied that Aikido specifically provides a universal full pentest for every deployment. Product-level claim remains unverified in this evaluation. |
| Continuous/full security assurance | **Rejected** | A passing automated scan does not establish absence of vulnerabilities, business-logic abuse, exploitable chains, or risk in untested infrastructure. |

**Practical opportunity:** Cut the time between introduction and detection of automatable security regressions while preserving targeted adversarial testing when warranted.

## Feasibility verdict and rank

- **Viable:** Yes, as an incremental security validation gate using existing remote CI where practical.
- **Utility:** High across repositories with meaningful code/configuration changes and CI coverage.
- **Effort:** Low–medium if existing GitHub-native scanning can be reused; higher if private-repository entitlements or compilation/runtime dependencies prevent this.
- **Implementation risk:** Low–medium, primarily false positives/negatives, cost, incomplete coverage, CI outages, and disruptive merge gating.
- **Relative priority:** Rank **1** over the Fireply-inspired manual reply-assistant candidate (rank **2**, medium utility/low–medium effort/low implementation risk). Full autonomous reply posting is excluded from the viable ranking because its platform-approval requirement is unresolved. Qualitative priorities are not measured ROI or authorized execution order.

## Minimal actionable specification — `change-triggered-security-validation`

**Goal:** Run available and appropriate security validation on security-relevant repository changes, associate findings with their triggering revision, and enforce an explicit, owner-approved merge policy. This is security regression detection, **not** full penetration testing.

**Functional requirements:**

1. Inspect the *selected* target repository's existing CI workflows, GitHub security configuration, supported source languages, branch protections, current findings, and Actions/Code Security eligibility before modifying anything.
2. Reuse repository-native pull-request triggers and existing available scanners (CodeQL/SAST, dependency or supply-chain analysis, and secret detection where supported). Do not introduce another scanner when an equivalent maintained control is already present.
3. Bind each run to the event, source revision, rules/configuration version, and scanner outcome. Treat results as valid only for covered components and scanning modes.
4. Distinguish newly introduced findings from known baseline findings where the selected tools support accurate comparison. Do not assert that every scanner restricts analysis to changed lines; event-triggered whole-repository scans may be the correct behavior.
5. Surface actionable findings with severity, affected file/package or rule, revision, and remediation or exception workflow.
6. Only after explicit policy selection, prevent merging when *new* findings violate the agreed threshold or required checks fail. Never silently treat a scan outage or missing scan output as a clean result.
7. Keep records in existing CI/alert/evidence surfaces instead of adding a new database, agent coordinator, custom policy engine, or third-party network scanner by default.

**Minimum scope:** one named repository and its existing CI; no portfolio-wide rollout, external target probing, automatic exploit attempts, production penetration tests, paid vendor adoption, or independent red-team replacement.

## Acceptance criteria

1. A test PR modifying an explicitly covered file/path causes a scan or a documented applicable check to run at the correct source revision.
2. A deliberately vulnerable *safe fixture* in the supported scope produces an actionable finding; a controlled clean fixture passes under the same configured scanner.
3. Findings are attributable to the revision and tool/rule configuration that produced them.
4. Existing/baseline findings are not silently mislabeled as new; where comparison is not supported, the result explicitly states that limitation.
5. A fixture exceeding the chosen severity/policy threshold fails the **required** merge check; an acceptable fixture passes.
6. Missing permissions, scanner crashes, incomplete required results, timeouts, or unsupported files/languages yield failure or explicit *unverified* coverage, never an unqualified green result.
7. Re-running with unchanged revision, configuration, and fixtures produces stable pass/fail classification and does not create duplicate independent work or contradictory statuses.
8. Reports do not disclose tokens, credentials, secret contents, or unrelated private data.
9. The resulting pipeline respects branch protection, free/approved capacity, and existing repository validation; no downgrade of tests or manual review.
10. Scope review confirms no unauthorized external scanning, no production effect, and no claim that a scan equals a penetration test.

## Dependencies and unresolved blockers

| Dependency / decision | Status | Resolution required before `ship` |
| --- | --- | --- |
| Target repository and accountable owner | **Unresolved** | Pick one repository, not the entire portfolio. |
| Existing workflow/security baseline | **Unverified for a chosen target** | Audit only the target's current CI, CodeQL/dependency/secret scanning, alert baseline, and required checks. |
| CodeQL eligibility and supported language | **Target-dependent** | Verify public/private visibility, GitHub Code Security entitlement, support for the language, and Actions permissions. Private repos cannot be assumed eligible. |
| Actions quota/cost | **Target-dependent** | Confirm sufficient remaining budget/capacity and no unauthorized incremental spend. |
| Required-check/branch-protection authority | **Unresolved** | Name an authorized merge policy owner and define threshold, exception handling, and branch configuration effects. |
| Finding baseline and false-positive handling | **Unresolved** | Define comparison method and bounded exception workflow; do not automatically suppress findings. |
| Tool coverage | **Unresolved** | State supported SAST/dependency/secrets categories and blind spots before advertising coverage. |
| Runtime validation | **Not performed** | Execute fixture-based tests only after implementation is separately authorized. |

## Rejected complexity and caveats

- **Reject:** per-commit live exploitation, full dynamic pentests on every push, external scanning without target authorization, blanket “pentest equivalent” claims, and unconditional enforcement across the portfolio.
- **Reject initially:** custom agent orchestration, parallel scanner farms, custom findings databases, bespoke scoring models, nonessential service infrastructure, or vendor substitution without coverage/cost evidence.
- **Retain:** scoped manual or independent penetration tests where threat model, regulations, major architecture changes, or business logic require them.
- **Distinguish:** a GitHub security scan is not proof that *every* modified component was scanned; languages, generated files, dependencies, and runtime exposure determine coverage.

## Subsequent triage / implementation planning

1. Compare candidate against existing AXIOM security/CI controls; if the chosen repo already satisfies the acceptance criteria, return **NO_OP** rather than introduce a duplicate.
2. Select one target and owner, establish entitlement and CI constraints, define severity/exception rules, then prepare the smallest repository-native workflow or settings change.
3. Validate against safe fixtures and live remote CI evidence, inspect the complete change and required-check behavior, and only then consider a separately authorized `ship`.
4. Keep `ship` limited to validated integration/commit/push. Deployment, production tests, external scanning, release, additional spend, and cross-repository rollout require separate authority.
5. If a target-dependent entitlement or permission is missing, record the exact blocker and stop; do not invent a technical workaround.

## Sources (verified 2026-11-04)

- GitHub Octoverse 2026, Oct 28 publication, commits and comparable yearly methodology: <https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/>
- Cobalt 2025 State of Pentesting, survey cadence: <https://www.cobalt.io/hubfs/State%20of%20Pentesting%202025/State-of-Pentesting-Report-2025.pdf>
- Cobalt State of Pentesting 2026, programmatic testing context (vendor research; not used to infer annual-testing majority): <https://resource.cobalt.io/state-of-pentesting-2026>
- GitHub CodeQL scanning: <https://docs.github.com/en/code-security/concepts/code-scanning/codeql/codeql-code-scanning>
- GitHub code-scanning default setup, prerequisites and access: <https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/configure-code-scanning/configure-code-scanning>
- GitHub advanced setup and PR/push triggers: <https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/configure-code-scanning/configuring-advanced-setup-for-code-scanning>
- AXIOM canonical `ship` workflow: <https://github.com/axiom-llc/axiom-director/blob/main/modules/workflows/ship.md>

## Scope completeness

The request referred to **three** input values but provided **two**. This is the complete security candidate; the Fireply candidate's full findings reside in the separately owned, [private AXIOM Director assessment](https://github.com/axiom-llc/axiom-director/blob/38493509d951bca82ce80de359d6e012815eef97/research/2026-11-04-fireply-reply-assistant-feasibility.md). No third candidate was inferred. No formal Research prompt was queued or marked complete by this feasibility analysis.
