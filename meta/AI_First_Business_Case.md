---
title: "AI-First Business Case (Economic Anchor)"
version: "v3.1"
status: "canonical"
phase: "Recovery"
owner: "stephan-adod"
secondary_owner: "ai-core-bot"
updated: "2025-10-23"
review_due: "2026-01-21"
retention: "12M"
dependencies:
  - "meta/AI_First_Handbook.md"
linked_docs:
  - "meta/AI_First_Roadmap.md"
  - "artefacts/governance_health_index.json"
accountability_scope: "meta/*"
policy_source: "meta/AI_First_Handbook.md"
policy_version: "v3.1"
governance_phase: "Recovery → Stabilization"
layer: "semantic"
review_status: "done"
notes: "Refined KPI definition, Health formula, Loop B activation"
---

# AI-First Business Case (Economic Anchor)

## 1 · Zweck
Der Business Case macht Wirtschaftlichkeit zum Regelkreis der Governance:
Jede Entscheidung wird an messbaren Wertströmen überprüft – nicht nur an Prozessen.

## 2 · Scope & Annahmen
- Scope: Core-Services der Micro DaaS Factory (ideate → scaffold → validate → publish)  
- Betrachtung: 12 Monate · Währung = EUR · Zeitbasis = Woche  
- Human Capacity: Playbook-Gates aktiv (max_ops_per_week = 5)  

## 3 · KPI-Definitionen (prüfbar)
| KPI | Formel | Ziel | Quelle |
|-----|---------|------|--------|
| **mROI** | (Value Gain = time_saved×hourly_rate + Δoutput_value) / Service Cost | > 1.0 | Business Services |
| **Uplift %** | (Baseline – Observed)/Baseline × 100 | > +0.5 % | Roadmap |
| **ΔMAPE** | MAPE_alt – MAPE_neu | < –0.02 | Forecasting |
| **Docs Freshness (d)** | today – updated | < 14 | Documentation |
| **Health Score** | siehe Formel unten | > 0.8 | Telemetry |

**Health-Formel:**  
\[
Health = 0.4·mROI + 0.3·Uplift + 0.2·(1 + ΔMAPE) + 0.1·(1 − Freshness/14)
\]

## 4 · Kostenmodell (inkl. Owner-Load)
- Fix: Infra + Tools  
- Variabel: Operator Zeit + Review Zeit  
- Review-Cost = CI-Minutes × rate_per_minute  
- Überschreitung von max 5 Ops/Woche → Freeze laut Playbook  

## 5 · Value-Mapping
| Quelle | Metrik | Gate | Zweck |
|---|---|---|---|
| Business Services | mROI | Health | Go/No-Go pro Service |
| Roadmap Milestones | Uplift | Health | Phase-Trigger |
| Forecasting | ΔMAPE | Health | Qualitätssteuerung |
| Documentation | Freshness | Ecosystem | Lern-Cycle |

## 6 · Phase-Trigger (Recovery → Stabilization)
**Eintritt:** Health ≥ 0.5 und mROI ≥ 1.0 (zwei Reviews innerhalb 14 Tage)  
**Exit:** Manual Sign-off + Health ≥ 0.8 (Gate grün)

## 7 · Telemetrie-Integration
- Jede Factory-Version → `artefacts/governance_health_index.json` (Append)  
- Update-Frequenz = 14 Tage (= Roadmap-Review-Window)  
- Lessons → `docs/lessons_core_v3.1.md` (Phase 2)  
- Commit-Hash wird gespeichert für Audit-Trace.  

## 8 · Risiken & Gegenmaßnahmen
- **Messdrift** (ΔMAPE > 0) → Schema-Lock + Review  
- **Überlast** → Freeze via Playbook  
- **Ökonomische Fehlannahme** → 4-Wochen-Reality-Check  

## 9 · Lessons (Phase 2)
**What:** Wirtschaft ist jetzt maschinell messbar.  
**Why:** Nur messbare Wertflüsse stabilisieren Governance.  
**Impact:** Framework verarbeitet Wert als Signal und kann sich ökonomisch kalibrieren.

## 10 · Outcome
Wenn mROI > 1 und Health > 0.8, trägt sich das System selbst – Governance wird ökonomisch lebendig.

## Meta-Note (Stephan Style)
> Wirtschaft ist Sprache in Zahlen.  
> Wenn mROI zur Grammatik wird, beginnt Governance zu denken.
