# Contract: opportunities

Shared rules: [document-rules.md](document-rules.md).

## Meaning

Customer progress developed from the owner's direction and the venture's capabilities, including opportunities beyond the supplied list. Attractiveness leads: compare what becomes possible for the target, how the venture can deliver it and its contribution to the ambition and commercial horizon. Product develops requirements, business-model-designer packages value and prioritize-bets chooses commitments.

The evidence column, Basis and status, records the basis and the fastest action that strengthens it. Use evidence to shape development and the next decision; a promising opportunity can justify a demonstration before demand has been observed.

## Identity and scope

One instance per venture, at `venture/{v}/strategy/opportunities.md`. Opportunities carry IDs `OPP-n`.

## Required properties

- Each opportunity references a target and states the situation, desired progress, current alternative and consequence.
- Basis and status carries sources, owner quotes or the reasoning for developed opportunities and the fastest action that strengthens the basis. Reported customer experience cites its record.
- Attractiveness leads the comparison: customer progress, venture fit and commercial contribution determine priority; correlated ratings are evaluated once.
- Each decision-relevant uncertainty names the condition that could change priority and the next action.

## Consumer reliance

Consumers may rely on the priority, its rationale and the evidence status of each opportunity.

## Acceptance

- Specialist evaluation (prioritize-opportunities): priorities distinguish meaningful customer outcomes, use interpretable comparison and keep uncertainty.
- Structural (document check): envelope, sections, columns, quoted owner passages, amounts with basis, references.

## Representation

| Section | Form | Size | Requiredness |
| --- | --- | --- | --- |
| Opportunity focus | Statement | 1–2 sentences | required |
| Opportunity definitions | Table | One row per material opportunity | required |
| Comparison | Table | One row per opportunity | required |
| Uncertainty and action | Table | One row per decision-relevant uncertainty | required |

**Opportunity focus:** what deserves attention first and the commercial reason.

### Opportunity definitions columns

| Column | Holds | Kind |
| --- | --- | --- |
| `ID` | `OPP-n` | id OPP |
| `Target` | The target situation | ref target-segments |
| `Situation` | The situation in which the problem arises | reasoning |
| `Desired progress` | The progress the customer seeks | reasoning |
| `Current alternative` | What they do now | factual |
| `Consequence` | What the problem costs or blocks, with basis | factual |

### Comparison columns

| Column | Holds | Kind |
| --- | --- | --- |
| `Opportunity` | The opportunity | ref opportunities |
| `Demand and payment` | Demand and payment indications with basis | factual |
| `Fit` | Venture fit | reasoning |
| `Switching and delivery` | Switching and delivery implications | factual |
| `Priority` | first, next, later or watch | status: first, next, later, watch |
| `Rationale` | Why this priority | reasoning |

### Uncertainty and action columns

| Column | Holds | Kind |
| --- | --- | --- |
| `Opportunity` | The opportunity | ref opportunities |
| `Basis and status` | Evidence basis, its role and the fastest action that strengthens it | reasoning |
| `Could change priority` | The condition that could change it | reasoning |
| `Next action` | The next action or observation | reasoning |
