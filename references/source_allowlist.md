# OCI Source Allowlist

Accept only URLs that match one of the following patterns:

- `https://docs.oracle.com/en-us/iaas/Content/*`
- `https://docs.oracle.com/en-us/iaas/releasenotes/*`
- `https://docs.oracle.com/en-us/iaas/api/*`
- `https://docs.oracle.com/iaas/Content/*`
- `https://docs.oracle.com/iaas/releasenotes/*`

Exclude by default unless explicitly approved:

- `*.pdf` outside OCI doc paths
- marketing pages outside OCI docs
- community/oracle blog content
- translated mirrors if canonical OCI page is available

Normalization rules:

- Prefer `https://docs.oracle.com/en-us/iaas/...` canonical form.
- Remove URL fragments for deduplication while preserving section text separately.
- Treat query parameters as non-canonical unless required for content rendering.
