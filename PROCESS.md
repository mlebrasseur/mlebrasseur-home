# Processing Process

Use this process whenever new information is added, whether it arrives as a file or as chat context.

Agent workflow and approval rules are governed by `AGENTS.md`.

## File Intake

1. Inspect files in `00-inbox/files/`.
2. Assign the next source ID using `SRC-YYYY-NNN`.
3. Classify each file into one category:
   - `legal`
   - `financing`
   - `inspection`
   - `insurance`
   - `tax`
   - `utilities`
   - `renovation`
   - `moving`
   - `maintenance`
   - `correspondence`
   - `other`
4. Move the original file to `01-sources/documents/<category>/`.
5. Extract relevant facts into a source note in `01-sources/extractions/YYYY/` using `templates/source-note.md`, including the final archived source path.
6. Update `01-sources/source-index.md` with the source ID and final archived/source path under `01-sources/`.
7. Update the relevant dashboard, finance, people, property, project, or decision files.

## Chat Intake

When the user gives context directly in chat:

1. Assign the next source ID using `SRC-YYYY-NNN`.
2. Create a source note in `01-sources/chat/YYYY/`.
3. Name it with `YYYY-MM-DD-category-short-description.md`.
4. Update `01-sources/source-index.md`.
5. Treat it as evidence, the same way a PDF or receipt would be treated.
6. Update all working files affected by that context.

Examples of chat context:

- A renovation quote.
- A payment made.
- A contractor call.
- A visit or inspection result.
- A decision.
- A recommendation request.
- A task completed.

## Naming Convention

Use this format:

```text
YYYY-MM-DD-category-short-description.ext
```

Examples:

```text
2026-07-05-legal-purchase-agreement.pdf
2026-07-05-renovation-bathroom-quote-abc.md
2026-07-05-finance-mortgage-preapproval.pdf
2026-07-05-payment-inspection-deposit.md
```

Use source IDs in this format:

```text
SRC-YYYY-NNN
```

Example:

```text
SRC-2026-001
```

## Update Rules

- In working files, put source IDs in `Source` columns. Add paths only when useful for clarity.
- Add money movement to `04-finance/ledger.md`.
- Add quotes and project costs to the relevant project file and `04-finance/renovation-costs.md` when applicable.
- Add deadlines to `02-dashboard/timeline.md` and `02-dashboard/next-actions.md`.
- Add unresolved facts to `02-dashboard/open-questions.md`.
- Add concerns to `02-dashboard/risks.md`.
- Add people to `05-people/contacts.md`, `05-people/contractors.md`, or `05-people/service-providers.md`.
- Add recommendations to `07-decisions/recommendations.md`.
- Add final choices to `07-decisions/decision-log.md`.

## Source Quality

For each extracted fact, preserve:

- The source path.
- The date received or learned.
- The date processed.
- The confidence level if the source is unclear.
- Any assumptions made during extraction.
