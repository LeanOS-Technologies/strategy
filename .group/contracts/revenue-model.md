# Contract: revenue-model

Shared rules: [document-rules.md](document-rules.md).

## Meaning

How the venture captures part of the value it creates: who uses, benefits, decides and pays; which event causes a purchase, entitlement or renewal and what obligation the payment creates; the charging unit, payment timing, recurrence and expansion; and the revenue and cost drivers that make the exchange viable. design-offers defines purchasable scope on it, set-prices supplies amounts, Finance implements consistent financial treatment, and Engagement understands the purchase path.

Proposed charging mechanics are choices. Predictions of response and estimates of delivery cost need their own basis. Conditional scenarios inform the choice without becoming financial records.

## Identity and scope

One instance per venture, at `venture/{v}/strategy/revenue-model.md`. Exchanges carry IDs `RM-n`.

## Required properties

- Payer, purchase event, entitlement and charging unit are intelligible and compatible for each exchange.
- Each charging mechanic has a buyer and delivery rationale; recurrence is justified by the customer's use, not by the seller's preference for recurring revenue.
- The document role carries the status of the proposed exchange; Value carries each driver’s basis, source or expression. Accepted terms cite their decision and observed costs cite Finance records.
- Assumed sales or support behaviour is never used as proof of profitability.
- The strongest alternative arrangement and the condition that would favour it are stated.

## Consumer reliance

Consumers may rely on the parties, purchase event, entitlement and charging unit of each exchange. Finance may rely on the drivers as Strategy's reasoning, not as financial records.

## Acceptance

- Specialist evaluation (design-revenue-model): the arrangement can attract payment and keep viable economics at plausible adoption levels; known economics, conditional consequences and unknowns are distinguishable.
- Structural (document check): envelope, sections, columns, quoted owner passages, amounts with basis, references.
- The owner accepts it.

## Representation

| Section | Form | Size | Requiredness |
| --- | --- | --- | --- |
| Value-capture choice | Prose | Up to 2 short paragraphs | required |
| Parties and exchange | Table | One row per distinct exchange | required |
| Charging mechanics | Table | One row per charging rule | required |
| Economics and alternatives | Table plus prose | One row per material driver; up to 2 short paragraphs | required |

**Value-capture choice:** why this arrangement fits the buyer, the value and the delivery model.

**Economics and alternatives:** the drivers in the table; in prose, the reference to Finance's definitions and records and the strongest alternative arrangement with its preference condition.

### Parties and exchange columns

| Column | Holds | Kind |
| --- | --- | --- |
| `ID` | `RM-n` | id RM |
| `Target` | The targets | ref target-segments |
| `User` | Who uses | factual |
| `Payer` | Who pays | factual |
| `Entitlement` | What the payment entitles | reasoning |
| `Purchase trigger` | The event that causes the purchase | reasoning |

### Charging mechanics columns

| Column | Holds | Kind |
| --- | --- | --- |
| `Model` | The exchange | ref revenue-model |
| `Charging unit` | The unit charged for (`licence`, `seat-month`, `report`, `engagement`) | factual |
| `Payment timing` | When payment is collected | factual |
| `Recurrence` | Renewal rule, or `none` | factual |
| `Expansion` | Expansion mechanism, or `none` | factual |

### Economics and alternatives columns

| Column | Holds | Kind |
| --- | --- | --- |
| `Driver` | A revenue or cost driver | reasoning |
| `Kind` | revenue or cost | status: revenue, cost |
| `Value` | The value with unit and basis, `unknown`, or `n/a` | factual |
| `Effect on the choice` | How it bears on the arrangement | reasoning |
