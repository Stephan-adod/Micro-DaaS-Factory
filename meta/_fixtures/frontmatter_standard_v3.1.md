---
title: Frontmatter Standard v3.1
version: v3.1
status: canonical
owner: stephan-adod
secondary_owner: ai-core-bot
updated: 2025-10-23
review_due: 2026-01-23
retention: permanent
layer: infrastructure
policy_source: meta/AI_First_Handbook.md
policy_version: v3.1
accountability_scope: meta/*
notes: "Standardisierte Frontmatter-Struktur für alle Canonical-Dokumente in AI Native Governance v3.1"
---

# Frontmatter Standard (v3.1)

Dieses Dokument definiert die verbindliche Struktur und Pflichtfelder für alle Canonical-Dateien im AI-Native Governance Framework v3.1.  
Ziel ist vollständige maschinelle Lesbarkeit, eindeutige Ownership und automatische Review-Kontrolle.

---

## 🧱 Canonical Frontmatter Template

```yaml
---
title: "<Dokumentname>"
version: "v3.1"
status: "canonical"           # oder active / draft / archived
phase: "Recovery"             # aus system_version.json
owner: "stephan-adod"
secondary_owner: "ai-core-bot"  # optional
updated: "2025-10-23"
review_due: "2025-12-23"
retention: "permanent"        # oder 12M / 24M
dependencies:
  - "meta/AI_First_Handbook.md"
  - "meta/AI_First_Roadmap.md"
linked_docs:
  - "meta/CORE_INDEX.md"
  - "meta/system_version.json"
accountability_scope: "meta/*"
policy_source: "meta/AI_First_Handbook.md"
policy_version: "v3.1"
governance_phase: "Recovery → Stabilization"
layer: "semantic"              # semantic / operational / infrastructure
review_status: "pending"       # oder ok / overdue
notes: "Baseline Header für AI-Native Governance v3.1"
---
