# Contract: price-book

Shared rules: [document-rules.md](document-rules.md).

## Meaning

The prices of the offers' exact entitlements and the commercial rules around them: for each price, its unit, currency, payment timing, eligibility and whether it is proposed or accepted; for each rule (discount, anchor, test, exception), its bound, expiry and approval authority; and the economic basis and expected response that informed the choice. Engagement applies the current rules, Finance bills and evaluates economics, Customers interprets entitlements, Governance reviews exposure, and Meaning states accurate price claims.

A recommended price is a commercial proposal, never evidence of willingness to pay. Scenario arithmetic keeps the status of its premises.

## Identity and scope

One instance per venture, at `venture/{v}/strategy/price-book.md`. Prices carry IDs `PRC-n`; rules carry `RUL-n`.

## Required properties

- Every offer in the offer-catalogue has a price row: an amount with currency, `free`, or `unknown` with the named material decision that prevents a recommendation.
- Each price's charging unit matches the charging unit of its offer's revenue-model exchange; amounts and units match the entitlement.
- Accepted prices stay distinct from proposed prices.
- Discounts and exceptions stay within the approved authority and never invalidate the delivery arrangement.
- Basis in Economic basis and response carries the inspected sources, owner quotes and calculation premises; each price row carries its amount basis and Price status. Margin reasoning uses those premises.
- Contribution per transaction is net collected revenue minus the variable costs defined for that transaction; acquisition and longer-term effects need their own compatible cohort and horizon.

## Consumer reliance

Consumers may rely on accepted prices and rules as current terms, on proposed prices as recommendations, and on each rule's bound and authority.

## Acceptance

- Specialist evaluation (set-prices): each requested offer has a reasoned price or free-status recommendation from the available basis; the proposal is useful for a decision while demand or costs remain open.
- Computational (business-model-designer commercial tool; document check): arithmetic in scenarios, discount bounds, unit agreement with the revenue model.
- Structural (document check): envelope, sections, columns, quoted owner passages, amounts with basis, references.
- The owner accepts it.

## Representation

| Section | Form | Size | Requiredness |
| --- | --- | --- | --- |
| Pricing choice | Prose | Up to 2 short paragraphs | required |
| Prices | Table | One row per offer and price rule | required |
| Commercial rules | Table | One row per rule | required |
| Economic basis and response | Table | One row per material scenario or assumption | required |

**Pricing choice:** the current logic, the important trade-off and the strongest alternative.

### Prices columns

| Column | Holds | Kind |
| --- | --- | --- |
| `ID` | `PRC-n` | id PRC |
| `Offer` | The offer priced | ref offer-catalogue |
| `Eligibility` | Who the price applies to | factual |
| `Amount` | Amount with currency and basis, `free`, or `unknown` | factual |
| `Price status` | proposed or accepted | status: proposed, accepted |
| `Charging unit` | The unit, matching the revenue-model exchange | factual |
| `Payment timing` | When it is paid | factual |
| `Applicability` | Scope, period or test bound | factual |

### Commercial rules columns

| Column | Holds | Kind |
| --- | --- | --- |
| `ID` | `RUL-n` | id RUL |
| `Rule` | Discount, anchor, test or exception | reasoning |
| `Eligibility and bound` | Who qualifies and the limit | factual |
| `Expiry or decision` | When it ends or is decided | factual |
| `Authority` | Who approves it | factual |

### Economic basis and response columns

| Column | Holds | Kind |
| --- | --- | --- |
| `Scenario` | The scenario or assumption | reasoning |
| `Relationship` | The net-price and cost relationship, with expression where calculated | factual |
| `Basis` | Demand, value or cost source, reasoning or calculation premises | reasoning |
| `Consequence` | What follows for the price | reasoning |
| `Would change the price` | The observation that would change it | reasoning |
