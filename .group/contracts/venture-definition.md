# Contract: venture-definition

Shared rules: [document-rules.md](document-rules.md).

## Meaning

The integrated account of the venture: the owner's perspective and ambition, the possibility it pursues, whom it serves, what it provides, how it works and how its activities form a business. Every Strategy document and operating group uses it to develop choices consistent with the owner's view and the venture's scope.

Detailed objectives, prices, entitlements and priorities stay in their owning documents and are referenced here. The definition supplies governing meaning; observed commercial outcomes come from their source records.

## Identity and scope

One instance per venture, at `venture/{v}/strategy/venture.md`. When the venture already holds a document performing this role, that document's path and owner are adopted instead, and this contract governs it. Supplied owner material stays an input snapshot and is never the operative definition.

## Required properties

- The Conclusion states what the venture is and the possibility it pursues; later sections develop its mechanism.
- It states the owner's purpose, convictions and ambition at full strength and develops what they make possible.
- The Perspective and ambition basis line quotes owner material; the Scope note column carries the basis for each scope record. Accepted decisions retain their authority.
- Existing business, accepted direction and proposed or future parts are distinguished; planned capability is never presented as delivered.
- The current focused route is described inside the whole; a narrow target or campaign never replaces the accepted scope.
- Detailed prices, target metrics, entitlement terms and priorities are referenced by their documents, not restated.

## Consumer reliance

Consumers may rely on it as the current account of the venture's purpose, offering structure, operating mechanism, commercial relationship and scope, with the status of each part marked. They may not rely on it for prices, targets, offer terms or evidence of demand.

## Acceptance

- Specialist evaluation (define-venture, then the group coherence check): a reader can explain what the venture does, who uses and buys it, what they receive, how it operates and how its activities form a business without reading the other Strategy documents; the rest of Strategy agrees with it or proposes the corresponding revision.
- Structural (document check): envelope, sections, columns, quoted owner passages, amounts with basis, references.
- The owner accepts it.

## Representation

| Section | Form | Size | Requiredness |
| --- | --- | --- | --- |
| Perspective and ambition | Prose with basis line | Up to 3 short paragraphs | required |
| Purpose and customers | Prose | Up to 2 short paragraphs | required |
| What it provides | Table or prose | Up to 3 short paragraphs, or one row per offering family | required |
| How it works | Prose | Up to 3 short paragraphs | required |
| Commercial relationship | Prose | Up to 2 short paragraphs | required |
| Scope and current form | Table | One row per part | required |

**Perspective and ambition:** the owner's worldview, convictions and ambition as the owner states them, developed into the possibilities they open. A basis line holds the exact supporting quotes.

**Purpose and customers:** the useful change the venture enables, for whom, and the distinction between user, customer and beneficiary where it matters.

**What it provides:** the offering families or domains, what customers receive, how the parts relate, and references to offer or product definitions where they exist.

**How it works:** customer starting situation → venture activity and operating mechanism → delivered result; the roles of AI, people and the customer; the delivery arrangement where material.

**Commercial relationship:** what is sold or exchanged, who pays and for what at the model level, and the relationship to `revenue-model` and `offer-catalogue` without copying their details.

### Scope and current form columns

| Column | Holds | Kind |
| --- | --- | --- |
| `Part` | An offering family, capability, market scope or relationship | reasoning |
| `Status` | available, accepted direction, proposed, future or excluded | status: available, accepted direction, proposed, future, excluded |
| `Scope note` | The distinction that matters, the current focus within the whole, and its basis | reasoning |
