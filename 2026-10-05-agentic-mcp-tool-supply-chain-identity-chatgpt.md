# Minimal identity and version binding for MCP and remote tools

- Queue item: `RQ-2026-10-04-012`
- Date: 2026-10-05
- Target: `chatgpt`
- Classification: research synthesis; no production control change
- Decision status: `ACCEPT_WITH_FOLLOWUP`

## Question

What minimal identity/version binding should complement tool-schema digests so an agent can detect MCP or remote-tool implementation changes, endpoint substitution, and rug-pull behavior without requiring heavyweight attestation?

## Executive finding

Use a small, locally trusted **tool binding manifest** whose approved identity is derived from evidence outside the tool's own descriptive payload.

For every high-risk remote tool, bind:

1. the exact canonical endpoint/resource URI;
2. the expected authorization-server issuer or other independently configured trust domain;
3. the transport kind and protocol-version policy;
4. the normalized tool-schema digest;
5. an implementation evidence type and value when one is independently verifiable;
6. an owner-approved monotonically increasing binding generation.

For local/stdio tools, replace network identity with the exact launch command plus the executable or resolved package artifact digest. Treat MCP `serverInfo.name` and `serverInfo.version` only as telemetry: the current MCP specification explicitly says these fields are self-reported, unverified, and unsuitable for security decisions.

Any unexpected change to a security-bound field puts the tool in `QUARANTINED`. High-risk calls fail closed until an authorized manifest update records the new binding. A schema match alone never proves implementation identity.

This is the smallest deployable control because it reuses TLS/OAuth identity for remote endpoints, content digests for local artifacts, and AXIOM's existing explicit approval/receipt model. It does not introduce a new PKI, transparency log, or general software-attestation platform.

**Hard limit:** a provider can replace code behind the same authenticated endpoint while preserving the same schema. Without independently signed provenance, a deployment identifier from a trusted control plane, or reproducible artifact access, that event is not cryptographically detectable. The correct state is `IMPLEMENTATION_UNVERIFIABLE`, not a fabricated identity claim.

## Primary and authoritative evidence

### 1. MCP 2026-07-28 discovery and versioning

The modern MCP specification requires servers to implement `server/discover`; the response reports supported protocol versions, capabilities, and `serverInfo`. The same specification states that `serverInfo` is self-reported, is not verified by the protocol, and should not drive security decisions. Protocol versions and capabilities support compatibility checks, not implementation authentication.

- https://modelcontextprotocol.io/specification/2026-07-28/server/discover
- https://modelcontextprotocol.io/specification/2026-07-28/basic/versioning

### 2. MCP authorization and protected-resource identity

The current MCP authorization specification requires HTTP MCP servers to publish OAuth Protected Resource Metadata, clients to use it for authorization-server discovery, resource indicators to name the intended MCP server, and servers to validate token audience. It defines the canonical MCP server URI as the OAuth resource identifier. These bindings distinguish the intended protected resource and issuer; they do not identify the deployed code revision.

- https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization

### 3. RFC 9728 protected-resource metadata

RFC 9728 requires the returned `resource` value to exactly match the protected resource identifier used to derive the metadata URL and requires TLS certificate checking. This is useful against endpoint impersonation. Signed metadata is optional and can strengthen metadata integrity when its issuer is independently trusted.

- https://www.rfc-editor.org/rfc/rfc9728.html

### 4. RFC 9525 TLS service identity

RFC 9525 specifies how a client constructs reference identifiers independently and verifies them against identifiers presented in a TLS certificate. This authenticates the network service name under PKIX; it does not attest the server's application code.

- https://www.rfc-editor.org/rfc/rfc9525.html

### 5. MCP security guidance

MCP security guidance describes malicious discovery URLs, redirects, DNS rebinding, local-server compromise, token passthrough, and confused-deputy risks. It recommends HTTPS, validation of redirect destinations, private-address protections, audience binding, and sandboxing. These controls are prerequisites for treating endpoint identity as meaningful.

- https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices

### 6. TUF and SLSA as upper-bound references

TUF demonstrates that signed versioned metadata, expiration, hashes, and persistent client state address rollback, freeze, and mix-and-match attacks. SLSA provenance demonstrates how an artifact can be bound to a builder and build definition. Both are useful design references, but adopting either whole framework would exceed this queue item's minimum-control objective.

- https://theupdateframework.io/docs/security/
- https://theupdateframework.io/docs/metadata/
- https://slsa.dev/spec/v1.2/build-provenance

## Evidence boundaries

The cited standards establish service-name authentication, resource/issuer binding, protocol discovery, and stronger software-supply-chain patterns. They do **not** establish that:

- TLS identity equals implementation identity;
- an OAuth issuer controls or attests the MCP implementation;
- a self-reported server version is truthful;
- an unchanged schema implies unchanged behavior;
- a digest observed from the same potentially compromised server is independent evidence;
- every hosted provider exposes a stable deployment or artifact identifier.

Those distinctions are mandatory. A control that hashes only `tools/list` detects interface drift but does not close the same-schema rug-pull case.

## Threat model

### In scope

- configuration substitution to a different HTTP origin or path;
- OAuth resource or issuer substitution;
- redirects or discovery metadata that move authorization to an unexpected domain;
- replacement of a local executable, package, container, or launch command;
- tool-schema additions, removals, or semantic-surface changes visible in the schema;
- rollback to a previously seen, no-longer-approved binding;
- provider-published deployment/release changes when a trusted identifier exists;
- accidental use of a different MCP protocol era or unsupported version.

### Out of scope

- a malicious provider changing behavior behind the same authenticated endpoint and same schema when no independent deployment evidence exists;
- compromise of AXIOM's local manifest/approval store or its signing/authorization authority;
- compromised roots of trust such as the platform account, package registry, OAuth issuer, or PKIX ecosystem;
- semantic behavior changes invisible to schema and synthetic probes;
- proving reproducible builds or end-to-end binary provenance for SaaS.

## Minimal binding manifest

A normalized record is sufficient:

```json
{
  "binding_schema": "axiom-tool-binding/v1",
  "tool_set_id": "github",
  "risk": "HIGH",
  "transport": "streamable-http",
  "endpoint": {
    "canonical_resource_uri": "https://example.invalid/mcp",
    "redirect_policy": "same-origin-only",
    "auth_issuers": ["https://issuer.example.invalid"]
  },
  "protocol": {
    "allowed_versions": ["2026-07-28"],
    "server_info_observed": {"name": "example", "version": "1.2.3"}
  },
  "interface": {
    "canonicalization": "axiom-tool-schema-c14n/v1",
    "sha256": "<normalized tools/resources/prompts schema digest>"
  },
  "implementation": {
    "evidence_type": "provider-deployment-id | artifact-sha256 | package-lock | none",
    "evidence_value": "<value or null>",
    "trust_source": "<independent control plane/package registry/local filesystem or null>"
  },
  "generation": 7,
  "approved_at": "<RFC3339>",
  "approved_by": "<authority receipt id>"
}
```

Rules:

1. `endpoint.canonical_resource_uri` is exact after one documented canonicalization pass. Do not silently treat different paths, ports, or schemes as equivalent.
2. `auth_issuers` comes from approved configuration or previously validated protected-resource metadata, not from an untrusted tool response accepted in the same transaction.
3. `server_info_observed` is logged but excluded from the security identity because MCP defines it as self-reported.
4. `interface.sha256` covers deterministic normalized schemas, annotations, protocol feature declarations, and names. Descriptions should be included because altered descriptions can change model behavior.
5. `implementation.evidence_value` is security-bound only when its trust source is independent of the tool endpoint. A version string returned by the server is not enough.
6. `generation` must strictly increase on every approved binding change. Clients persist the highest approved generation to reject rollback.
7. The manifest is immutable once approved. Updates create a new record linked to the prior record and approval receipt.

## Transport-specific identity evidence

| Tool form | Minimum independent binding | Stronger optional evidence | Residual risk |
|---|---|---|---|
| Remote HTTP MCP | Exact HTTPS resource URI, RFC 9525 TLS validation, exact RFC 9728 resource match, expected OAuth issuer, schema digest | Signed protected-resource metadata; provider control-plane deployment ID; signed provenance | Same endpoint/issuer can serve changed code |
| Remote non-MCP API | Exact HTTPS origin/path policy, TLS identity, expected account/installation/tenant ID from trusted control plane, API-schema digest | Provider deployment/release attestation | Provider backend may change invisibly |
| Local stdio executable | Exact command/arguments, executable SHA-256, restricted environment, schema digest | Package signature or provenance | Interpreter and dependencies may drift unless included |
| Package-launched stdio | Locked package name/version/source plus resolved artifact digest and command, schema digest | Registry signature/provenance | Registry/account compromise; transitive dependency drift if lock incomplete |
| Containerized tool | Image manifest digest, exact entrypoint/args, mounted capability set, schema digest | Signed image provenance | Runtime/kernel/base service dependencies remain outside the digest |

## Enforcement state machine

`UNSEEN -> VERIFIED -> QUARANTINED -> VERIFIED(new generation)`

### Connection-time algorithm

1. Load the highest authorized manifest generation for the logical tool set.
2. Resolve the configured endpoint or local artifact from that manifest, never from model output.
3. For HTTP, validate TLS service identity; enforce redirect and address policy; fetch and validate protected-resource metadata; require exact resource and approved issuer matches.
4. For local tools, hash the resolved artifact and compare the exact launch command and dependency lock identity.
5. Negotiate only an allowed MCP protocol version.
6. Retrieve capabilities and schemas; canonicalize using the manifest's named algorithm; compare the digest.
7. Obtain implementation evidence from the independently trusted source when configured. Never accept a replacement evidence source merely because the tool advertises it.
8. If every required field matches, enter `VERIFIED`; otherwise enter `QUARANTINED` with stable reason codes.
9. Permit high-risk calls only in `VERIFIED`. Quarantine is sticky for the transaction.

### Stable mismatch reasons

- `ENDPOINT_MISMATCH`
- `TLS_IDENTITY_INVALID`
- `RESOURCE_ID_MISMATCH`
- `AUTH_ISSUER_MISMATCH`
- `REDIRECT_POLICY_VIOLATION`
- `PROTOCOL_VERSION_MISMATCH`
- `SCHEMA_DIGEST_MISMATCH`
- `ARTIFACT_DIGEST_MISMATCH`
- `DEPLOYMENT_ID_MISMATCH`
- `BINDING_ROLLBACK`
- `IMPLEMENTATION_EVIDENCE_MISSING`
- `IMPLEMENTATION_UNVERIFIABLE`

## Change policy

Not every change is malicious, but no security-bound drift should be auto-accepted.

- **High risk:** fail closed; require explicit manifest revision and approval.
- **Moderate risk:** quarantine mutations; optionally allow separately classified read-only calls only if the policy proves they cannot create external effects.
- **Low risk:** log drift and require bounded revalidation before the next effectful call.

An approval must show a semantic diff: endpoint, issuer, schema additions/removals, annotation changes, requested capabilities, implementation evidence, and generation. Approving only a new aggregate digest is insufficient because it hides what changed.

## Rollback and freeze handling

A digest detects difference, not freshness. Add only the minimum durable state:

- highest approved `generation` per logical tool set;
- current and immediately previous approved manifest digest;
- approval timestamp and receipt;
- optional expiry/recheck deadline for externally supplied implementation evidence.

Reject a lower generation even if its manifest was once valid. Do not let the server choose the generation. If no independently trustworthy freshness source exists, record that limitation and treat silent provider changes as undetectable rather than inventing a timestamp guarantee.

## Compatibility analysis

### Why this remains KISS

- one small manifest schema;
- SHA-256 over existing schema/artifact material;
- reuse of RFC 9525 and RFC 9728 validation already required for secure HTTP authorization;
- one monotonic integer and immutable approval receipt;
- no new online verifier, CA, blockchain, transparency log, or continuously running service.

### Expected integration cost

- deterministic schema canonicalization must be versioned;
- HTTP connector setup must expose the canonical resource and approved issuer;
- local launchers must resolve the actual executable/package artifact before hashing;
- the runtime must retain the highest approved generation outside model-controlled state;
- tool selection must check verification state before effect authorization.

These are implementation hypotheses until AXIOM's actual connector registry and admission path are inspected.

## Synthetic validation matrix

All cases use inert fixtures and offline endpoints.

| ID | Mutation | Expected result |
|---|---|---|
| B1 | Exact approved binding | `VERIFIED` |
| B2 | Host changed, identical schema | `QUARANTINED: ENDPOINT_MISMATCH` |
| B3 | Path changed on same host | `QUARANTINED: ENDPOINT_MISMATCH` |
| B4 | Valid TLS for unexpected host | `QUARANTINED: ENDPOINT_MISMATCH` |
| B5 | Invalid TLS name for expected host | `QUARANTINED: TLS_IDENTITY_INVALID` |
| B6 | Protected-resource `resource` differs by port/path | `QUARANTINED: RESOURCE_ID_MISMATCH` |
| B7 | Authorization issuer changed | `QUARANTINED: AUTH_ISSUER_MISMATCH` |
| B8 | Redirect crosses origin | `QUARANTINED: REDIRECT_POLICY_VIOLATION` |
| B9 | Tool parameter added | `QUARANTINED: SCHEMA_DIGEST_MISMATCH` |
| B10 | Tool description changed only | `QUARANTINED: SCHEMA_DIGEST_MISMATCH` |
| B11 | Tool annotations changed only | `QUARANTINED: SCHEMA_DIGEST_MISMATCH` |
| B12 | Self-reported server version changed only | telemetry change; no identity conclusion |
| B13 | Local executable bytes changed, schema same | `QUARANTINED: ARTIFACT_DIGEST_MISMATCH` |
| B14 | Locked package source changed, version same | `QUARANTINED: ARTIFACT_DIGEST_MISMATCH` |
| B15 | Manifest generation lower than highest seen | `QUARANTINED: BINDING_ROLLBACK` |
| B16 | Deployment ID changed at trusted provider control plane | `QUARANTINED: DEPLOYMENT_ID_MISMATCH` |
| B17 | Deployment ID claimed only by tool itself | `IMPLEMENTATION_EVIDENCE_MISSING` |
| B18 | Same endpoint, schema, issuer, no independent deployment evidence; backend changed | `IMPLEMENTATION_UNVERIFIABLE`; test demonstrates limitation, not detection |
| B19 | New manifest approved with semantic diff and higher generation | `VERIFIED(new generation)` |
| B20 | Approval for tool A replayed for tool B | deny |

## Zero-cost MVE

Build an offline validator over manifest fixtures only after inspecting the owning registry/enforcement repository.

1. Define canonicalization fixtures for tools, resources, prompts, annotations, and descriptions.
2. Replay B1-B20 without network access or real credentials.
3. Assert verification state, reason code, and whether high-risk calls are admitted.
4. Prove digest determinism by shuffling JSON object keys and list inputs whose ordering is semantically irrelevant.
5. Prove semantic sensitivity by mutating descriptions, annotations, endpoint path, issuer, package source, and artifact bytes.
6. Persist the highest generation in a tamper-resistant location already controlled by AXIOM; verify rollback rejection across process restart.
7. Record `IMPLEMENTATION_UNVERIFIABLE` for SaaS fixtures lacking independent evidence.

Proposed promotion gates are hypotheses, not measured results:

- all B2-B17 and B20 mismatches fail closed for high-risk calls;
- B1 and B19 are admitted deterministically;
- canonicalization produces identical digests for semantically identical fixtures;
- changed descriptions and annotations never disappear through normalization;
- B18 is never misreported as verified implementation continuity;
- validation adds no external service or incremental hosted cost.

## Rejection criteria

Reject or redesign the proposal if:

1. the runtime accepts a new endpoint, issuer, artifact, deployment ID, or schema without a new authorized generation;
2. tool-supplied `serverInfo` is treated as independent identity evidence;
3. redirect or discovery processing can escape the approved resource/issuer policy;
4. normalization omits model-relevant descriptions or effect annotations;
5. rollback is accepted after process restart;
6. an unavailable implementation attestation is silently replaced by self-attestation;
7. adoption requires a new PKI or online attestation service before the basic endpoint/artifact binding can provide value;
8. false confidence is created for same-endpoint, same-schema SaaS changes.

## Decision

**ACCEPT_WITH_FOLLOWUP.** The minimum control worth testing is a versioned tool binding manifest combining:

- independent transport/resource/issuer identity;
- protocol policy;
- normalized schema digest;
- independently sourced implementation evidence when available;
- monotonic owner-approved generation and rollback memory.

Do not promote MCP `serverInfo` into a security control. Do not claim that endpoint and schema binding detects every provider rug pull.

## Implementation candidate

None is authorized or justified yet. A bounded candidate becomes available only after inspecting the repository that owns AXIOM's tool registry/admission path and confirming:

1. where canonical endpoint and issuer configuration lives;
2. whether existing schema digests include descriptions and annotations;
3. whether local artifact or provider deployment identifiers are exposed independently;
4. where monotonic generation state can be persisted and checked;
5. which high-risk calls can be blocked centrally before dispatch.

That inspection should produce one owner repository, one enforcement hook, and one native validation command before code is proposed.