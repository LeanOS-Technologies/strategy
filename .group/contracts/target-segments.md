# Contract: target-segments

Shared rules: [document-rules.md](document-rules.md).

## Meaning

The customers the venture concentrates on now, why they are preferred to the strongest alternative for the objective and horizon, how a prospect is qualified, and which segments follow under which conditions. Product, Meaning, Engagement, Evidence and business-model-designer share this customer scope and do not redefine it.

An initial focus is distinct from the venture's whole market scope: a beachhead is a scoped choice, never a redefinition of the venture.

## Identity and scope

One instance per venture, at `venture/{v}/strategy/target-segments.md`. Targets carry IDs `TGT-n`; qualification rules carry `QR-n`.

## Required properties

- Each target references a declared segment and the advantage that makes it winnable.
- The choice states its horizon and its reason against the strongest alternative, and the assumption that could reverse it.
- Qualification rules use observable indicators and state the treatment when the indicator is unknown; a prospect is never excluded only because a fact is not yet collected.
- Rules rest on a commercial mechanism and are marked `[proposed]` unless supplied by the owner or established by evidence.
- Later segments activate on commercial or capability conditions, not on a date alone.

## Consumer reliance

Consumers may rely on the target scope, the qualification rules and the distinction between rejection and unknown. They may not rely on a rule as empirically predictive unless its basis says so.

## Acceptance

- Specialist evaluation (choose-targets): an intended user can apply the rules to an individual or organisation; the choice fits its scope and horizon and is preferable to a real alternative under stated premises.
- Computational (market-strategist qualify tool): rules give qualified, disqualified or unknown on sample prospects.
- Structural and reference (document check): segment and advantage references resolve.
- The owner accepts it.

## Representation

| Section | Form | Size | Requiredness |
| --- | --- | --- | --- |
| Target choice | Prose | Up to 2 short paragraphs | required |
| Target profile | Table | One row per selected target | required |
| Qualification | Table | One row per rule | required |
| Sequence and sensitivity | Table | One row per deferred or subsequent segment | required |

**Target choice:** the current focus, its horizon and the reason to prefer it.

### Target profile columns

| Column | Holds | Kind |
| --- | --- | --- |
| `ID` | `TGT-n` | id TGT |
| `Segment` | The segment it draws on | ref segments |
| `Buyer and user` | Who buys and who uses | factual |
| `Buying situation` | When and how the purchase happens | reasoning |
| `Need` | The need the venture addresses | reasoning |
| `Advantage` | The advantage records that make it winnable | ref differentiation |

### Qualification columns

| Column | Holds | Kind |
| --- | --- | --- |
| `ID` | `QR-n` | id QR |
| `Target` | The target the rule applies to | ref target-segments |
| `Kind` | qualifier or disqualifier | status: qualifier, disqualifier |
| `Indicator` | The observable indicator | reasoning |
| `When unknown` | What happens when the indicator is not known | reasoning |

### Sequence and sensitivity columns

| Column | Holds | Kind |
| --- | --- | --- |
| `Segment` | The deferred or subsequent segment | ref segments |
| `Disposition` | parallel, next, later or excluded | status: parallel, next, later, excluded |
| `Strongest alternative` | The alternative compared | reasoning |
| `Enabling condition` | The commercial or capability condition that activates it | reasoning |
| `Reversing assumption` | The assumption that could reverse the preference | reasoning |
