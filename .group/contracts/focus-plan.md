# Contract: focus-plan

Shared rules: [document-rules.md](document-rules.md).

## Meaning

What to advance now and why, what can run in parallel, what follows a specific output, and what is deliberately deferred. It gives each actual executor, or an explicitly needed capability, a useful next action, and pairs every blocked action with the step that enables it. Execution groups organise their work from it; execution detail stays with them.

The plan is built on the ready set: the next actions whose prerequisites (actual inputs, access and action-specific authority) are satisfied, ordered by strategic contribution and enabling value. A preference sets priority; only an output another action needs creates a dependency. One blocked action never removes the others from the ready set.

The plan holds no money. When an action needs an actual purchase or financial commitment, the plan names the purchase and the action that needs it; Finance decides it and independent work continues.

## Identity and scope

One instance per venture, at `venture/{v}/strategy/focus-plan.md`. Actions carry IDs `ACT-n`; enabling actions carry `ENB-n`.

## Required properties

- Every action references an active or proposed bet, names its intended output, its execution owner and its timing.
- An executor is an installed capability or named person; an unbuilt group or unavailable tool appears only with an enabling action.
- A `now` or `parallel` action has its prerequisites satisfied; an `after` action names the output or condition it waits for.
- Independent work is never held behind another action's missing prerequisite.
- A needed purchase is attached to the action that needs it, never a global stop condition.
- No amount of money, reserve, budget line or estimate of owner hours or headcount appears. Human involvement appears only as a named decision or contribution an action needs.

## Consumer reliance

Execution groups may rely on the current focus, the action timing and the named prerequisites. Finance may rely on each named purchase being attached to a specific action. review-strategy may rely on the change conditions.

## Acceptance

- Specialist evaluation (set-focus): the plan advances the objective through the bets, preserves real dependencies and explains priority.
- Computational (venture-strategist focus tool): the ready set matches the timing column; no dependency cycle.
- Structural (document check): columns, statuses, bet references; no money or hour estimate.
- The owner accepts it.

## Representation

| Section | Form | Size | Requiredness |
| --- | --- | --- | --- |
| Current focus | Statement | 1–2 sentences | required |
| Work sequence | Table | One row per material next action | required |
| Enabling actions | Table | One row per missing prerequisite | conditional: a prerequisite needs work |
| Change conditions | List | One line per consequential condition | required |

**Current focus:** what to advance now and why it has priority.

**Change conditions:** the observation or completed dependency that would change concentration or sequence.

### Work sequence columns

| Column | Holds | Kind |
| --- | --- | --- |
| `ID` | `ACT-n` | id ACT |
| `Bet` | The bet the action serves | ref bet-portfolio |
| `Action and output` | The action and the output it produces | reasoning |
| `Executor` | The installed capability or named person that performs it | factual |
| `Timing` | now, parallel, after or deferred | status: now, parallel, after, deferred |
| `Prerequisite` | `none`, action or enabling IDs, or the named condition | factual |

### Enabling actions columns

| Column | Holds | Kind |
| --- | --- | --- |
| `ID` | `ENB-n` | id ENB |
| `Action` | The blocked actions | ref focus-plan |
| `Missing condition` | The concrete missing prerequisite | reasoning |
| `Enabling step or alternative` | What enables it, or the available alternative route | reasoning |
| `Owner` | Who performs or decides the enabling step | factual |
| `Continuing work` | The independent work that proceeds meanwhile | reasoning |
