# Contract: differentiation

Shared rules: [document-rules.md](document-rules.md).

## Meaning

The customer-relevant advantage the venture has, or could build, over what the target would actually use or do without the offer. Each advantage is a chain: capability and its availability → comparison condition against an actual alternative → customer consequence → the buyer who values it most. Shared attributes can still be purchase requirements; a combination of common capabilities is an advantage when the combination has a meaningful consequence. choose-targets and choose-frame use the same chains; Meaning preserves their evidence status in messages; bets can prioritise building a planned advantage.

## Identity and scope

One instance per venture, at `venture/{v}/strategy/differentiation.md`. Alternatives carry IDs `ALT-n`; advantages carry `ADV-n`. During initial construction the targets referenced can be candidate segments.

## Required properties

- Alternatives include the status quo where the target would keep it, and exclude theoretical competitors irrelevant to the choice.
- Each advantage states its capability's availability (available, planned, unknown) and names the alternative it is compared against.
- A planned capability is never presented as current; its proof or development need is recorded.
- Quantified superiority has a relevant comparison basis; a persuasive benefit chain does not establish measured speed, savings or preference.
- Decision-relevant trade-offs and sacrifices are visible.

## Consumer reliance

Consumers may rely on the leading advantage, its comparison condition and the availability of each capability. They may not rely on a hypothesised customer benefit as demonstrated.

## Acceptance

- Specialist evaluation (define-differentiation): leading advantages matter to a defined buyer and rest on explicit comparative conditions; a unique feature without consequential value does not pass.
- Computational (positioning-strategist chain check): every advantage names a declared alternative and has a support row; planned capability names its proof or development need.
- Structural (document check): envelope, sections, columns, quoted owner passages, amounts with basis, references.

## Representation

| Section | Form | Size | Requiredness |
| --- | --- | --- | --- |
| Leading value | Statement | 1–2 sentences | required |
| Alternative basis | Table | One row per actual alternative | required |
| Advantage chains | Table | One row per material advantage | required |
| Support and trade-offs | Table | One row per advantage | required |

**Leading value:** the most consequential comparative value and its best-fit customer.

### Alternative basis columns

| Column | Holds | Kind |
| --- | --- | --- |
| `ID` | `ALT-n` | id ALT |
| `Alternative` | What the target would use or do instead | reasoning |
| `Target` | The targets or candidate segments that consider it | ref target-segments or segments |
| `Why considered` | Why it is a real alternative for them | reasoning |
| `Basis` | The source, quote, derivation or reason supporting the alternative | reasoning |

### Advantage chains columns

| Column | Holds | Kind |
| --- | --- | --- |
| `ID` | `ADV-n` | id ADV |
| `Capability` | The capability or combination | reasoning |
| `Availability` | available, planned or unknown | status: available, planned, unknown |
| `Against` | The alternatives compared | ref differentiation |
| `Customer consequence` | Operational consequence → customer outcome | reasoning |
| `Target` | Who values it most | ref target-segments or segments |

### Support and trade-offs columns

| Column | Holds | Kind |
| --- | --- | --- |
| `Advantage` | The advantage | ref differentiation |
| `Support` | Evidence or assumption with its basis and testing action | reasoning |
| `Sacrifice` | The relevant trade-off | reasoning |
| `Needed proof or development` | What must be demonstrated or built, or `none` | factual |
