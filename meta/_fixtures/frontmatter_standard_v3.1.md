---
title: Canonical Frontmatter Standard
version: v3.1
status: canonical
updated: 2025-10-23
owner: stephan-adod
secondary_owner: ai-core-bot
phase: Recovery
review_due: 2025-12-23
retention: permanent
layer: infrastructure
accountability_scope: meta/_fixtures/*
policy_source: meta/AI_First_Handbook.md
policy_version: v3.1
governance_phase: Recovery → Stabilization
notes: "Referenzdokument – definiert den verbindlichen Frontmatter-Standard für alle Canonicals in v3.1"
---

# Canonical Frontmatter Standard · v3.1

Dieses Dokument definiert die verpflichtenden **Frontmatter-Felder** für alle Canonical-Dokumente  
im Rahmen von *AI Native Governance as Infrastructure v3.1*.

Ziel: Einheitliche, maschinenlesbare und überprüfbare Governance-Metadaten,  
die technische, semantische und organisatorische Synchronität sicherstellen.

---

## 🧭 Strukturübersicht

```yaml
---
title: "<Dokumentname>"
version: "v3.1"
status: "canonical"           # oder active / draft / archived
phase: "Recovery"             # aktuelle Governance-Phase
owner: "stephan-adod"         # Hauptverantwortliche Person
secondary_owner: "ai-core-bot"  # optionale Co-Governance Instanz
updated: "2025-10-23"         # letztes Änderungsdatum
review_due: "2025-12-23"      # nächste Review-Fälligkeit
retention: "permanent"        # oder z.B. "12M", "24M"
dependencies:                 # abhängige Dateien (Upstream)
  - "meta/AI_First_Handbook.md"
  - "meta/AI_First_Roadmap.md"
linked_docs:                  # assoziierte Dokumente (Downstream)
  - "meta/CORE_INDEX.md"
  - "meta/system_version.json"
accountability_scope: "meta/*"
policy_source: "meta/AI_First_Handbook.md"
policy_version: "v3.1"
governance_phase: "Recovery → Stabilization"
layer: "semantic"             # semantic / operational / infrastructure
review_status: "pending"      # oder ok / overdue
notes: "Kurzbeschreibung oder Kontext"
---
