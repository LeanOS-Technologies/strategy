# Contract: strategy-review

Shared rules: [document-rules.md](document-rules.md).

## Meaning

A diagnosis of what actual results and changed conditions mean for the current direction, and the changes it recommends at the decisions that own the causes. It distinguishes whether an intervention occurred and had enough exposure, which explanations the observations support, and which artifact and owner must change. It is not a competing authority for prices, targets or focus: the affected skills revise their own documents.

## Identity and scope

One instance per review, at `venture/{v}/strategy/strategy-review/{period}.md`, where `{period}` names the review point (`2026-11`, `2026-11-launch`). The current direction lives in the reviewed documents; earlier reviews are history.

## Required properties

- Each disposition compares expected and observed results under their execution and exposure conditions; Observed carries the source record, and Discriminating basis carries the support for diagnosis. Disposition records the recommended action.
- Each material explanatory issue lists competing explanations and the observations that distinguish them; an outcome gap alone never establishes strategic failure.
- Each required change names its artifact, owner, ordering and the next observation or decision condition.
- Where evidence is insufficient, the review names the next observation and a bounded decision point.

## Consumer reliance

set-objectives and the affected skills may rely on the diagnosis and the named changes as recommendations; execution owners receive direction changes only through the accepted revised documents.

## Acceptance

- Specialist evaluation (review-strategy): dispositions follow from observations, execution and remaining opportunity; diagnosis is separated from assumption; the proposed change addresses the supported mechanism at its owner.
- Structural (document check): envelope, sections, columns, quoted owner passages, amounts with basis, references.
- The owner accepts it.

## Representation

| Section | Form | Size | Requiredness |
| --- | --- | --- | --- |
| Strategic consequence | Prose | Up to 2 short paragraphs | required |
| Bet dispositions | Table | One row per reviewed bet | required |
| Diagnosis | Table | One row per material explanatory issue | required |
| Required changes | Table | One row per affected decision | required |

**Strategic consequence:** what the result means for the current direction and concentration.

### Bet dispositions columns

| Column | Holds | Kind |
| --- | --- | --- |
| `Bet` | The reviewed bet | ref bet-portfolio |
| `Objective` | The objective it serves | ref objectives |
| `Expected` | What the bet expected, with its status | factual |
| `Observed` | The observation with its basis, or `unknown` | factual |
| `Execution and exposure` | Whether the intervention ran and long enough to read | reasoning |
| `Disposition` | continue, increase, change, hold or close | status: continue, increase, change, hold, close |
| `Reason` | Why this disposition | reasoning |

### Diagnosis columns

| Column | Holds | Kind |
| --- | --- | --- |
| `Observation` | What was observed, with basis | reasoning |
| `Explanations` | The competing explanations | reasoning |
| `Discriminating basis` | The observation that tells them apart | reasoning |
| `Conclusion` | The supported explanation or the open uncertainty | reasoning |

### Required changes columns

| Column | Holds | Kind |
| --- | --- | --- |
| `Artifact` | The document type to revise | factual |
| `Owner` | The skill that owns the change | factual |
| `Change` | The proposed change | reasoning |
| `Ordering` | Dependency or order among the changes | factual |
| `Next condition` | The observation or decision that follows | reasoning |
