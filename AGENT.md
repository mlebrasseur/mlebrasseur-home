# Agent Instructions

This repo is the operating record for the house: documents, facts, projects, money, decisions, and recommendations.

## Default Flow

Stay in blueprint mode unless the user explicitly says `go`.

In blueprint mode:
- Read or inspect files only as needed.
- Do not create, edit, move, rename, or delete files.
- Propose the work clearly.
- List the files that would change.
- Wait for `go`.

When inspecting, check both new inputs and relevant existing markdown files. Keep inspection targeted to the request, likely affected dashboards, indexes, finance files, project files, contacts, and decision records.

After `go`:
- Make the approved changes.
- If the plan materially changes, stop and provide a revised blueprint.
- Verify the result.
- Summarize what changed.

## Source Rule

Nothing important should exist only in a summary file.

Dates, amounts, contacts, obligations, decisions, and recommendations should link back to a source in `01-sources/` whenever practical.

## Tone

Use a calm, practical, factual tone.

Write for future homeowner use:
- concise
- dated where useful
- clear about facts vs assumptions vs recommendations
- direct about risks without exaggeration

Avoid vague summaries, motivational language, unsupported conclusions, and legal-style overcomplication.

## Processing

Files start in `00-inbox/files/`.

Processed evidence goes in:
- `01-sources/documents/` for original files
- `01-sources/extractions/` for source notes created from original files
- `01-sources/chat/` for context from conversation

Working knowledge goes in:
- `02-dashboard/`
- `03-property/`
- `04-finance/`
- `05-people/`
- `06-projects/`
- `07-decisions/`
- `08-reference/`

## Commit Comments

Never create commits.

When asked for a commit comment, check the current changes first, then provide one line only using conventional commit format.
