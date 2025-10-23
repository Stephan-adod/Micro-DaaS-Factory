---
title: AI-First Handbook
version: v3.1
status: canonical
updated: 2025-10-23
owner: stephan-adod
---

# AI-First Handbook (Policy Anchor)

## Zweck
Gemeinsame Sprache, Hard Rules und Verantwortlichkeiten für AI-Native Governance.

## Core Principles (Hard Rules)
1. One PR = One Intent
2. No Future Dates (Frontmatter `updated` ≤ Commit-Zeit)
3. Owner Pflicht (Core-Files: `owner: stephan-adod`)
4. Links müssen existieren (keine toten Verweise im Core)
5. Governance = Infrastructure (Regeln sind maschinell prüfbar)
6. Human in the Loop aktiv (Playbook kann jederzeit stoppen)

## Governance Layer (Definition)
- **Semantic:** Bedeutung & Wert → Handbook, Business Case  
- **Operational:** Umsetzung & Takt → Roadmap, Playbook, Bootstrap  
- **Infrastructure:** Struktur & Validierung → Architecture, Schema, System Version, Health Index

## Canonical Core (v3.1)
- meta/AI_First_Handbook.md  
- meta/AI_First_Roadmap.md  
- meta/AI_First_System_Architecture.md  
- meta/Human_in_the_Loop_Playbook.md  
- meta/governance_recovery_bootstrap_v3.1.md  
- meta/governance_manifest_schema_v3.1.json  
- meta/system_version.json  
- docs/AI_First_Business_Case.md  
- artefacts/governance_health_index.json *(optional, automatisch erzeugt)*

## Change Control
- Policy-Änderungen = PR-Typ **POLICY**, brauchen expliziten Review.
- Tags nur, wenn Gates aus Bootstrap grün sind (Scope/Health/Ecosystem).
