# Zero-cost compute harness: primary-source revalidation

Status: canonical research, revalidated 2026-09-22.

## Scope and method

This asset independently re-researches the supplied zero-cost compute-pool proposal against current primary/official provider documentation. The supplied document is a claim inventory, not evidence. Current provider documentation outranks its numbers. “Verified” means the cited official source currently supports the material claim; “qualified” means an important condition changes its operational interpretation; “unresolved” means reviewed primary material does not establish the claimed durability/cadence.

This is capacity research, not evidence that AXIOM has accounts, credentials, quota, or successful runtime integration.

## Findings

| Resource | Finding | Current evidence / correction | Harness interpretation |
|---|---|---|---|
| Groq Free | VERIFIED | GPT-OSS 120B/20B and Qwen 3.8 27B are currently listed at 30 RPM, 1,000 RPD, 8K TPM and 200K TPD; 429 and rate-limit headers are documented. [G1] | Strong direct-API pool; limits remain model-specific. |
| Cloudflare Workers AI | VERIFIED | 10,000 Neurons/day at no charge; reset 00:00 UTC. Some models require paid billing. [C1] | Strong recurring inference pool; model eligibility must be discovered. |
| Gemini Developer API | VERIFIED, DYNAMIC | Google documents RPM/TPM/RPD, per-project limits, midnight-Pacific RPD reset, model/tier variation, and non-guaranteed actual capacity. [GO1] | Discover account/model limits; do not hard-code one free quota. |
| OpenRouter free models | VERIFIED | openrouter/free routes among zero-token-price models. Official material states 50 free-model requests/day and 20 RPM without loaded credits; >=$10 credits raises daily ceiling to 1,000. [OR1][OR2] | Zero-additional-spend baseline is 50/day unless account already satisfies credit condition. |
| IBM watsonx.ai Runtime Lite | VERIFIED | Lite includes 300,000 tokens/data points/month, 20 CUH/month and 100 pages/month; inactive Lite services can be deleted after 30 days. [IBM1] | Recurring pool with inactivity lifecycle handling. |
| Cohere evaluation keys | VERIFIED | Evaluation/trial keys are free/limited; current Chat trial use is 20 req/min and trial keys are capped at 1,000 API calls/month. [CO1] | Low-volume fallback/specialized pool. || Hugging Face routed inference | VERIFIED | Free users receive $0.10/month, explicitly subject to change. [HF1] | Tiny recurring emergency/experimentation pool. |
| Hugging Face ZeroGPU | VERIFIED | Free accounts receive 5 GPU-min/day; 48 GB large and 96 GB xlarge are documented, with xlarge consuming 2x quota. Eligible free accounts can host up to two ZeroGPU Spaces. [HF2] | Short GPU micro-bursts only; queueing and Gradio-only hosting constrain use. |
| Modal Starter | VERIFIED | Starter is $0 and includes $30/month compute. [M1] | Strong recurring general compute pool. |
| Lightning AI Free | CORRECTED | Current pricing says “up to 30 free credits to start”: 5 on registration and 25 more after adding a card; unused free credits expire after 12 months. “Up to 80 GPU hours” derives from these credits. A free CPU Studio can run with four-hour restarts. [L1] | Do not model GPU credits as recurring monthly capacity. Treat as signup/exhaustible capacity plus constrained free CPU Studio. |
| Oracle Cloud Always Free | VERIFIED | Always Free persists after trial; A1 is equivalent to 2 OCPUs/12 GB total and AMD E2.1.Micro instances remain listed. Capacity can be unavailable. [O1][O2] | Strong always-on control-plane candidate if provisionable. |
| Google Cloud Free Tier | VERIFIED, QUALIFIED | Google lists one e2-micro/month, Cloud Run 2M requests/month and Cloud Build 120 build-min/day. Limits are ongoing but subject to change and eligibility. [GC1] | Useful control/serverless/build pools. |
| GitHub Actions public | VERIFIED | Standard hosted runners are free/unlimited for public repos; current standard public Linux runner is 4 CPU/16 GB/14 GB SSD. [GH1] | Legitimate CI/validation pool, not generic persistent worker farm. |
| CircleCI | VERIFIED | Free gives 30,000 credits/month; qualifying public open-source Linux builds can use up to 400,000 credits/month. [CI1] | CI/batch pool; eligibility and per-resource credit cost must be tracked. |
| GitLab.com CI | VERIFIED | Free namespaces receive 400 compute minutes/month. [GL1] | Modest recurring CI pool. |
| Kaggle GPU | VERIFIED | Kaggle documents free Tesla P100 access and weekly GPU quota of 30 hours or sometimes higher depending on demand/resources. [K1] | Interactive/bounded batch GPU pool; capacity is demand-sensitive. |
| Google Colab Free | VERIFIED RESTRICTION | Free runtimes are interactive, at most 12 hours depending on availability/usage, and prohibit remote-control and distributed-worker uses. [COL1] | Exclude from unattended harness execution; manual compute only. |
| Cloudflare Workers | VERIFIED | Free: 100,000 requests/day, 10 ms CPU/request, 128 MB memory; request quota resets midnight UTC. [C2] | Lightweight router/webhook/control edge, not compute worker. || Deno Deploy | VERIFIED | Free: 1M requests/month, 10 active CPU-hours/month, 150 GiB-hours memory, 20 GiB egress. [D1] | Secondary scale-to-zero control plane. |
| Netlify Free | VERIFIED | Free is $0 with a hard 300-credit/month limit and includes Functions and Agent Runners. [N1] | Small independent serverless/agent-trigger pool. |
| Scaleway Generative APIs | QUALIFIED / CADENCE UNRESOLVED | Official docs confirm a 1,000,000-token Free Tier and OpenAI compatibility, but reviewed primary text does not establish that this allowance renews monthly/daily. [S1][S2] | Free allowance of unresolved renewal semantics, not recurring capacity. |
| OpenCode Zen free models | VERIFIED TEMPORARY | Current docs identify multiple free models as limited-time offers. [OC1] | Opportunistic only; never durable capacity. |
| GitHub Models | VERIFIED RETIRED | GitHub states the service was fully retired 2026-07-30. [GH2] | Exclude. |

## Claims not promoted to canonical capacity

The supplied proposal also named SiliconFlow, Azure Pipelines, Vercel Hobby, GitHub Codespaces, Gemini CLI/Code Assist quotas, and several trial-credit inference providers. They may be viable, but this revalidation pass did not obtain enough current primary evidence to promote every supplied numeric allowance into the canonical table. They remain provider-specific follow-up candidates rather than assumed capacity.

The original claim that Lightning AI provides a recurring monthly GPU pool is contradicted by current primary pricing: free GPU credits are signup credits, not a documented monthly refill. Scaleway's one-million-token Free Tier is real, but renewal cadence remains unresolved in reviewed primary material. These distinctions materially change scheduler design.

## Canonical architecture implications

The proposed separation between an inference pool and execution pool remains technically coherent, but provider ranking should not be encoded as timeless research truth. The scheduler should select from verified account-local capability records.

A provider record should preserve: provider ID; resource class; protocol; capabilities; zero-cost allowance type (recurring, signup, temporary, unknown-cadence); observed remaining quota when available; reset/cooldown when evidenced; health; account eligibility state; and evidence timestamp/reference. Provider APIs/headers override static research numbers at runtime.

Expected states remain available, rate_limited, quota_exhausted, capacity_unavailable, auth_failed, temporary_error, and disabled. A quota response is a scheduling transition, not a reason to evade limits. CI services belong to legitimate CI/build/test/validation workloads; interactive notebook services must not be repurposed contrary to platform restrictions.

## Evidence boundaries

Verified allowances are snapshots as of 2026-09-22, not contractual guarantees of future free capacity. “Free” may still require account creation, identity verification, payment method, region eligibility, or provider terms. No claim here establishes that an AXIOM-controlled account currently has the allowance. Runtime account inspection and a minimal authorized smoke test are required before marking a backend operational.## Primary sources

- [G1] Groq, Rate Limits: https://console.groq.com/docs/rate-limits
- [C1] Cloudflare, Workers AI Pricing: https://developers.cloudflare.com/workers-ai/platform/pricing/
- [C2] Cloudflare, Workers Limits: https://developers.cloudflare.com/workers/platform/limits/
- [GO1] Google, Gemini API Rate Limits: https://ai.google.dev/gemini-api/docs/rate-limits
- [OR1] OpenRouter, Free Models Router: https://openrouter.ai/openrouter/free/
- [OR2] OpenRouter, Lowest-Cost LLM Inference guide: https://openrouter.ai/blog/tutorials/how-to-get-the-lowest-cost-llm-inference-on-openrouter/
- [IBM1] IBM Cloud, watsonx.ai Runtime catalog: https://cloud.ibm.com/catalog/services/watsonxai-runtime
- [CO1] Cohere, API Key and Rate Limits: https://docs.cohere.com/v1/docs/rate-limits
- [HF1] Hugging Face, Inference Providers Pricing: https://huggingface.co/docs/inference-providers/en/pricing
- [HF2] Hugging Face, ZeroGPU: https://huggingface.co/docs/hub/spaces-zerogpu
- [M1] Modal, Pricing: https://modal.com/pricing
- [L1] Lightning AI, Pricing: https://lightning.ai/pricing/
- [O1] Oracle, OCI Free Tier: https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier.htm
- [O2] Oracle, Always Free Resources: https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
- [GC1] Google Cloud, Free Tier: https://cloud.google.com/free
- [GH1] GitHub, GitHub-hosted runners: https://docs.github.com/en/actions/reference/runners/github-hosted-runners
- [GH2] GitHub, GitHub Models: https://docs.github.com/en/github-models
- [CI1] CircleCI, Credits: https://circleci.com/docs/guides/plans-pricing/credits/
- [GL1] GitLab, Compute Minutes: https://docs.gitlab.com/ci/pipelines/compute_minutes/
- [K1] Kaggle, Efficient GPU Usage: https://www.kaggle.com/docs/efficient-gpu-usage
- [COL1] Google, Colab FAQ: https://research.google.com/colaboratory/faq.html
- [D1] Deno, Deploy Pricing: https://deno.com/deploy/pricing
- [N1] Netlify, Pricing: https://www.netlify.com/pricing/
- [S1] Scaleway, Generative APIs: https://www.scaleway.com/en/generative-apis/
- [S2] Scaleway, Generative APIs FAQ: https://www.scaleway.com/en/docs/generative-apis/faq/
- [OC1] OpenCode, Zen: https://opencode.ai/docs/zen

## Revalidation rule

Before implementation, re-open the provider's primary source and record the account-visible limit where available. Any contradiction between this document and live provider/account state resolves in favor of live primary/account evidence. Revalidate when an adapter is implemented, a quota changes unexpectedly, or a provider becomes operationally important.
