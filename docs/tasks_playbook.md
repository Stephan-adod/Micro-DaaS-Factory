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
5. **CI prüft** bei PR/main & täglich (Schedule); **failt** bei:
   - offenen/überfälligen `blocking` Tasks
   - **unmet dependencies**
   - `evidence_required` aber **keine Evidence**
6. **Tipps**: IDs fortlaufend, `priority` nutzen (P0=kritisch), kleine Einheiten bevorzugen

## Beispiele
- Health Report (recurring, 14d): Nach Erzeugung Report-Datei als `evidence` verlinken
- Lessons Entry (one_time): Markdown unter `docs/lessons/` ablegen
