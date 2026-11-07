# Public publication control

This repository is unrestricted worldwide disclosure. Every tracked file, branch,
commit, release artifact, workflow output, issue attachment, and external asset must
be treated as public regardless of its license.

## Decision classes

- `PUBLIC`: Approved public writing, synthetic demonstrations, validated
  metrics, documentation, and low-level interfaces safe for worldwide disclosure.
- `REDACT`: Publish a separately reviewed high-level summary; preserve the
  original in verified private storage with provenance and digest.
- `PRIVATE`: Personal/family/medical information, unpublished manuscripts,
  correspondence, identifying metadata, credentials, and private source evidence.
- `PROPRIETARY`: Implementation-specific algorithms, agent controls, internal
  architectures, optimization strategies, proprietary telemetry, pricing models,
  unpublished research, and sensitive security findings.

Unclear sensitivity or commercial differentiation means `PRIVATE` or
`PROPRIETARY` pending an owner review. A public-safe summary can be
`REDACT`. File extensions, "research-only" labels, and a restrictive content
license do not declassify source material.

## Required review before publication

1. Enumerate the complete proposed asset including history and attached media.
2. Check sensitive-personal, secret, third-party-rights, and proprietary-IP risk.
3. Preserve the complete restricted source in verified private retention first;
   record source revision, path, destination, and matching Git blob identity.
4. Publish only approved files or separately edited public summaries; verify
   relative links and run affected validation suites.
5. Evaluate historical refs, releases, forks, caches, searchable snippets, and
   external links independently. Removing a file in HEAD is insufficient.
6. Never rewrite shared Git history without explicit approval. Coordinate
   sensitive-history cleanup, impacted forks, and key rotation separately.

`python3 .github/scripts/publication_check.py` performs deterministic,
repository-wide scanning for restricted paths, common live-token patterns,
identifying records and binary data. It intentionally errs on preventing
exposure. A passing scan **does not establish** public approval for an asset.
Owner review remains required for intellectual-property and contextual risks.

Configure branch protections/rulesets to require successful publication checks
and owner review before merge. These protections must be verified in GitHub
settings; adding the workflow alone does not enforce branch protection.
