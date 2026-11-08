# INVARIANTS: business-model-designer

Each invariant states a required property, its observable violation, its status and verification appropriate to that property. Verification examines actual artifacts, operations or observations. Use the lightest suitable checks that establish the required properties and strengthen the usable result.

Status: **Enforced**, invalid construction or transition is prevented within the stated boundary; **Verified**, the stated check establishes the property under relevant premises; **Assumed**, correctness depends on a named condition not established here. These are verification statuses, not labels required on the worker's prose.

Notation: `D` = the owned document paths and their candidates (`venture/{v}/strategy/{revenue-model,offer-catalogue,price-book}.md` and the same paths under `candidate/`); `T` = scratch scope; `U` = none. `RM`, `OFR`, `PRC`, `RUL` are the exchange, offer, price and rule records; `unit(x)` is the charging unit token of a record; `check` is `python3 workers/strategy/.group/tools/check.py venture/{v}/strategy --owner-material {paths}` on the working view; `commercial` is `python3 workers/strategy/business-model-designer/tools/commercial.py`.

## Domain invariants and laws

### I1 Exchange coherence

**Property.** For every exchange `RM`, the payer, purchase event, entitlement and charging unit describe one purchase: the payer is the party whose money pays for that entitlement, the event triggers that payment, and the unit is what the payment counts. Every offer except a free component references exactly the exchanges it implements, and its entitlement is the exchange's entitlement or a stated part of it.

**Violation signature.** A "licence" whose entitlement implies indefinite updates or hosting (an access period sold as a one-off); a payer who is not the party with the budget; an offer whose entitlement includes something its exchange does not charge for; an offer with no exchange.

**Status.** Verified per request by specialist evaluation; offer → exchange references Enforced by `check` rule REF.

**Verification.**

- Class: specialist evaluation; structural for references.
- Target and method: the candidate `revenue-model` and `offer-catalogue`; for each exchange, read the four roles, the event, the entitlement and the obligation together and test whether one purchase is described; run `check` for REF.
- Acceptance: every exchange describes one coherent purchase; every non-free offer references an exchange; REF reports no error.
- Evidence: the request's work-result (evaluation note and `check` output).
- Correction owner: design-revenue-model for the exchange, design-offers for the entitlement; recheck price-book.

### I2 Price unit equals exchange unit

**Property.** For every price `PRC` referencing offer `o` with exchanges `E(o)`: `unit(PRC) ∈ {unit(e) : e ∈ E(o)}`, unless the price is `free` or its unit is `n/a`. Amount and unit match the entitlement priced.

**Violation signature.** A licence exchange priced per month; a conversion priced per seat; a price per report when the offer grants a perpetual licence.

**Status.** Enforced by `check` rule UNIT on the assembled set; the match of amount to entitlement Verified by specialist evaluation.

**Verification.**

- Class: structural and specialist evaluation.
- Target and method: candidate `price-book`, `offer-catalogue`, `revenue-model`; `check` rule UNIT; read each price against its entitlement.
- Acceptance: no UNIT error; each amount prices the stated entitlement.
- Evidence: `check` output in the work-result.
- Correction owner: set-prices for the price unit, or design-revenue-model when the exchange unit is wrong.

### I3 Every offer priced

**Property.** Every offer in `offer-catalogue` has at least one price row: an amount with currency and label, `free` with its commercial role, or `unknown` naming the material decision that prevents a recommendation. A missing owner price is never such a decision.

**Violation signature.** An offer absent from the price-book; a blank amount; `unknown` justified only by "no price was supplied".

**Status.** Presence Enforced by `check` rule PRICED; the sufficiency of an `unknown` justification Verified by specialist evaluation.

**Verification.**

- Class: structural and specialist evaluation.
- Target and method: `check` rule PRICED; read every `unknown` amount's deciding question.
- Acceptance: no PRICED error; each `unknown` names a decision that genuinely prevents a recommendation.
- Evidence: `check` output and evaluation note in the work-result.
- Correction owner: set-prices.

### I4 Every offer states what it makes possible for its buyer

**Property.** Each offer connects a valuable buyer possibility to its entitlement, customer contribution and path to first value. Packaging and price reasoning preserve that useful outcome.

**Violation signature.** The offer is a list of features or deliverables; the buyer cannot tell what they can accomplish; first value requires an undisclosed contribution.

**Status.** Verified by specialist evaluation per request.

**Verification.**

- Class: specialist evaluation; structural where the group check applies.
- Target and method: Read Offers, Delivery and first value and the pricing rationale as the target buyer; trace possibility → entitlement → customer action → usable result.
- Acceptance: A buyer can explain the outcome, what they receive and how to reach first value; the entitlement can deliver that outcome under its stated conditions.
- Evidence: the candidate, cited owner material, check output and evaluation in the request's work-result.
- Correction owner: design-offers; recheck design-revenue-model and set-prices.

### I5 Deliverable promises

**Property.** Every element an offer promises is available now, or sold on a stated future condition; an offer with status `available` includes only available capability. A roadmap capability never enters an entitlement silently.

**Violation signature.** An available offer whose entitlement includes a planned capability; a delivery claim with a number and no basis; a future offer listed as available.

**Status.** Verified per request by specialist evaluation against `documentation`, `roadmap` and owner material.

**Verification.**

- Class: specialist evaluation.
- Target and method: each row of Offers and Delivery and first value against the capability sources; check quantitative delivery claims for a basis.
- Acceptance: every promised element has an availability basis or a stated future condition.
- Evidence: evaluation note in the work-result.
- Correction owner: design-offers; positioning-strategist rechecks frame expectations.

### I6 Economic statements keep their premises

**Property.** Every amount and percentage carries its basis in the same row or sentence. Contribution per transaction = net collected revenue − variable costs defined for that transaction, computed only from inputs with a stated basis; when an input is unknown the result is `unknown`. A scenario's consequence keeps its premise wherever it is used. No illustrative or unsupported number substantiates a margin, and lifetime value is never inferred from unobserved retention.

**Violation signature.** A margin or contribution figure computed from a cost nobody observed; a scenario result cited without its "if"; an expression that does not hold; mixed currencies added.

**Status.** Labels Enforced by `check` rule NUM-BASIS; arithmetic and units Enforced by `check` rule ARITH and by `commercial` (exit 2 on mixed currencies, `unknown` on unknown inputs; Verified by `tools/test_commercial.py`); premise preservation Verified by specialist evaluation.

**Verification.**

- Class: computational and specialist evaluation.
- Target and method: `check`; `python3 -m unittest discover -s workers/strategy/business-model-designer/tools -p 'test_*.py'`; read each scenario's premise in its consumers.
- Acceptance: no NUM-BASIS or ARITH error; tests pass; no premise is dropped.
- Evidence: command outputs in the work-result.
- Correction owner: the skill that wrote the figure (design-revenue-model or set-prices); `commercial.py` for a calculation defect.

### I7 Constructs have a customer reason

**Property.** Recurrence, tiers, variants, bundles, entry offers, trials, guarantees and anchors each carry a decision-relevant purpose and delivery condition. A subscription requires something recurring for the customer; a tier requires a distinct need, entitlement, purchasing condition or delivery cost; an anchor requires an accurate comparison.

**Violation signature.** A subscription justified by predictable revenue alone; three tiers with cosmetic differences; a guarantee on a delivered service; an anchor to an inflated or unsourced price.

**Status.** Verified per request by specialist evaluation.

**Verification.**

- Class: specialist evaluation.
- Target and method: Charging mechanics, Variants and conditions, Commercial rules; for each construct, find its stated purpose and condition.
- Acceptance: each construct has a customer reason; a simple direct offer is accepted without added constructs.
- Evidence: evaluation note.
- Correction owner: design-revenue-model for recurrence; design-offers for packaging; set-prices for anchors.

### I8 Commercial rules within authority

**Property.** Every discount, test or exception rule states eligibility, a bound, an expiry or decision point and the approving authority; its application stays within the bound declared by the autonomy policy or decision rights, and its net price stays above any floor that keeps delivery viable.

**Violation signature.** A discount with no bound or authority; a bound wider than the declared delegation; a concession whose net price no longer covers the service it buys.

**Status.** Bound arithmetic Enforced by `commercial discount` (exit 1 outside bound or floor); presence of bound and authority Enforced by `check` (REASONING on Rule; factual columns read by evaluator); delegation fit Verified by specialist evaluation against `autonomy-policy`.

**Verification.**

- Class: computational and specialist evaluation.
- Target and method: `python3 workers/strategy/business-model-designer/tools/commercial.py discount --list … --discount … --bound … [--floor …]` for each concession; read each rule against the policy.
- Acceptance: exit 0 for every applied concession; every rule names a bound and authority within the delegation.
- Evidence: command output in the work-result.
- Correction owner: set-prices.

### I9 Compared with the real alternative

**Property.** The revenue model states its strongest alternative arrangement and the condition that would favour it; each offer states why it beats the buyer's actual alternative; each price is reasoned against the buyer's reference on equivalent scope and time.

**Violation signature.** No alternative arrangement; an offer justified by its own features only; a price compared with a competitor's price for a different scope or period.

**Status.** Verified per request by specialist evaluation.

**Verification.**

- Class: specialist evaluation.
- Target and method: Economics and alternatives prose, Offer logic, Pricing choice and the differentiation references.
- Acceptance: each comparison names the alternative and the scope basis.
- Evidence: evaluation note.
- Correction owner: the skill owning the document.

## Contract invariants

### C1 Ownership and write scopes

**Property.** Input snapshots and unrelated state remain unchanged. Writes are confined to `D`, `T` and any declared `U`. An authorised update affects only worker-owned targets. Corrections to another owner's state are prepared for that owner through the declared interface.

**Violation signature.** Input snapshot changed; an unrelated object was modified; a write exceeded its declared scope; another owner's state was silently corrected.

**Status.** Verified per request by comparison of writes with the declared scopes.

**Verification.** Class: structural. Method: record the current revisions and relevant write scope at intake, then compare the actual writes with `D`, `T` and any declared `U`; confirm input snapshots and unrelated state are unchanged. Prepare corrections outside business-model-designer's ownership for the named source owner. Evidence: intake revisions and the work-result's write list; endpoint equality establishes preservation at those endpoints. Correction owner: the operation that wrote out of scope.

### C2 Request distinction and update integrity

**Property.** Creation confirms that its target is absent and does not overwrite another result. An update has an explicit owned target, is based on its current revision and preserves unrelated content. Request inputs, outputs and material changes remain distinguishable. Creation needs no prior instance.

**Violation signature.** A collision overwrites a prior result; an update target lacks authority; its base moved without reconciliation; unrelated content changes; a result cannot be tied to its request; creation is blocked merely because no prior instance exists.

**Status.** Verified through creation or update preflight and final comparison.

**Verification.** Class: structural. Method: creation checks that the target is absent; inspect `candidate/` for another change before writing. For updates, compare the target's current revision with the revision read using `strategy_docs.py rev`, reconcile movement and inspect the candidate for unrelated changes. Tie each output to its request. Evidence: preflight revisions and work-result. Correction owner: business-model-designer's delivery step.

### C3 Canonical sources and derived representations

**Property.** Each object has one declared authority for its concern. Deterministic exports are regenerated from canonical sources. Accepted nondeterministic candidates are retained with relevant inputs and settings. Derived representations preserve their source relationship; exact regeneration is claimed when a supporting mechanism establishes it.

**Violation signature.** An export disagrees with its source; an unrecorded edit changes a derived representation; a generated result is claimed reproducible without a supporting mechanism; competing authorities govern the same concern.

**Status.** Verified for canonical documents and regenerated views; generated prose is retained with its inputs.

**Verification.** Class: structural and computational. Method: treat the owned Markdown as canonical, retain the selected candidate and consumed revisions, regenerate the group view with `workers/strategy/.group/tools/view.py` and compare using `--check`. Inspect source relationships for any generated material; exact replay is asserted only for a checked deterministic operation. Evidence: candidate, Built from, work-result and view check output. Correction owner: business-model-designer's generating operation or canonical source.

### C4 Faithful intent and factual accuracy

**Property.** The owner's purpose, convictions, ambition and decisions retain their meaning and authority through the work. Material factual claims have support appropriate to their consequences. Computations use valid inputs and methods; observations record relevant conditions. Designs, proposals and working assumptions are identifiable where the distinction affects a decision, expectation or action. Convictions, ambitions and useful constructions are expressed directly. Relevant context and references carry detailed support.

**Violation signature.** Owner intent is treated as a factual assertion requiring proof; ambition or an idea loses substance through blanket qualification; a factual claim is fabricated or materially unsupported; a calculation has invalid premises; a proposed result is presented as an observed outcome; a consequential assumption is concealed; repeated labels obscure the usable meaning.

**Status.** Verified by specialist evaluation of governing intent and factual support; computational checks establish their declared subset.

**Verification.** Class: specialist evaluation; computational where applicable. Method: compare the owned result with owner material for purpose, convictions and ambition; inspect consequential factual support, calculations and assumptions through the group's document check and the worker's tools. Evidence: source passages, command output and the request's evaluation in its work-result. Correction owner: the skill that interpreted, constructed or stated the material.

### C5 Coherent execution and dependencies

**Property.** Every PROFILE operation has an actual executor. Composed operations satisfy postcondition-to-precondition, or pass through a declared check or adapter. Specialist decisions use their methods; specified operations use executable capabilities. Required dependencies resolve before dependent execution. Substitutions preserve interface meaning, effects and acceptance. Available resolution, construction and independent work proceed within their inputs and authority.

**Violation signature.** An unexecuted capability is declared available; a generic instruction conceals a missing specialist method; a calculation is inconsistent; an actual dependency is absent; a substitution changes required semantics; an obtainable input is delegated back without proportionate resolution; an independent branch is halted by an unrelated dependency.

**Status.** Verified by executor checks, tool results and specialist review of the selected route.

**Verification.** Class: structural, computational and specialist evaluation. Method: resolve PROFILE executors and required dependencies; run `python3 workers/strategy/.group/tools/check.py venture/{v}/strategy` and the selected worker tool checks. Inspect an obtainable-input case and an independent-work continuation. Confirm that substitutions preserve the consuming interface and that specialist choices use their declared methods. Evidence: command results and the work-result's actual resolution and continuation. Correction owner: the responsible operation, method or dependency.

### C6 Authorised and confirmed effects

**Property.** External or consequential actions stay within declared authority, permission level and bounds. Existing authorisation is applied within its scope. Choices requiring owner authority are prepared concretely while independent work continues. An external effect is reported on confirmation; an unknown outcome is reconciled before retry.

**Violation signature.** An action exceeds authority or a bound; preparation is treated as permission to effect; existing authorisation is repeatedly requested; a consequential owner choice is silently assumed; submission is reported as delivery; an uncertain effect is repeated without reconciliation.

**Status.** Verified per request against local execution and existing authority.

**Verification.** Class: structural. Method: compare actual writes and recorded commands with business-model-designer's local scopes and effect bounds; apply existing authority and prepare reserved owner choices concretely. Inspect any effect confirmation and uncertain-outcome reconciliation before claiming completion or retrying. Evidence: work-result, write list and any command confirmations. Correction owner: the effecting operation or reserved decision.

### C7 Whole, useful and developed result

**Property.** The actual result fulfils the request, meets its contract and required domain properties, and is usable by its intended consumer. Specialist work develops the requested substance from the starting point the responsibility supports. Creative work develops useful possibilities and carries the chosen approach into a substantive result. Verification assesses the actual construction and strengthens it where needed. The answer leads with what was produced, what it enables and the next useful action, with relevant support and remaining dependencies proportionate to their consequences.

**Violation signature.** The result omits requested work; a concept is blocked by an irrelevant demand for operating history; paperwork replaces specialist production; critique removes substance without repairing the construction; a useful possibility is left as a plan despite available means to produce it; structure is used to claim specialist success; a consequential dependency is hidden; a reported result lacks the appropriate check or observation.

**Status.** Verified through the actual checks and specialist consumer-use evaluation below.

**Verification.** Determine acceptance from the required properties below and actual retained evidence, including specialist evaluation where needed. Check usefulness, substantive quality and correctness at the result's intended stage. Correction owner: the decision, method, operation or deliverable requiring strengthening or repair.

| Document type | Required properties | Evidence class / method |
| --- | --- | --- |
| `revenue-model` | I1, I6, I7, I9, C1–C7 | `check`; `commercial` where calculated; specialist coherence and alternative review; Finance and design-offers can interpret the exchange |
| `offer-catalogue` | I1, I4, I5, I7, I9, C1–C7 | `check`; specialist buyer possibility, first-value and delivery review; Engagement can explain and Customers can fulfil the offer |
| `price-book` | I2, I3, I6, I7, I8, I9, C1–C7 | `check`; `commercial discount` and contribution where used; specialist price and premise review; Engagement and Finance can apply the terms |
