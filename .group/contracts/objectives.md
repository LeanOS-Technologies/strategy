# Contract: objectives

Shared rules: [document-rules.md](document-rules.md).

## Meaning

The outcomes the venture seeks in the current stage: the dominant outcome that deserves concentration now and the smallest set of objectives that gives the needed focus. Each objective is observable, has a target expressing a stated ambition and a horizon with its basis. Bets, focus and every operating group use the outcomes and precedence rules; Evidence owns detailed metric definitions and measurement.

A target is an ambition, never a forecast. An owner-set target, a worker-proposed target and an accepted target are different statuses.

## Identity and scope

One instance per venture, at `venture/{v}/strategy/objectives.md`, covering the horizon it states. Objectives carry IDs `OBJ-n`.

## Required properties

- The objective set carries the owner's ambition for reach, adoption, authority or scale beside the first commercial outcomes that serve it. Each is an observable outcome with a metric or criterion.
- Target status records the decision status; Basis carries the rationale, owner quote where supplied, and source or construction supporting the target and horizon.
- Baseline holds the current value, or `starting` for a new venture; Basis cites the value’s source. A target states the desired outcome.
- The horizon has a basis in the mandate or the outcome mechanism.
- Consequential conflicts between objectives have a precedence or conditional rule.
- A moved date or changed target shows its rationale in the change; a missed target is never hidden.

## Consumer reliance

Consumers may rely on the outcomes, their precedence and the status of each target. They may not rely on a target as a prediction of results, or on a baseline marked `unknown`.

## Acceptance

- Specialist evaluation (set-objectives): each objective serves the mandate and can be observed; the set resolves its material conflicts and gives a useful starting direction; one objective suffices when it supplies the focus.
- Structural (document check): envelope, sections, columns, quoted owner passages, amounts with basis, references.
- The owner accepts it.

## Representation

| Section | Form | Size | Requiredness |
| --- | --- | --- | --- |
| Focus | Statement | 1–2 sentences | required |
| Objectives | Table | One row per necessary objective | required |
| Trade-offs | Table | One row per consequential conflict | required |
| Basis and reconsideration | Prose | Up to 3 short paragraphs | required |

**Focus:** the dominant outcome and why it deserves concentration now.

**Basis and reconsideration:** the link to the mandate, the proposed outcome mechanism, material assumptions, deferred alternatives and the conditions that warrant revision.

### Objectives columns

| Column | Holds | Kind |
| --- | --- | --- |
| `ID` | `OBJ-n` | id OBJ |
| `Outcome` | The desired outcome | reasoning |
| `Metric or observation` | How achievement is observed | reasoning |
| `Baseline` | The current value, or `starting` for a new venture | factual |
| `Target` | The target value or state with its basis | factual |
| `Target status` | owner-set, proposed or accepted | status: owner-set, proposed, accepted |
| `Horizon` | The date or period | factual |
| `Basis` | Source of the baseline; owner quote or proposal rationale for the target and horizon; contribution to ambition | reasoning |

### Trade-offs columns

| Column | Holds | Kind |
| --- | --- | --- |
| `Competing outcomes` | The objectives in conflict | ref objectives |
| `Rule` | Precedence or conditional rule | reasoning |
| `Deferred` | What is deferred and until when | reasoning |
