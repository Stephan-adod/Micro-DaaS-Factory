# Tasks Playbook (Human-in-the-Loop) · v3.1

## Ziel
Transparente, CI-überwachte To-Do-Liste für wiederkehrende und einmalige Owner-Aufgaben.

## Felder (Kurz)
- `type`: recurring|one_time
- `blocking`: true -> Pipeline darf nicht weiter, bis erledigt
- `status`: open|in_progress|done|skipped
- `due`/`next_due`: Fälligkeit
- `evidence`: Dateien/Links als Nachweis

## Workflow
1. **Aufgabe anlegen/ändern** in `artefacts/tasks_index.json` (UTC/ISO-8601 mit `Z` oder Offset)
2. **Abhängigkeiten** per `depends_on` pflegen; erst abschließen, wenn Vorgänger `done|skipped`
3. **Erledigen** ⇒ `status: done` + (falls `evidence_required`) **Nachweis** in `evidence` verlinken
4. **Recurring** ⇒ `interval_days` ODER `rrule` setzen; bei Abschluss Next-Due planen
5. **CI prüft**:
   - **PR (Soft Mode):** nur informativ, **kein Fail** bei offenen Blockern
   - **main / schedule / workflow_dispatch:** **Fail**, wenn:
     - offenen/überfälligen `blocking` Tasks
     - **unmet dependencies**
     - `evidence_required` aber **keine Evidence**
6. **Tipps**: IDs fortlaufend, `priority` nutzen (P0=kritisch), kleine Einheiten bevorzugen

## CLI – schnelle Bedienung
```bash
# Liste offene Blocker (kompakt)
python artefacts/tasks_cli.py list --open --blocking
# Task abschließen + Report als Evidence verlinken, Next-Due automatisch planen
python artefacts/tasks_cli.py complete T-2025-10-24-01 --evidence docs/health_reports/2025-11-06_health_report.md
# Task 3 Tage snoozen
python artefacts/tasks_cli.py snooze T-2025-10-24-03 --days 3
# Next-Due explizit setzen (Datum/Zeit)
python artefacts/tasks_cli.py plan T-2025-10-24-01 --until 2025-11-20T09:00:00Z
# Deterministisch testen (ohne Writeback)
python artefacts/tasks_cli.py list --open --blocking --now 2025-11-06T09:00:00Z --dry-run
```
**Hinweis:** `rrule` (falls genutzt) wird bevorzugt; sonst `interval_days`.

## Beispiele
- Health Report (recurring, 14d): Nach Erzeugung Report-Datei als `evidence` verlinken
- Lessons Entry (one_time): Markdown unter `docs/lessons/` ablegen
