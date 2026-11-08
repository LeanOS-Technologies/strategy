# Contract: offer-catalogue

Shared rules: [document-rules.md](document-rules.md).

## Meaning

The purchasable offers: for each, the buyer's intended outcome, what is included and what the customer supplies, the revenue-model exchange it implements, its delivery status and the path to first value, and any variant, entry mechanism or proposed condition with its purpose. set-prices prices the exact entitlement; Product and Customers fulfil it; Engagement sells within its scope; Governance reviews commitments; Meaning explains the same value.

New names, bundles and terms are proposals until adopted. The catalogue covers the commercial levels the venture source names while distinguishing available, proposed and future offers; a complete future range is not a prerequisite to releasing a first useful offer.

## Identity and scope

One instance per venture, at `venture/{v}/strategy/offer-catalogue.md`. Offers carry IDs `OFR-n`.

## Required properties

- Each offer references its targets, opportunities and revenue-model exchange.
- Each offer has a capability basis or an explicit development dependency; promised value is deliverable now or sold on stated future conditions.
- Included scope, customer contribution, support boundaries and exclusions are explicit.
- Proposed commercial conditions stay distinct from Governance-approved wording; quantitative delivery claims have a basis.
- Each variant, tier, trial, entry offer or guarantee has a decision-relevant purpose and delivery condition.

## Consumer reliance

Consumers may rely on each offer's scope, entitlement and status (available, proposed, future). They may not sell a proposed or future offer as available.

## Acceptance

- Specialist evaluation (design-offers): the buyer can understand the exchange and the path to value; each offer has a credible advantage over the alternative and a justified scope.
- Structural and reference (document check): target, opportunity and revenue-model references resolve.
- The owner accepts it; Governance reviews commitments.

## Representation

| Section | Form | Size | Requiredness |
| --- | --- | --- | --- |
| Offer logic | Prose | Up to 2 short paragraphs | required |
| Offers | Table | One row per purchasable offer | required |
| Delivery and first value | Table | One row per offer | required |
| Variants and conditions | Table | One row per variant or condition | conditional: a variant, entry mechanism, guarantee or proposed condition applies |

**Offer logic:** why the selected packaging fits the buying situations.

### Offers columns

| Column | Holds | Kind |
| --- | --- | --- |
| `ID` | `OFR-n` | id OFR |
| `Offer` | The offer's name | reasoning |
| `Target` | The targets | ref target-segments |
| `Opportunity` | The opportunities it addresses | ref opportunities |
| `Promised outcome` | What the buyer achieves | reasoning |
| `Entitlement` | What is included | reasoning |
| `Revenue model` | The exchange it implements | ref revenue-model |
| `Status` | available, proposed or future | status: available, proposed, future |

### Delivery and first value columns

| Column | Holds | Kind |
| --- | --- | --- |
| `Offer` | The offer | ref offer-catalogue |
| `Delivery status` | What can be delivered now, and when the rest | factual |
| `Prerequisites` | What the customer needs first | factual |
| `First value` | The path to first value | reasoning |
| `Customer contribution` | What the customer supplies | factual |
| `Support and exclusions` | Support boundary and what is outside the purchase | factual |

### Variants and conditions columns

| Column | Holds | Kind |
| --- | --- | --- |
| `Offer` | The offer | ref offer-catalogue |
| `Variant or condition` | The variant, entry mechanism, guarantee or condition | reasoning |
| `Purpose` | Its commercial role | reasoning |
| `Delivery condition` | What delivery it requires | factual |
| `Approval` | Approval status or Governance reference | factual |
