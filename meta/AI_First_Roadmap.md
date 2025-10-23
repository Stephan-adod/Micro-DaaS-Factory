---
title: "AI-First Roadmap"
version: "v3.1"
status: "active"
phase: "Recovery"
owner: "stephan-adod"
secondary_owner: "ai-core-bot"
updated: "2025-10-23"
review_due: "2025-12-22"
retention: "12M"
dependencies:
  - "meta/AI_First_Handbook.md"
  - "meta/AI_First_Business_Case.md"
linked_docs:
  - "meta/system_version.json"
  - "meta/governance_recovery_bootstrap_v3.1.md"
accountability_scope: "meta/*"
policy_source: "meta/AI_First_Handbook.md"
policy_version: "v3.1"
governance_phase: "Recovery → Stabilization"
layer: "operational"
review_status: "pending"
notes: "Phase map + KPI gates"
---

# Roadmap v3.1

## Phase-Mapping
| Phase | Fokus | Gate (muss grün sein) | Deliverable |
|------|-------|------------------------|-------------|
| P0 | Recovery Bootstrap | Scope Gate | meta/governance_recovery_bootstrap_v3.1.md |
| P1 | Stabilization (Health) | Health Gate (score ≥ 0.8) | artefacts/governance_health_index.json |
| P2 | Ecosystem Enablement | Ecosystem Gate | Transition Log + Baseline |

## Business-KPI Bindung (aus docs/AI_First_Business_Case.md)
- mROI ≥ 1.0
- ΔMAPE ≤ −0.02
- Uplift ≥ +0.5 %
- Docs Freshness < 14 Tage

> Roadmap respektiert das Playbook (Freeze/Availability). Ohne grünes Gate kein Phasenwechsel.
