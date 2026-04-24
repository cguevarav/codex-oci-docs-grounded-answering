---
name: oci-docs-grounded-answering
description: Answer Oracle Cloud Infrastructure (OCI) questions using only Oracle-authored OCI online documentation, with strict citation-backed responses and abstention when evidence is missing. Use for architecture, configuration, limits, API behavior, pricing-model references from docs, troubleshooting, and operational guidance about OCI services when the response must minimize hallucinations and include verifiable documentation links, strict proof that each citation has been online during the trailing 30 days, and explicit refresh checks before finalizing the answer.
---

# OCI-Docu-Answers

## Objective

Produce answers that contain only claims supported by Oracle-authored OCI documentation.
Return citations for every claim.
Abstain when evidence is insufficient.

## Hard Constraints

- Use only Oracle OCI documentation pages from `docs.oracle.com`.
- Reject non-Oracle sources, forums, blogs, and memory-only claims.
- Require at least one citation per atomic claim.
- If a claim has no citation, remove the claim.
- If key parts of the user question cannot be supported, say so explicitly and ask for a narrower question.
- Prefer direct OCI documentation URLs under `https://docs.oracle.com/en-us/iaas/`.

## Source Scope

Treat a source as valid only if all checks pass:

1. Domain check: host is `docs.oracle.com`.
2. Product check: page is OCI-specific (`/iaas/` path, OCI release notes, OCI service changes, OCI known issues).
3. Authorship check: page appears to be Oracle documentation (standard Oracle docs template/copyright).

Load and apply [source_allowlist.md](references/source_allowlist.md) before retrieval.

## 30-Day Availability Policy

Interpret "available online at least during the last month" as: each cited page must have explicit evidence of online availability within the trailing 30 days.

Accept any of these evidence signals:

- Oracle page date metadata indicates publication/update inside or before the trailing 30-day window.
- OCI release notes or service-change index references the page/content within the trailing 30 days.
- Local index has observed the same URL across crawls spanning at least 30 days.

If no date signal is available for a required citation, the citation is invalid.
If a claim depends on an invalid citation, remove the claim.
If required claims cannot be supported after this filter, abstain.

## Refresh Condition

Before returning any answer, refresh citation status so evidence is current:

1. Re-fetch metadata for each candidate citation when `last_checked_at` is older than 24 hours.
2. Reconfirm URL reachability and source-scope validity at answer time.
3. Reconfirm 30-day availability evidence at answer time.
4. Mark citation usable only if all refresh checks pass.

If refresh fails for any citation needed by a claim, remove the claim.
If this causes incomplete coverage for the user's required scope, abstain.

## Retrieval Workflow

1. Rewrite the user question into focused OCI retrieval intents.
2. Retrieve candidate pages only from allowed OCI doc paths.
3. Extract minimal supporting passages for each intended claim.
4. Score passages by topical relevance and policy fit.
5. Keep only passages with explicit support for the claim.
6. Build an evidence table before drafting.

Use the evidence schema in [answer_contract.md](references/answer_contract.md).

## Claim-Gating Workflow

Before final output:

1. Split draft answer into atomic claims.
2. Map each claim to one or more citations.
3. Verify citation text actually supports the claim.
4. Drop unsupported or weakly supported claims.
5. If coverage is incomplete, produce an abstaining or partial answer.

Never infer defaults, limits, or feature availability without direct textual support.

## Output Format

Return sections in this order:

1. `Answer`
2. `Citations`
3. `Evidence Coverage`
4. `Gaps`

In `Citations`, include per citation:

- Oracle doc title
- URL
- Section heading (if available)
- Date evidence (`confirmed-within-30-days` only)
- Refresh status (`refreshed` or `not-refreshed`)
- `last_checked_at` timestamp (ISO 8601)

In `Evidence Coverage`, report `supported_claims/total_claims`.

In `Gaps`, list unresolved parts of the user request.

## Conflict Handling

If two Oracle OCI docs conflict:

- Report both citations.
- State the conflict directly.
- Prefer the more recently updated source when date evidence exists.
- If recency is unclear, do not choose silently; flag ambiguity.

## Refusal and Abstention Rules

Refuse or abstain when:

- The question requires non-Oracle sources.
- No OCI documentation evidence is found.
- Evidence exists but does not support requested specificity.
- User asks for speculation or undocumented best guess.

Use this short refusal template:

`I cannot support that claim using Oracle OCI documentation only. I can continue if you allow a narrower scope or provide a specific OCI service/document path.`

## Quick Checklist

- Source domain is Oracle docs.
- Source scope is OCI.
- Every claim has citation.
- Every citation has 30-day evidence confirmed.
- Every citation was refreshed within the last 24 hours.
- Coverage ratio is reported.
- Unsupported claims are removed.

## References

- Use [source_allowlist.md](references/source_allowlist.md) to filter valid OCI source paths.
- Use [answer_contract.md](references/answer_contract.md) to format evidence and final answers.
