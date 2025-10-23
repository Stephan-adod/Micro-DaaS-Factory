---
title: "Human-in-the-Loop Playbook"
version: "v3.1"
status: "canonical"
phase: "Recovery"
owner: "stephan-adod"
secondary_owner: "ai-core-bot"
updated: "2025-10-23"
review_due: "2025-12-22"
retention: "12M"
dependencies:
  - "meta/AI_First_Handbook.md"
linked_docs:
  - "meta/AI_First_Roadmap.md"
  - "meta/AI_First_System_Architecture.md"
accountability_scope: "meta/*"
policy_source: "meta/AI_First_Handbook.md"
policy_version: "v3.1"
governance_phase: "Recovery → Stabilization"
layer: "operational"
review_status: "pending"
notes: "Lifestyle guards + freeze/override"
---

# HITL Playbook

## Lifestyle Gates
- max_ops_per_week: 5
- min_recovery_days: 2
- availability_window: 09:00–18:00 UTC
- freeze_status: active|inactive

## Overrides
- **Freeze** kann jeden Run stoppen.
- **Manual Sign-off** vor Phase-Wechsel, wenn KPIs knapp sind.

> Roadmap und Bootstrap müssen diese Gates respektieren.
