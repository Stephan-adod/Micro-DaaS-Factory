---
title: CORE INDEX (Canonical Pointers)
version: v3.1
status: active
updated: 2025-10-23
owner: stephan-adod
layer: meta
---

# CORE INDEX · v3.1 (Canonical Skeleton)

Dieses Dokument bildet den verbindlichen Einstiegspunkt für alle Canonical-Dateien
im Framework **AI Native Governance as Infrastructure (v3.1)**.  
Es definiert die Kernstruktur, Querverweise und überprüfbare Verantwortlichkeiten.

---

## 🔹 Canonical Set (v3.1)

| Kategorie | Datei | Beschreibung |
|------------|--------|---------------|
| **Semantic Layer** | [AI_First_Handbook.md](meta/AI_First_Handbook.md) | Policy & Core Principles |
| | [AI_First_Business_Case.md](meta/AI_First_Business_Case.md) | Wirtschaftlichkeit & KPI-Anker |
| **Operational Layer** | [AI_First_Roadmap.md](meta/AI_First_Roadmap.md) | Strategie, Phase & Gate-Mapping |
| | [Human_in_the_Loop_Playbook.md](meta/Human_in_the_Loop_Playbook.md) | Owner-Lifestyle & Freeze-Gates |
| | [governance_recovery_bootstrap_v3.1.md](meta/governance_recovery_bootstrap_v3.1.md) | Loops A/B/C und Gate-Definition |
| **Infrastructure Layer** | [AI_First_System_Architecture.md](meta/AI_First_System_Architecture.md) | Technische Struktur & Micro DaaS Factory |
| | [governance_manifest_schema_v3.1.json](meta/governance_manifest_schema_v3.1.json) | Maschinenlesbarer Struktur-Contract |
| | [system_version.json](meta/system_version.json) | Realität, Version & Phase Pointer |
| *(optional)* | [governance_health_index.json](artefacts/governance_health_index.json) | Telemetrie & Health Feedback |

---

## 🔹 Governance Layer-Mapping

| Layer | Zweck | Kontrollmechanismen |
|--------|--------|---------------------|
| **Semantic** | Bedeutung & Werte | Handbook · Business Case |
| **Operational** | Umsetzung & Entscheidung | Roadmap · Playbook · Bootstrap |
| **Infrastructure** | Validierung & Automation | Architecture · Schema · System Version · Health Index |

---

## 🔹 Policy Anchors

- Policy Source: [`meta/AI_First_Handbook.md`](meta/AI_First_Handbook.md)
- Policy Version: `v3.1`
- Owner: `stephan-adod`
- Freeze Enforcement: aktiv über Playbook  
- Governance Phase: *Recovery → Stabilization*

---

## 🔹 Notes

- Nur Dateien aus diesem Index gelten als **Canonical**.
- Jede Änderung am Core erfordert einen **Policy-konformen Pull Request** (`One Intent`).
- Kein File darf außerhalb des Index als „governance relevant“ deklariert werden.
- Validierung erfolgt durch `meta/governance_manifest_schema_v3.1.json`.

---

> **AI-Native Principle:**  
> *Governance is Infrastructure – das System validiert sich selbst.*
