---
title: AI First Handbook
version: v3.1
status: canonical
phase: enrichment
governance_phase: Recovery → Stabilization
owner: stephan-adod
updated: 2025-10-23
review_due: 2026-01-21
retention: permanent
layer: semantic
policy_source: meta/AI_Native_Governance_Framework_v3.1.md
policy_version: v3.1
dependencies:
  - meta/AI_Native_Governance_Framework_v3.1.md
linked_docs:
  - meta/AI_First_Roadmap.md
  - meta/Human_in_the_Loop_Playbook.md
  - meta/AI_First_Business_Case.md
review_status: done
---

# AI First Handbook (Policy Anchor)

## 1 · Zweck
Das *AI First Handbook* definiert die **semantische Grundlage** des Core-Governance-Frameworks.  
Es legt fest, **was Begriffe bedeuten**, **welche Werte Priorität haben**, und **wie Regeln als maschinell prüfbare Policy** verstanden werden.

> Governance beginnt hier – im Sprachkern des Systems.  
> Bedeutung ist Infrastruktur.

## 2 · Semantic Seeds
| Seed | Beschreibung |
|------|---------------|
| AI-Native Mindset | Entscheidungen werden so gestaltet, dass Maschinen und Menschen gleichberechtigt verständlich agieren können. |
| Governance as Code | Jede Regel wird maschinenlesbar formuliert und versioniert. |
| Owner-Lifestyle Balance | Menschliche Kapazität begrenzt den operativen Scope; das System schützt diese Grenze. |
| Economy Alignment | Wirtschaftliche Kennzahlen spiegeln den Wert und Zustand des Governance-Systems. |
| Self-Observation as Value | Beobachtung und Reflexion sind messbare Systemleistungen. |
| Human Override Principle | Menschliche Eingriffe bleiben oberste Instanz – unabhängig von Automatik. |
| Policy Feedback Loop | Jede Policy erzeugt eine Rückkopplung: Messung → Anpassung → Stabilisierung. |

## 3 · Core Policy Principles
1. **Bedeutung vor Prozess** – Regeln werden erst verstanden, dann automatisiert.  
2. **Automatisierung = Verantwortung** – Code trägt Governance-Pflicht.  
3. **Transparenz = Vertrauen** – Nur nachvollziehbare Abläufe sind gültig.  
4. **Balance ist Pflicht** – Der Owner bleibt Mensch, nicht Operator.  
5. **Feedback ist Wert** – Lernen ist eine Governance-Leistung.

## 4 · Hard Rules (nicht verhandelbar)
- Volles Frontmatter gemäß `frontmatter_standard_v3.1.md`.  
- `owner` = `stephan-adod`.  
- Kein `updated` > Commit-Datum.  
- Jeder PR enthält Intent + Scope + Impact.  
- `review_due` ≤ +90 Tage.

## 5 · Soft Guards (kontextsensitiv)
- Loop-Intensität (A/B/C) darf angepasst werden.  
- Health-Index darf temporär < 0.8 fallen während Lernphasen.  
- Owner kann Playbook-Override setzen.  
- Principles dürfen erweitert, nicht gelöscht werden.

## 6 · Interfaces (Cross Links)
| Ziel | Zweck | Verbindung |
|------|--------|------------|
| Roadmap | Operative Phasensteuerung | Policy → Phase Rules |
| Playbook | Human Override | Lifestyle Gates |
| Business Case | Wirtschaftliche Steuerung | KPI Anchors |
| System Architecture | Technische Umsetzung | Policy → Micro DaaS Spec |

## 7 · Governance Hooks
**Loops:** A · B · C  
**Gates:** Scope → Health → Ecosystem  
**Expected Health Impact:** +0.2 nach Owner Review  
Hook-Level: `semantic · enrichment · v3.1`

## 8 · Feedback Protocol
1. Owner Review → semantische Kohärenz prüfen  
2. Lessons Update → `docs/lessons_core_v3.1.md` ergänzen  
3. Schema Sync → Canonical Fields validieren  
4. System-Version Commit → Health/Phase aktualisieren

## 9 · Lessons (Phase 2)
**What:** Das Handbook wandelt Struktur in Bedeutung um.  
**Why:** Nur klare Sprache ermöglicht messbare Governance.  
**Impact:** Policy wird von Dokument zu Infrastruktur.

## 10 · Meta-Note (Stephan Style)
> Sprache ist der Code der Governance.  
> Wenn Bedeutung maschinenlesbar wird, entsteht Selbststeuerung.  
> Dieses Handbook ist der semantische Quellcode des Core-Systems.
