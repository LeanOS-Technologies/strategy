# Contract: bet-portfolio

Shared rules: [document-rules.md](document-rules.md).

## Meaning

The bets the venture runs to reach its objectives. A bet is an intervention with a proposed outcome mechanism (customer or operating condition → intervention → hypothesised response → objective contribution) that establishes, exploits or improves part of the commercial configuration. The portfolio states the chosen concentration, how bets reinforce or compete, the strongest forgone alternative, each bet's next commitment and the conditions for continuing, expanding, changing or stopping it. Operational tasks serve bets without each becoming a bet.

## Identity and scope

One instance per venture, at `venture/{v}/strategy/bet-portfolio.md`. Bets carry IDs `BET-n`. Bet disposition (proposed, active, held, scaling, closing) is the bet's own state; candidate and current remain the document's approval lifecycle.

## Required properties

- Each bet references at least one current objective and explains its contribution through a mechanism.
- Hypothesis and basis carries each bet's hardest consequential assumption, its source or reasoning and the action that tests it; response estimates retain their premises there. An intended outcome is never restated as a prediction.
- Each bet is compared with a relevant alternative, including continuing current work where that is the real alternative.
- Continue, change and stop conditions have a basis and are never backfilled to make the bet pass.
- Learning value is counted once, as the later decision it can change.
- Bets are jointly compatible; their commercial references agree with the selected targets, advantage, offers and prices.
- No bet holds an amount of money or an estimate of owner hours.

## Consumer reliance

set-focus may rely on the active bets, their next commitments and their dependencies. Product and execution owners may rely on the chosen scope. Nobody may rely on a hypothesised response as observed.

## Acceptance

- Specialist evaluation (prioritize-bets): each selected bet has a plausible objective mechanism, a reason to outrank alternatives and a defined next commitment; uncertainty is represented without fabricated precision or double-counted learning.
- Structural (document check): envelope, sections, columns, quoted owner passages, amounts with basis, references.
- The owner accepts it.

## Representation

| Section | Form | Size | Requiredness |
| --- | --- | --- | --- |
| Portfolio choice | Prose | Up to 3 short paragraphs | required |
| Bets and mechanisms | Table | One row per current or retained bet | required |
| Commitment and comparison | Table | One row per bet | required |
| Evidence and control | Table | One row per bet | required |

**Portfolio choice:** the chosen concentration, how the bets reinforce or compete, and the strongest forgone alternative.

### Bets and mechanisms columns

| Column | Holds | Kind |
| --- | --- | --- |
| `ID` | `BET-n` | id BET |
| `Objective` | The objectives it serves | ref objectives |
| `Scope` | Customer, offer and situation the bet covers | reasoning |
| `Intervention` | What the venture does | reasoning |
| `Expected outcome` | The intended result; Hypothesis and basis carries its premises and supporting reasoning | reasoning |
| `Mechanism` | Why the intervention could produce the outcome | reasoning |
| `Commercial references` | Target, opportunity, advantage, offer or price records it relies on | factual |

### Commitment and comparison columns

| Column | Holds | Kind |
| --- | --- | --- |
| `Bet` | The bet | ref bet-portfolio |
| `Disposition` | proposed, active, held, scaling or closing | status: proposed, active, held, scaling, closing |
| `Next action` | The next useful commitment | reasoning |
| `Dependency` | An actual dependency, or `none` | factual |
| `Rationale` | Why it outranks the alternative | reasoning |
| `Alternative` | The relevant alternative compared | reasoning |

### Evidence and control columns

| Column | Holds | Kind |
| --- | --- | --- |
| `Bet` | The bet | ref bet-portfolio |
| `Hypothesis and basis` | The hardest consequential assumption and what supports it | reasoning |
| `Observation horizon` | When the response can be read | factual |
| `Continue, change or stop` | The conditions and their basis | reasoning |
| `Next commitment` | What the next decision commits to | reasoning |
