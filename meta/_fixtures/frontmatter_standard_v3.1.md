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
🧩 Feldbeschreibung
Feld	Typ	Bedeutung	Zweck
title	string	Menschlicher Name	Erleichtert Navigation & semantische Suche
version	string	Semantische Version	Grundlage für Tagging & Schema-Validierung
status	string	Dokumentstatus	Steuert Workflow (active, draft, archived)
phase	string	Governance-Phase	Synchronisiert mit system_version.json
owner	string	Verantwortliche Person	Verantwortlichkeit (Accountability)
secondary_owner	string	Co-Reviewer (AI)	Ermöglicht AI-begleitete Validierung
updated	date	Änderungsdatum	Für Drift Detection & Audit Logs
review_due	date	Nächste Review-Fälligkeit	Erzeugt automatische Review-Erinnerung
retention	string	Aufbewahrungsdauer	Basis für Retention-Policy & Archivierung
dependencies	array	Upstream-Dateien	Für Dependency Tracking (Cross-Sync)
linked_docs	array	Downstream-Dokumente	Für Impact- und Sync-Prüfungen
accountability_scope	string	Wirkungsbereich	Z. B. meta/* oder artefacts/*
policy_source	string	Policy-Anker	Governance-Referenz (Handbook)
policy_version	string	Version der Policy	schützt vor Policy-Drift
governance_phase	string	Kontextphase	Human-readable Prozessindikator
layer	string	semantische Schicht	semantic / operational / infrastructure
review_status	string	pending / ok / overdue	Health-Signal für Audit & Dashboard
notes	string	Freitext-Kommentar	Kontext oder rationale Entscheidung

🧠 Best-Practice Regeln
Alle Canonicals enthalten dieses Header-Set.
Fehlende Felder werden mit null oder "n/a" gekennzeichnet.

updated ≤ Commit-Datum.
Keine Future-Dates. Wird CI-seitig validiert.

review_due ≤ +90 Tage.
Jeder Core-Doc muss spätestens nach 3 Monaten überprüft werden.

dependencies & linked_docs
bilden zusammen eine bidirektionale Sync-Map,
auf deren Basis AI-Core-Validator Drift erkennt.

policy_source = Handbook.
Jede Datei verweist auf dieselbe Policy-Quelle.

retention bestimmt, wann Dokumente archiviert werden:

permanent: immer behalten

12M: 1 Jahr nach Erstellung archivieren

24M: 2 Jahre

temp: bis zur nächsten Major-Version

🧮 Beispiel (realistisch)
yaml
Code kopieren
---
title: "AI-First Roadmap"
version: "v3.1"
status: "active"
phase: "Recovery"
owner: "stephan-adod"
secondary_owner: "ai-core-bot"
updated: "2025-10-23"
review_due: "2025-12-23"
retention: "12M"
dependencies:
  - "meta/AI_First_Handbook.md"
linked_docs:
  - "meta/system_version.json"
accountability_scope: "meta/*"
policy_source: "meta/AI_First_Handbook.md"
policy_version: "v3.1"
governance_phase: "Recovery → Stabilization"
layer: "operational"
review_status: "ok"
notes: "Phasensteuerung für AI-Native Governance v3.1"
---
