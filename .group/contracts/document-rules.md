# Strategy document rules

The rules every Strategy contract shares, written once. Each type contract in this directory references them and adds its own meaning, properties and representation. The group's must-agree rules are in [AGENTS.md](../../AGENTS.md); the document check implements the machine-checkable part of these rules ([`../tools/check.py`](../tools/check.py)).

## 1. Envelope

Every Strategy document follows this form:

```
# {Title}

Owner: {worker}/{skill} · Updated: {YYYY-MM-DD}
Built from: {type}/{subject}@{revision}, …

## Conclusion
{the current recommendation or decision and its immediate consequence, in one or two sentences}

## {contract sections, in contract order}
```

- *Built from* names every input the content rests on with the revision read, owner material included (`owner/{file}@{revision}`). A document with no inputs yet says `Built from: none`.
- A record another document refers to carries a stable local ID with its type's prefix (`OBJ-1`, `SEG-2`). IDs live in their owning document; there is no separate registry. An ID is never reused for a different record.
- Exact values are table cells; reasoning is short connected prose; relationships are explicit ID references.

## 2. Basis

Put a record's basis in its table's basis or source column. Quote an owner-supplied fact or decision there, cite the inspected source of an external fact, and show the expression of a calculation. The record's status (proposed, accepted or observed) is carried by its status column and the document's role.

Prose states the venture's choices, convictions and ambitions directly. Use a bracketed marker in prose only where the distinction changes the reader's decision. Keep detailed support with the record it supports.

| Value | Basis cell carries | Holds when |
| --- | --- | --- |
| `owner` | `[owner: "exact passage"]` | The passage appears in owner material named in Built from |
| `observed` | `[observed: {type}/{subject}#{record}]` or `[observed: {url}]` | The inspected record supports the fact |
| `derived` | `[derived: {method or inputs}]`, with the calculation's expression | Applying the method to those inputs gives the result |
| `estimate` | `[estimate: {method}; {basis}]` | The factors and consequential assumptions are available for inspection |
| `proposed` | `[proposed]` and the reason for the choice | The construction is offered for decision |
| `accepted` | `[accepted: {decider} {date}]` | The declared decider's acceptance exists |
| `hypothesis` | `[hypothesis]`, the relationship and the action that tests it | The relationship guides work before observation |

An attribution quotes the owner accurately in the record's basis or source cell. An observation cites the Evidence, Product or Finance record or external source it rests on. A Strategy document supplies choices and derivations; observations come from their confirming records.

## 3. Requiredness

Develop each required section from the starting material and resolve missing inputs.

| Field or section | Rule |
| --- | --- |
| Factual cell (`factual` columns) | Holds the value with its basis; holds `unknown` only when the value bears on a decision and remains unavailable after proportionate resolution. The record names its route: research, measurement or owner choice. Use `n/a: {reason}` for an inapplicable field |
| Reasoning cell (`reasoning` columns) | Holds the developed choice, rationale, comparison or consequence the reader needs |
| Status cell (`status` columns) | Holds one of the contract's values |
| Reference cell (`ref` columns) | Holds IDs in the named type, comma-separated, or `none` |
| Required section | Contains its relevant records, or `Omitted: {reason}` when inapplicable |
| Conditional section | Contains the relevant work when its condition holds |

Produce a usable construction while decision-relevant empirical questions follow their named resolution routes. Establish business quantities through their appropriate sources or calculations.

## 4. Quantities

- An amount carries its unit or currency (`49 USD`, `12 inspections`). A percentage carries `%`.
- Every amount or percentage carries its basis in the same row, including a basis or source cell, or in its sentence.
- A calculated value shows its expression: `{expression} = {result}`, for example `49 USD − 2.10 USD = 46.90 USD [derived: price minus processing fee]`. Additive terms share one unit; a currency multiplies only by plain numbers or percentages.
- Targets, prices, estimates, observations and calculated consequences keep their distinct labels (`[proposed]` target, `[estimate: …]` size, `[observed: …]` count, `[derived: …]` result).
- Strategy documents hold no cash position, reserve, budget assignment or estimate of owner hours. `focus-plan` names a needed purchase and the action that needs it, and Finance decides it.

## 5. Contract representation tables

Each type contract declares its sections and, for each table section, its columns. The document check reads these declarations.

- **Sections table:** `Section | Form | Size | Requiredness`, where requiredness is `required` or `conditional: {condition}`.
- **Columns table** under `### {Section} columns`: `Column | Holds | Kind`, where kind is `id {PREFIX}`, `reasoning`, `factual`, `status: {value}, {value}`, or `ref {type}` (`ref {type} or {type}` when either type serves).
