---
title: "Frontmatter Standard v3.1"
version: "v3.1"
status: "fixture"
phase: "enrichment"
governance_phase: "Recovery → Stabilization"
owner: "stephan-adod"
updated: "2025-10-23"
review_due: "2026-01-21"
retention: "temp"
layer: "meta"
policy_source: "meta/AI_Native_Governance_Framework_v3.1.md"
policy_version: "v3.1"
review_status: "in_progress"
notes: "Non-Canonical; CI-whitelisted"
---

# Frontmatter Standard · v3.1

This fixture defines the canonical YAML frontmatter schema for governance documents in the Micro DaaS Factory stack.

## Required fields

| Key | Type | Description |
| --- | --- | --- |
| `title` | string | Human-readable document title. |
| `version` | string | Semantic version label for the document (e.g., `v3.1`). |
| `status` | enum | One of `draft`, `active`, `canonical`, or `deprecated`. |
| `phase` | string | Lifecycle phase associated with the document (e.g., `Recovery`). |
| `owner` | string | Primary accountable owner (`stephan-adod` for canonical assets). |
| `updated` | date | ISO-8601 date of the last material update. Must not be in the future. |

## Recommended fields

| Key | Type | Description |
| --- | --- | --- |
| `secondary_owner` | string | Secondary steward, typically automation or a backup human. |
| `review_due` | date | Next scheduled review (60 days cadence unless specified otherwise). |
| `retention` | string | Retention window (e.g., `permanent`, `12M`). |
| `dependencies` | array[string] | Canonical files this document depends on. |
| `linked_docs` | array[string] | Additional references that provide supplemental context. |
| `accountability_scope` | string | Glob-style scope of responsibility (e.g., `meta/*`). |
| `policy_source` | string | Canonical policy pointer that authorizes this document. |
| `policy_version` | string | Version tag of the referenced policy source. |
| `governance_phase` | string | Bridge string describing phase transitions (e.g., `Recovery → Stabilization`). |
| `layer` | enum | Governance layer (`semantic`, `operational`, `infrastructure`). |
| `review_status` | enum | Lifecycle review status (`pending`, `ok`, `overdue`). |
| `notes` | string | Short free-text annotation. |

## Validation rules

1. **No future dates** — `updated` and `review_due` must be ≤ the commit date.
2. **Canonical owners** — Canonical documents must list `owner: stephan-adod` and `secondary_owner: ai-core-bot`.
3. **Layer alignment** — Use the layer that matches the document category:
   - `semantic`: policy, definitions, business context.
   - `operational`: roadmaps, playbooks, bootstrap guides.
   - `infrastructure`: architecture, schemas, telemetry.
4. **Dependencies must exist** — Every entry in `dependencies` and `linked_docs` must resolve to a file in the repository.
5. **Policy source loop** — `policy_source` must point to the canonical handbook (`meta/AI_First_Handbook.md`) unless an approved override exists.

## Example frontmatter block

```yaml
---
title: "AI-First Handbook"
version: "v3.1"
status: "canonical"
phase: "Recovery"
owner: "stephan-adod"
secondary_owner: "ai-core-bot"
updated: "2025-10-23"
review_due: "2025-12-22"
retention: "permanent"
dependencies:
  - "meta/CORE_INDEX.md"
linked_docs:
  - "meta/system_version.json"
  - "meta/AI_First_Roadmap.md"
accountability_scope: "meta/*"
policy_source: "meta/AI_First_Handbook.md"
policy_version: "v3.1"
governance_phase: "Recovery → Stabilization"
layer: "semantic"
review_status: "pending"
notes: "Policy anchor for AI-Native Governance v3.1"
---
```

Use this canonical fixture as the authoritative reference when validating or generating frontmatter for governance documents.
