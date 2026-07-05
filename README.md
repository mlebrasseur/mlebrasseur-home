# Home Repository

This repository is the operating record for the house: documents, extracted facts, timelines, money movement, projects, decisions, and recommendations.

## How To Use This Repo

Agent workflow and approval rules are governed by `AGENT.md`.

1. Put new files in `00-inbox/files/`.
2. Tell Codex any new context in chat, such as quotes, payments, decisions, calls, visits, or completed tasks.
3. Codex converts new inputs into source notes, moves processed documents into `01-sources/`, and updates the working markdown files.
4. Use `02-dashboard/` to see the current situation, next actions, timeline, open questions, and risks.

## Main Areas

| Area | Purpose |
|---|---|
| `00-inbox/` | Unprocessed files and temporary chat intake |
| `01-sources/` | Original files, extraction notes, and chat-derived source notes |
| `02-dashboard/` | Current status, timeline, next actions, open questions, and risks |
| `03-property/` | Property facts, rooms, systems, appliances, warranties, and maintenance |
| `04-finance/` | Ledger, budget, mortgage, taxes, insurance, utilities, and renovation costs |
| `05-people/` | Contacts, contractors, service providers |
| `06-projects/` | Active workstreams such as closing, moving, renovations, repairs |
| `07-decisions/` | Decision log, recommendations, rejected options |
| `08-reference/` | Glossary and recurring processes |
| `templates/` | Reusable formats for consistent extraction |

## Agent Rules

See `AGENT.md` for source rules, tone, and approval workflow.
