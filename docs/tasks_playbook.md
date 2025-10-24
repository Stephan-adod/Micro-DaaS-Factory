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
1. **Aufgabe anlegen/ändern** in `artefacts/tasks_index.json`
2. **Erledigen** ⇒ `status: done` setzen, optional `last_run`/`next_due` aktualisieren
3. **CI prüft** bei PR/main und täglich per Schedule
4. **Blocking-Policy**: Offene/überfällige `blocking: true` ⇒ CI failt (main)

## Beispiele
- Health Report (recurring, 14d): Nach Erzeugung Report-Datei als `evidence` verlinken
- Lessons Entry (one_time): Markdown unter `docs/lessons/` ablegen
