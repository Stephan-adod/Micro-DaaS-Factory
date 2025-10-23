---
title: AI Native Governance as Infrastructure Framework
version: v3.1
status: canonical
updated: 2025-10-23
owner: stephan-adod
---

# AI Native Governance as Infrastructure (ANGI)

## 1 · Zweck
Dieses Framework beschreibt, wie **Wirtschaftlichkeit**, **Owner-Lifestyle** und **Infrastruktur-Governance** in einem
AI-nativen System logisch und technisch verbunden werden.

Ziel ist ein System, das:
- **sich selbst überprüft**,  
- **wirtschaftlich messbar** bleibt,  
- und den **Owner entlastet**, anstatt ihn zu überlasten.

---

## 2 · Canonical Core (v3.1)

| Layer | Datei | Zweck |
|--------|--------|--------|
| **Semantic Layer** | `meta/AI_First_Handbook.md` | Policy-Quelle, Begriffe, Hard Rules |
|  | `meta/AI_First_Business_Case.md` | Wirtschaftlichkeit & KPI-Definition |
| **Operational Layer** | `meta/AI_First_Roadmap.md` | Phasen- und Zeitsteuerung |
|  | `meta/Human_in_the_Loop_Playbook.md` | Human Override, Lifestyle-Balance |
|  | `meta/governance_recovery_bootstrap_v3.1.md` | Loops A/B/C + Gates |
| **Infrastructure Layer** | `meta/AI_First_System_Architecture.md` | Technische Struktur + Micro DaaS Factory |
|  | `meta/governance_manifest_schema_v3.1.json` | Maschinen-Contract |
|  | `meta/system_version.json` | Realität / Phase / Pointer |
| *(optional)* | `artefacts/governance_health_index.json` | Telemetrie / Health Feedback |

> Diese neun Dateien bilden das **Framework-Fundament**.
> Keine weiteren Dokumente dürfen „canonical“ genannt werden, ohne Policy-PR.

---

## 3 · Schichtenlogik

| Ebene | Ziel | Verantwortliche Artefakte |
|--------|------|----------------------------|
| **Semantic** | Bedeutung, Sprache, Wert | Handbook · Business Case |
| **Operational** | Umsetzung, Takt, Entscheidung | Roadmap · Playbook · Bootstrap |
| **Infrastructure** | Struktur, Automatisierung, Validierung | Architecture · Schema · System Version · Health Index |

```text
Handbook ─┬─> Roadmap ─┬─> Bootstrap
           │            │
           │            ├─> Playbook (Freeze/Override)
           │            ├─> Business_Case (KPIs)
           │            └─> Architecture (Micro DaaS Factory)
           │
           └─> Schema <─> System_Version <─> Health_Index
4 · Core Principles
One PR = One Intent

No Future Dates – updated darf nie nach dem Commit-Datum liegen.

Owner Pflicht – jedes Core-File: owner: stephan-adod.

Links müssen existieren – keine toten Verweise.

Governance = Infrastructure – Regeln sind maschinell prüfbar.

Human in the Loop aktiv – Playbook darf jede Automatik stoppen.

Value ist Feedback – Business-KPIs steuern Roadmap-Phasen.

5 · Governance Loops
Loop	Zweck	Input	Output	Gate
A – Reality Alignment	Bestand prüfen	Core Docs	meta_inventory_audit / sync_report	Scope Gate
B – Self Observation	Zustand messen	Telemetrie & KPIs	governance_health_index.json	Health Gate
C – Reflection & Recommit	Lernen & Stabilisierung	Lessons	transition_governance.md / Baseline	Ecosystem Gate

6 · Version & Phase Kontrolle
meta/system_version.json = einzige Wahrheit für Version / Phase.

json
Code kopieren
{
  "version": "v3.1",
  "phase": "Recovery",
  "phase_goal": "Stabiler Kern aktiviert",
  "health_score": 0.0-1.0
}
Tags werden nur gesetzt, wenn Scope- & Health-Gate grün sind.

CI-Guardrails:

prüft Owner, Future Dates, Link-Existenz

validiert Manifest ↔ Schema

7 · Micro DaaS Factory (Architektur-Modul)
In meta/AI_First_System_Architecture.md verankert.

Purpose: wiederverwendbare, leichtgewichtige Data- & Automation-Services.
Lifecycle: ideate → scaffold → validate → publish
KPIs: mROI per Service · ΔMAPE · Uplift
Governance Hook: jede Factory-Version durchläuft Schema-Validierung & Phase-Gate.

8 · Owner Lifestyle (Kontrolle durch Playbook)
Playbook-Regeln:

max_ops_per_week ≤ 5

min_recovery_days = 2

freeze_status = active | inactive

availability_window (UTC-Zeitfenster)

Roadmap respektiert diese Werte bei jeder Phase.

9 · Economic Governance Impact
Im Business Case dokumentiert:

KPI	Zielwert	Governance-Nutzung
mROI	> 1.0	Health Gate Kriterium
ΔMAPE	< -0.02	Value Loop Signal
Uplift %	> +0.5 %	Roadmap Phase-Trigger
Docs Freshness (d)	< 14	Audit Check

10 · Quality Assurance
Feld	Kriterium	Ziel
Konsistenz	Alle Canonicals verlinkt & valide	✅
Automatisierbarkeit	Schema & CI prüfen Core Rules	✅
Observability	Health Index liefert Werte > 0.8	✅
Human Balance	Playbook Gates aktiv	✅
Economic Feedback	Business-KPI in Health integriert	✅

11 · Outcome
Das Framework erlaubt:

AI-Native Governance – Regeln = Code, ausführbar & messbar.

Economy Alignment – jeder technische Schritt ist mit Business-KPI verknüpft.

Lifestyle Safety – der Mensch bleibt aktiver Regler, nicht Bottleneck.

Infrastructure Consistency – kein Drift zwischen Docs und Realität.

AI Native Governance as Infrastructure bedeutet:
das System lebt seine eigene Governance – prüfbar, wertbasiert und menschlich steuerbar.

---

## 12 · Canonical Frontmatter (Contract)
Alle Canonicals müssen die v3.1-Frontmatter-Felder führen (siehe meta/_fixtures/frontmatter_standard_v3.1.md). 
Pflichtfelder: title, version, status, phase, owner, updated, review_due, retention, dependencies, linked_docs, layer, policy_source, policy_version.
Nicht erfüllte Felder = PR-Blocker.

## 13 · Change Propagation (Dependency Sync)
- Jede Canonical pflegt `dependencies` (Upstream) und `linked_docs` (Downstream).
- Sobald ein Upstream-Dokument `updated` > eigenes `updated` hat, gilt das Dokument als `stale`.
- Stale-Signal: review_status = pending (bis Sync-PR gemerged).
- PR-Template erfordert “Impacted Docs” Häkchen + Aktualisierung der betroffenen `linked_docs`.

## 14 · Review & Retention Governance
- review_due ≤ +90 Tage ab `updated`. Overdue = PR-Blocker.
- retention: permanent | 12M | 24M | temp. Nach Ablauf → archivieren (nicht löschen).

## 15 · Lessons Integration (Phase 2)
- Eine Sammelstelle: docs/lessons_core_v3.1.md (optional in Phase 2).
- Jede Phase-2-Änderung trägt 3 Learnings ein (What/Why/Impact), max. 5 Zeilen je Punkt.

## 15a · Role Feedback Integration (Phase 2+)
- Jede Phase-2-Änderung erzeugt mindestens ein *Human-in-the-Loop*-Signal (Owner Review, Lessons, Approval).
- Die Zuordnung Owner ⇄ AI ⇄ Codex ⇄ Repo wird im *meta/Human_in_the_Loop_Playbook.md* dokumentiert.
- Lessons werden mit PR-Metadaten verknüpft (Intent, Scope, Impact, Commit-Tag).

## 16 · Definition of Ready (Phase 2)
Vor Start von Phase 2 müssen stehen:
- CORE_INDEX vollständig
- system_version.json zeigt auf alle Canonicals
- Frontmatter v3.1 in allen Canonicals normalisiert
- governance_manifest_schema_v3.1.json akzeptiert Frontmatter-Felder
- PR-Template, CODEOWNERS, Commit-Conventions vorhanden

## 16a · Definition of Roles (Canonical)
- **Owner:** strategisch & semantisch verantwortlich (Intent, Review, Lessons, Gates).
- **AI Partner (ChatGPT):** semantische Übersetzung & Strukturbildung (Scaffold, Policy-Text).
- **Codex App:** technische Implementierung (Writes, PR-Erstellung) unter CI/Schema-Guards.
- **Repo (CI & Guards):** Governance-Validator (Schema, Links, Owner, Dates).

## 17 · Codex Integration & Quality Control Loop (Phase 2+)

**17.1 Automationsrecht**  
Codex App darf Änderungen an Canonicals ausführen, sofern:
1) *One PR = One Intent* dokumentiert ist,  
2) Scope & Impact im PR beschrieben sind,  
3) ein Owner-Review vor Merge erfolgt.

**17.2 Doppelte Qualitätskontrolle**  
1) *Technisch:* CI, Schema-Validator, PR-Guards.  
2) *Semantisch:* Owner Review & Lessons-Eintrag.

**17.3 Feedback-Integration**  
Nach erfolgreichem Merge:
- Aktualisierung von `meta/system_version.json` (Health/Phase, falls relevant),  
- Lessons werden mit PR-Metadaten verknüpft,  
- Health-Score +0.1–0.2, wenn beide Validierungen „grün“.

**17.4 Safety Overrides**  
`freeze_status = active` im Playbook blockiert alle Codex-Writes bis manueller Reset.

**17.5 Auditability**  
Jede Codex-Aktion schreibt einen Governance-Eintrag in `artefacts/governance_health_index.json` (Zeitpunkt, Intent, Datei, Gate-Status).
