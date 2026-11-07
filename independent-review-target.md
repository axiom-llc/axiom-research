# Reproducible Technical Review — Public Protocol

AXIOM supports evidence-oriented engineering review of bounded execution,
policy authorization, state recovery, and knowledge-system durability.

## Review method

1. Select public source revisions for the component under test.
2. State the exact contract and the falsifiable acceptance target.
3. Reproduce the component's publicly documented tests in an isolated,
   synthetic environment using the owning repository's instructions.
4. Preserve command output, version and environment fingerprints, and failures.
5. Separate demonstrated behavior from implementation intent, historical
   acceptance, vendor claims, and production-deployment assumptions.

## Evidence limitations

Passing local or CI tests provides scope-bound evidence about the selected
revision and test environment. Independent security assurance, deployment
status, customer outcomes, live integrations, and unrestricted autonomy require
additional direct evidence.

The original revision-specific system analysis, reproduction map, and detailed
internal verification targets have been preserved in private AXIOM storage.

See [publication controls](PUBLICATION.md) and [simulations](simulations/).
