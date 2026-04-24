# Answer Contract

## Evidence Table Schema

Build this internal table before answering:

- `claim_id`: short identifier
- `claim_text`: atomic statement
- `source_title`
- `source_url`
- `source_section`
- `support_snippet`: short quote or tight paraphrase anchor
- `date_evidence`: `confirmed-within-30-days` only
- `refresh_status`: `refreshed` | `not-refreshed`
- `last_checked_at`: ISO 8601 timestamp
- `support_strength`: `strong` | `moderate` | `weak`

Drop claims with `weak` support.
Drop claims whose citations are missing `confirmed-within-30-days`.
Drop claims whose citations are `not-refreshed` or stale (`last_checked_at` older than 24 hours).

## Final Response Template

### Answer

- Provide only fully supported claims.
- Keep statements concise and scoped to the user question.

### Citations

1. `<title>`
   URL: `<url>`
   Section: `<heading-or-N/A>`
   Date evidence: `confirmed-within-30-days`
   Refresh status: `<refreshed|not-refreshed>`
   Last checked: `<ISO-8601>`

### Evidence Coverage

`<supported_claims>/<total_claims> claims supported`

### Gaps

- List unresolved points.
- Ask the user whether to continue with narrower scope if needed.
