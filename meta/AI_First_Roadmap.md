---
title: AI First Roadmap
version: v3.1
status: canonical
phase: enrichment
governance_phase: Recovery → Stabilization
owner: stephan-adod
updated: 2025-10-23
review_due: 2026-01-21
retention: permanent
layer: operational
policy_source: meta/AI_Native_Governance_Framework_v3.1.md
policy_version: v3.1
dependencies:
  - meta/AI_First_Handbook.md
  - meta/AI_First_Business_Case.md
  - meta/governance_recovery_bootstrap_v3.1.md
linked_docs:
  - meta/Human_in_the_Loop_Playbook.md
  - meta/system_version.json
  - artefacts/governance_health_index.json
review_status: done
---

# AI First Roadmap (Operational Anchor)

## 1 · Zweck
Die *AI First Roadmap* übersetzt die Prinzipien des *AI First Handbook* in operatives Handeln.  
Sie legt fest, wie das Core-Governance-System in Phasen arbeitet, wie Loops und Gates die Entwicklung steuern,  
und wie Fortschritt messbar bleibt, ohne Geschwindigkeit mit Wert zu verwechseln.

> Die Roadmap ist kein Zeitplan – sie ist der Puls der Governance.

---

## 2 · Phasenstruktur (v3.1)

| Phase | Ziel | Health-Score | Loop-Fokus | Exit-Condition |
|--------|------|--------------|-------------|----------------|
| **Recovery** | Minimal-Kern aktivieren | 0.0 – 0.3 | A – Reality Alignment | Stabiler Kern, CI grün |
| **Stabilization** | Health > 0.5 & Prozesse im Gleichgewicht | 0.3 – 0.6 | B – Self Observation | Health-Gate ≥ 0.8 |
| **Optimization** | Wirtschaft + Infrastruktur maximieren | 0.6 – 0.9 | A + B | KPI + ΔMAPE-Zielwerte |
| **Reflection** | Lernen & Recommit (Framework Loop C) | ≥ 0.9 | C – Reflection & Recommit | Lessons integriert, neue Phase initiiert |

---

## 3 · Decision & Rhythm Parameters

| Phase | Loop-Cadence | Review-Window | Decision-Window |
|--------|---------------|---------------|----------------|
| Recovery | weekly | 7 d | 1 PR = 1 Intent |
| Stabilization | bi-weekly | 14 d | 2 PRs per Cycle |
| Optimization | monthly | 30 d | auto-triggered |
| Reflection | adaptive | end-phase | manual review |

> Rhythmus = Governance-Atmung.  
> Der Takt folgt Kapazität, nicht Kalender.

---

## 4 · Value Integration Matrix

| Phase | Economic KPI | Trigger / Gate | Zielwert |
|--------|----------------|----------------|-----------|
| Recovery | mROI ≥ 1.0 | Scope Gate | Stabilität aktiv |
| Stabilization | Uplift > +0.5 % | Health Gate | Growth Proof |
| Optimization | ΔMAPE < –0.02 | Health Gate | Predictive Control |
| Reflection | Docs Freshness < 14 d | Ecosystem Gate | Learn Cycle closed |

> Jede Phase ist eine ökonomische Aussage über Governance-Gesundheit.

---

## 5 · Phase → Loop → Gate-Mapping

| Phase | Aktive Loops | Primärer Gate | Lessons Output |
|--------|---------------|----------------|----------------|
| Recovery | A – Reality Alignment | Scope Gate | Initial Setup Lessons |
| Stabilization | B – Self Observation | Health Gate | Operational Stability Learnings |
| Optimization | A + B | Health Gate | Performance Feedback |
| Reflection | C – Reflection & Recommit | Ecosystem Gate | Phase Recap & Next Intent |

---

## 6 · Feedback Protocol

1. **Owner Review** → Phasen-Kohärenz prüfen.  
2. **Lessons Update** → What/Why/Impact in `docs/lessons_core_v3.1.md`.  
3. **Schema Sync** → Canonical Fields validieren.  
4. **System-Version Commit** → Health / Phase aktualisieren.  

> Jede Phase endet mit einem Governance-Signal in `meta/system_version.json`.

---

## 7 · Phase Feedback Hand-Off

Nach Abschluss jeder Phase wird der zugehörige Lessons-Eintrag aus  
`docs/lessons_core_v3.1.md` als *Phase Recap* hier unten angehängt.  
Damit wird die Roadmap zum lernenden Dokument.

```markdown
### Phase Recap Template
- **Phase:** <Name>  
- **What:** …  
- **Why:** …  
- **Impact:** …  
- **Gate Result:** Scope / Health / Ecosystem

```

8 · Governance Hooks

Loops: A · B · C
Gates: Scope → Health → Ecosystem
Expected Health Impact: +0.15 (nach Owner Review)
Hook-Level: operational · enrichment · v3.1

9 · Lessons (Phase 2)

What: Die Roadmap verknüpft Bedeutung mit Handlung.
Why: Nur strukturierte Phasen ermöglichen prüfbare Governance.
Impact: Das Framework wird operativ taktfähig und messbar.

10 · Meta-Note (Stephan Style)

Phasen sind keine Zeiten – sie sind Bewusstseinszustände.
Die Roadmap ist nicht Planung, sondern Rhythmus.
Wenn Bedeutung der Atem ist, ist die Roadmap der Puls der Governance.


---
