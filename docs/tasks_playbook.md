# Tasks Playbook (Human-in-the-Loop) · v3.1

## Ziel
Transparente, CI-überwachte To-Do-Liste für wiederkehrende und einmalige Owner-Aufgaben.

## Prozessübersicht (E2E)
1. **Planen**: Task anlegen (ID, title, phase, owner, blocking, priority, depends_on, due/interval/rrule)
2. **Arbeiten**: Status `open → in_progress` (optional)
3. **Abschließen**: `done` + (falls `evidence_required`) Nachweis in `evidence` verlinken
4. **Wiederauftakten (recurring)**: `interval_days` **oder** `rrule` → `next_due` planen
5. **CI-Kontrolle**: PR = Soft Mode (nur Info), main/schedule/dispatch = **blockierend**
6. **Review**: 14-Tage Rhythmus; Lessons & Health Report referenzieren

## Definition of Done (DoD)
- [ ] `status: done`
- [ ] Abhängigkeiten (`depends_on`) sind `done|skipped`
- [ ] Falls `evidence_required: true` → mindestens **ein** Eintrag in `evidence`
- [ ] Für `recurring`: `next_due` gesetzt (entweder aus `interval_days` oder `rrule` berechnet)

## Rollen / RACI (Phase 3)
- **Owner:** stephan-adod (entscheidet, priorisiert, bestätigt DoD)
- **System (CI):** prüft Blocker/Dependencies/Evidence, erzwingt Policy auf **main**

## Felder (Kurz)
- `type`: recurring|one_time
- `blocking`: true -> Pipeline darf nicht weiter, bis erledigt
- `status`: open|in_progress|done|skipped
- `due`/`next_due`: Fälligkeit
- `evidence`: Dateien/Links als Nachweis
- `interval_days`/`rrule`: Recurrence-Quelle (bei Konflikt hat `rrule` Vorrang)
- `priority`: P0 (kritisch) bis P3 (optional)

## Workflow-Details
1. **Aufgabe anlegen/ändern** in `artefacts/tasks_index.json` (UTC/ISO-8601 mit `Z` oder Offset)
2. **Abhängigkeiten** per `depends_on` pflegen; erst abschließen, wenn Vorgänger `done|skipped`
3. **Erledigen** ⇒ Definition of Done prüfen; Nachweise (`evidence`) ergänzen
4. **Recurring** ⇒ `interval_days` ODER `rrule` setzen; bei Abschluss `next_due` planen
5. **CI prüft** blockierende Tasks, Dependencies und Evidence gemäß Policy (siehe oben)
6. **Tipps**: IDs fortlaufend, kleine Einheiten bevorzugen, `priority` nutzen

## CLI – Arbeitsabläufe
```bash
# Übersicht: aktuell offene Blocker
python artefacts/tasks_cli.py list --open --blocking

# Task abschließen + Evidence und (falls nötig) Next-Due automatisch planen
python artefacts/tasks_cli.py complete T-YYYY-MM-DD-NN --evidence <PATH>

# Snoozen (z.B. bis Datum)
python artefacts/tasks_cli.py snooze T-YYYY-MM-DD-NN --until 2025-11-20T09:00:00Z

# Planen (z.B. +14 Tage)
python artefacts/tasks_cli.py plan T-YYYY-MM-DD-NN --days 14

# Deterministische Smoke-Tests (ohne Writeback)
python artefacts/tasks_cli.py list --open --blocking --now 2025-11-06T09:00:00Z --dry-run
```

## Qualitätssicherung
- **QA-Workflow**: `.github/workflows/tasks_cli_qa.yml` führt Smoke-Tests aus (Dry-Run-Unveränderlichkeit, Plan/Complete Grundpfade).
- **Deterministisch**: Alle Beispiele verwenden `--now` (ISO-8601, UTC bevorzugt).

## Make Quick Actions
Für häufige Aufgaben stehen Make-Targets zur Verfügung (automatisch `DRY_RUN=true`).

```bash
# Offene Blocker anzeigen
make tasks-list NOW=$(date -u +%FT%TZ)

# Task abschließen + Evidence verlinken (automatische Planung aktiv)
make task-complete ID=T-2025-10-24-01 EVIDENCE=docs/health_reports/2025-11-06_health_report.md DRY_RUN=false

# Task um 3 Tage verschieben
make task-snooze ID=T-2025-10-24-03 DAYS=3 DRY_RUN=false
```

### Hinweise
- Standardmäßig läuft alles im **Dry-Run** (sicherer Testmodus).
- `NOW` (ISO-8601) kann für deterministische Zeitstempel angegeben werden.
- Auf Windows bitte Git Bash oder WSL verwenden.
- Diese Targets nutzen exakt die CLI; keine zusätzliche Logik.

## Beispiele
- Health Report (recurring, 14d): Nach Erzeugung Report-Datei als `evidence` verlinken
- Lessons Entry (one_time): Markdown unter `docs/lessons/` ablegen
