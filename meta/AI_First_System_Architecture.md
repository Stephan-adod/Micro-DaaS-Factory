---
title: AI-First System Architecture
version: v3.1
status: canonical
updated: 2025-10-23
owner: stephan-adod
---

# Architektur v3.1

## Schichten
L0 Data • L1 Processing • L2 Services • **L3 Micro DaaS Factory** • L4 Governance • L5 Interfaces.

## Micro DaaS Factory (Canonical)
- **Purpose:** wiederverwendbare, leichte Data/Automation-Services
- **Interface:** versioniert, idempotent, deklarativer Contract (I/O)
- **Lifecycle:** ideate → scaffold → validate → publish
- **KPIs:** mROI/Service, ΔMAPE, Uplift (Quelle Business Case)
- **Governance-Hook:** jede Version unterliegt Schema-Validation & Phase-Gate

## Governance Integration
- Schema prüft Struktur, System Version hält Phase/Version, Roadmap nutzt KPIs als Phase-Gates.
