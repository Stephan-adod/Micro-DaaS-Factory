---
title: Human in the Loop Playbook
version: v3.1
status: canonical
phase: enrichment
owner: stephan-adod
updated: 2025-10-23
review_due: 2026-01-21
retention: permanent
layer: semantic-operational
policy_source: meta/AI_Native_Governance_Framework_v3.1.md
policy_version: v3.1
dependencies:
  - meta/AI_First_Handbook.md
  - meta/AI_First_Roadmap.md
  - meta/AI_First_System_Architecture.md
  - meta/AI_First_Business_Case.md
linked_docs:
  - artefacts/governance_health_index.json
  - meta/system_version.json
review_status: in_progress
---

# Human in the Loop Playbook (Semantic ↔ Operational Bridge)

## 1 · Zweck
Das *Human in the Loop Playbook* definiert, wie der Mensch als bewusster Regler des Core-Systems handelt.  
Es legt fest, **wann**, **wie** und **unter welchen Grenzen** menschliche Entscheidungen Vorrang haben  
und wie diese Entscheidungen selbst zu Governance-Signalen werden.

> Governance ist Achtsamkeit in Bewegung.

---

## 2 · Human Control Principles
1. **Owner Awareness ** – Der Mensch ist Bewusstseinsquelle des Systems, nicht dessen Bediener.  
2. **Active Recovery ** – Pausen sind Governance-Aktionen, nicht Abwesenheit.  
3. **Bounded Ops ** – Eingriffe sind zeitlich und kognitiv begrenzt.  
4. **Override with Intent ** – Jeder Override ist dokumentiert und begründet.  
5. **Lifestyle as Metric ** – Lebensqualität ist eine Governance-Metrik.  
6. **Trust by Visibility ** – Transparente Eingriffe erzeugen Vertrauen.  
7. **Accountability by Design ** – Verantwortung ist strukturell eingebettet.

---

## 3 · Capacity Rules & Ops Credits
| Aktion | Credit (h) |
|---------|-----------:|
| PR-Review (canonical) | 1.5 |
| Prompt-Authoring (canonical) | 0.5 |
| Override / Freeze-Entscheid | 0.25 |
| High-Risk-Approval (Compliance) | 1.0 |

**Hard Limits**
- `max_ops_hours_per_week: 10`
- `min_recovery_days: 2`
- `freeze_status: active | inactive`

**Pacing Regel**
- ≥ 80 % Budget → nur sicherheits-/compliance-kritische Entscheidungen  
- ≥ 100 % → `freeze_status: active` bis Wochen-Reset  

**Health Link**
- ≤ 80 % Budget → +0.05 Health Stabilisierung  

> Zeit ist die härteste Governance-Regel – sie schützt Qualität durch Begrenzung.

---

## 4 · Compliance & Ethics (Owner Accountability Layer)

### Hard Rules
- **Rechtsgrundlage & Zweck:** Jede Änderung muss einen Compliance-Grund enthalten.  
- **Approval-Pflicht:** Personenbezogene, sensible oder öffentlich wirksame Inhalte → Owner-Freigabe vor Merge.  
- **Transparenz/Audit:** Jede solche Entscheidung erzeugt Lessons + „Compliance Note“.  
- **Ethik-Check:** Bias / Stakeholder-Impact / Reversibilität bewertet.  
- **SOD:** High-Risk = Author ≠ Approver.  

### 3×3 Checks (Regeltext)
| Kategorie | Prüffragen |
|------------|-------------|
| **Regulatory** | Rechtsgrundlage? Zweckbindung? Datenminimierung? |
| **Ethics** | Bias? Stakeholder-Impact? Reversibilität? |
| **Privacy** | Personenbezug? Sensible Daten? Retention konform? |

### Gate-Zuordnung
| Gate | Prüfung | Trigger |
|------|----------|---------|
| Scope Gate | Checklisten vollständig ? | Owner Approval |
| Health Gate | Compliance Lessons vorhanden ? | +0.05 Health |
| Ecosystem Gate | Ethik-Check bei externer Kommunikation | Publish Permit |

> Verantwortung = sichtbar machen, nicht delegieren.

---

## 5 · Human Feedback Protocol
**Owner Reflection → Lessons Update → Schema Sync → System-Version Commit**

1. Owner reflektiert Workload & Compliance-Entscheidungen.  
2. Lessons + Compliance Notes ergänzen.  
3. Schema / CI prüfen Policy Felder & Freeze-Status.  
4. Codex aktualisiert Health-Index (+0.1 nach Review).

---

## 6 · Impact
Das Playbook macht Menschlichkeit messbar – bewusste Grenzen werden Governance-Daten.

| Loop | Zweck | Output |
|------|--------|---------|
| A | Reality Alignment | Owner Capacity Audit |
| B | Self Observation | Lifestyle Metrics → Health Index |
| C | Reflection & Recommit | Lessons + Compliance Notes |

---

## 7 · Interfaces
| Ziel | Zweck | Verbindung |
|------|--------|------------|
| Roadmap | Phase ↔ Workload Rhythmus | Decision Windows ↔ Ops Budget |
| Architecture | Freeze/Unfreeze Mechanik | Playbook → CI Throttle Hook |
| Business Case | Human Cost ↔ Health | mROI → Owner Capacity |
| Framework | Role & Review Governance | §§15a – 17 |
| Health Index | Lifestyle Metrics | Loop B Feed |

---

## 8 · Governance Hooks
**Loops:** A · B · C  
**Gates:** Scope → Health → Ecosystem  
**Expected Health Impact:** +0.1 nach Owner Review  
Hook-Level: `semantic-operational · enrichment · v3.1`

---

## 9 · Lessons (Phase 2)
**What:** Das Playbook macht Menschlichkeit messbar.  
**Why:** Nur bewusste Grenzen erzeugen nachhaltige Governance.  
**Impact:** Human Balance und Ethik werden Governance-Metriken.

---

## 10 · Meta-Note (Stephan Style)
> Der Mensch ist kein Operator, sondern das Gleichgewicht.  
> Zehn Stunden sind nicht wenig – sie sind die Form von Verantwortung.  
>  
> Ethik ist nicht Korrektur, sondern Ursprung.  
> Dieses Playbook bewahrt, dass Governance nicht nur funktioniert – sie bleibt menschlich.
