# Makefile — Task convenience wrappers (Owner: stephan-adod)
# Usage:
#   make tasks-list
#   make task-complete ID=T-2025-10-24-01 EVIDENCE=docs/health_reports/2025-11-06_health_report.md
#   make task-snooze ID=T-2025-10-24-03 DAYS=3
# Globals: NOW=ISO8601, DRY_RUN=true|false
NOW        ?=
DRY_RUN    ?= true
PYTHON     ?= python
CLI        := artefacts/tasks_cli.py

.PHONY: help tasks-list task-complete task-snooze

help:
	@echo "targets: tasks-list | task-complete ID=... [EVIDENCE=path] | task-snooze ID=... DAYS=N|UNTIL=ISO"
	@echo "env: NOW='2025-11-06T09:00:00Z' DRY_RUN=true|false"

tasks-list:
	@$(PYTHON) $(CLI) list --open --blocking $(if $(NOW),--now $(NOW)) $(if $(filter true,$(DRY_RUN)),--dry-run,)

task-complete:
	@if [ -z "$(ID)" ]; then echo "[ERR] provide ID=..."; exit 2; fi
	@$(PYTHON) $(CLI) complete "$(ID)" $(if $(EVIDENCE),--evidence "$(EVIDENCE)") $(if $(NOW),--now $(NOW)) $(if $(filter true,$(DRY_RUN)),--dry-run,)

task-snooze:
	@if [ -z "$(ID)" ]; then echo "[ERR] provide ID=..."; exit 2; fi
	@if [ -z "$(DAYS)$(UNTIL)" ]; then echo "[ERR] provide DAYS=N or UNTIL=ISO"; exit 2; fi
	@$(PYTHON) $(CLI) snooze "$(ID)" $(if $(DAYS),--days $(DAYS)) $(if $(UNTIL),--until $(UNTIL)) $(if $(NOW),--now $(NOW)) $(if $(filter true,$(DRY_RUN)),--dry-run,)
