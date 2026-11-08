# INVARIANTS: positioning-strategist

Each invariant states a required property, its observable violation, its status and verification appropriate to that property. Verification examines actual artifacts, operations or observations. Use the lightest suitable checks that establish the required properties and strengthen the usable result.

Status: **Enforced**, invalid construction or transition is prevented within the stated boundary; **Verified**, the stated check establishes the property under relevant premises; **Assumed**, correctness depends on a named condition not established here. These are verification statuses, not labels required on the worker's prose.

Notation: `D` = the owned document paths and their candidates (`venture/{v}/strategy/{differentiation,positioning-decision,category-definition}.md` and the same paths under `candidate/`); `T` = scratch scope; `U` = none. `ALT`, `ADV` = alternative and advantage records of `differentiation`; `avail(a)` ∈ {available, planned, unknown} = the availability of advantage `a`'s capability.

## Domain invariants and laws

### I1 Comparative value against actual alternatives

**Property.** Every advantage names at least one declared alternative (`Against` ⊆ ALT ids), and the alternatives are what the target would actually use or do instead, including keeping the status quo where the target would keep it. The leading advantage has a consequential customer outcome for a defined buyer.

**Violation signature.** An advantage compared with nothing or with an undeclared alternative; a list of competitor products without the status quo when buyers mostly do nothing or improvise; a unique feature leads with no customer consequence; an alternative appears that the target never considers.

**Status.** Enforced for references and support rows; Verified per request for relevance and consequence.

**Verification.**

- Class: structural and computational; specialist evaluation.
- Target and method: `python3 workers/strategy/positioning-strategist/tools/positioning.py check venture/{v}/strategy/candidate/differentiation.md`; `python3 workers/strategy/.group/tools/check.py venture/{v}/strategy` (rule REF). Specialist review asks, for each alternative, why this target would choose it, and for the leading advantage, which customer outcome changes and for whom.
- Acceptance: no error findings; every alternative traceable to an observation, a quoted owner passage or the stated situation; the leading value names its best-fit customer.
- Evidence: command output and the review note in the request's work-result.
- Correction owner: define-differentiation; choose-targets and choose-frame recheck.

### I2 Availability is preserved

**Property.** A capability's availability is `available` only when Product documentation or owner material establishes it; `planned` and `unknown` capabilities name their proof or development need; no frame, category or offer presents a planned capability as current.

**Violation signature.** A roadmap item listed as available; a planned advantage leads a present-tense positioning choice; an available offer promises a planned capability; `none` in the development need of a planned capability.

**Status.** Enforced for the development-need rule; flagged by program and Verified by specialist evaluation for frames and offers.

**Verification.**

- Class: computational; specialist evaluation.
- Target and method: `python3 workers/strategy/positioning-strategist/tools/positioning.py check …/differentiation.md --positioning …/positioning-decision.md --offers …/offer-catalogue.md`; review each `review` finding against the wording of the frame and offer.
- Acceptance: no errors; each review finding resolved as planned-and-stated-as-planned, or corrected.
- Evidence: command output; review dispositions in the work-result.
- Correction owner: the skill that wrote the status; business-model-designer for offers; venture-strategist (define-venture) for the venture-definition.

### I3 Quantified superiority has a comparison basis

**Property.** A quantified claim of advantage (faster, cheaper, fewer) names the alternative, the condition and the observation or estimate it rests on; otherwise the consequence is stated qualitatively and labelled `[hypothesis]`.

**Violation signature.** "Saves 40% of report time" with no comparison basis; a benefit chain presented as a measured result.

**Status.** Enforced for the presence of a basis marker in each amount or percentage's row or sentence (`check.py` rule NUM-BASIS); Verified per request for the adequacy of the basis.

**Verification.**

- Class: structural; specialist evaluation.
- Target and method: `check.py` NUM-BASIS; review each quantified claim's basis against its source.
- Acceptance: each quantified claim has an `[observed: …]` or `[estimate: …]` basis matching its population and condition.
- Evidence: command output; review note.
- Correction owner: define-differentiation.

### I4 Accurate frame within the venture's scope

**Property.** The positioning choice names target, situation, frame and leading advantage; each consequential expectation the frame creates is set against the actual offering, and every mismatch has a resolution; the frame's audience stays inside the accepted venture-definition.

**Violation signature.** A frame that implies features, a buyer, a price level or a purchase the offering does not have; a narrow frame that silently redefines whom the venture serves; a slogan in place of a competitive choice.

**Status.** Verified per request.

**Verification.**

- Class: specialist evaluation.
- Target and method: compare the Frame meaning table with `offer-catalogue`, `differentiation` availability and `venture-definition` scope; ask what a buyer who knows the frame would expect first and whether the offering meets it.
- Acceptance: every expectation either met or named with its resolution; scope preserved or a venture-definition revision proposed.
- Evidence: review note in the work-result.
- Correction owner: choose-frame, with business-model-designer for offer scope.

### I5 Buyer interpretation is designed and tested

**Property.** The frame develops what the buyer should understand and compare, and pairs consequential interpretation assumptions with a demonstration or comprehension test. Observed interpretation cites the relevant source record.

**Violation signature.** The frame has no intended interpretation; a test is named without an audience or task; predicted recognition is reported as observed.

**Status.** Verified by specialist evaluation per request.

**Verification.**

- Class: specialist evaluation; structural where the group check applies.
- Target and method: Inspect the frame's expectations and comparison; prepare a description or demonstration and ask the target reader to explain the value, alternatives and expected capability. Record actual responses when available.
- Acceptance: The frame has a useful intended reading and a concrete test; empirical claims match actual observations.
- Evidence: the candidate, cited owner material, check output and evaluation in the request's work-result.
- Correction owner: choose-frame or design-category; recheck Meaning's interpretation.

### I6 Category membership is a real distinction

**Property.** A category is defined by problem, approach or outcome distinctions that decide representative included and excluded cases, including at least one case outside the venture's own offering that is in and one plausible neighbour that is out; its adoption path names audience, change, demonstration, owner and progress observation. Owner acceptance of a name is recorded as decision status only.

**Violation signature.** Membership equals "has our features"; only the venture's own product is in; no excluded neighbour; adoption claimed from acceptance.

**Status.** Enforced for section and column presence (`check.py`); Verified per request for the distinction.

**Verification.**

- Class: structural; specialist evaluation.
- Target and method: `check.py`; boundary review over the Definition and boundaries table.
- Acceptance: each case decided by a stated condition; a member other than the venture exists or is plausible; at least one neighbour is excluded for a stated reason.
- Evidence: command output; review note.
- Correction owner: design-category.

### I7 The frame choice compares a category option

**Property.** The frame choice develops and compares an existing frame, a narrower frame and a category grounded in the owner's perspective. It assesses the distinction, plausible members and adoption path before choosing.

**Violation signature.** An existing frame is selected without developing the category option; a category is only a new name; the comparison omits membership or adoption.

**Status.** Verified by specialist evaluation per request.

**Verification.**

- Class: specialist evaluation; structural where the group check applies.
- Target and method: Read Choice rationale and Implications; compare the three developed frames against advantage, buyer expectations and the owner's perspective.
- Acceptance: The chosen frame has a reasoned comparison, and a chosen or live category option has a category-definition to develop.
- Evidence: the candidate, cited owner material, check output and evaluation in the request's work-result.
- Correction owner: choose-frame; design-category for membership and adoption.

## Contract invariants

### C1 Ownership and write scopes

**Property.** Input snapshots and unrelated state remain unchanged. Writes are confined to `D`, `T` and any declared `U`. An authorised update affects only worker-owned targets. Corrections to another owner's state are prepared for that owner through the declared interface.

**Violation signature.** Input snapshot changed; an unrelated object was modified; a write exceeded its declared scope; another owner's state was silently corrected.

**Status.** Verified per request by comparison of writes with the declared scopes.

**Verification.** Class: structural. Method: record the current revisions and relevant write scope at intake, then compare the actual writes with `D`, `T` and any declared `U`; confirm input snapshots and unrelated state are unchanged. Prepare corrections outside positioning-strategist's ownership for the named source owner. Evidence: intake revisions and the work-result's write list; endpoint equality establishes preservation at those endpoints. Correction owner: the operation that wrote out of scope.

### C2 Request distinction and update integrity

**Property.** Creation confirms that its target is absent and does not overwrite another result. An update has an explicit owned target, is based on its current revision and preserves unrelated content. Request inputs, outputs and material changes remain distinguishable. Creation needs no prior instance.

**Violation signature.** A collision overwrites a prior result; an update target lacks authority; its base moved without reconciliation; unrelated content changes; a result cannot be tied to its request; creation is blocked merely because no prior instance exists.

**Status.** Verified through creation or update preflight and final comparison.

**Verification.** Class: structural. Method: creation checks that the target is absent; inspect `candidate/` for another change before writing. For updates, compare the target's current revision with the revision read using `strategy_docs.py rev`, reconcile movement and inspect the candidate for unrelated changes. Tie each output to its request. Evidence: preflight revisions and work-result. Correction owner: positioning-strategist's delivery step.

### C3 Canonical sources and derived representations

**Property.** Each object has one declared authority for its concern. Deterministic exports are regenerated from canonical sources. Accepted nondeterministic candidates are retained with relevant inputs and settings. Derived representations preserve their source relationship; exact regeneration is claimed when a supporting mechanism establishes it.

**Violation signature.** An export disagrees with its source; an unrecorded edit changes a derived representation; a generated result is claimed reproducible without a supporting mechanism; competing authorities govern the same concern.

**Status.** Verified for canonical documents and regenerated views; generated prose is retained with its inputs.

**Verification.** Class: structural and computational. Method: treat the owned Markdown as canonical, retain the selected candidate and consumed revisions, regenerate the group view with `workers/strategy/.group/tools/view.py` and compare using `--check`. Inspect source relationships for any generated material; exact replay is asserted only for a checked deterministic operation. Evidence: candidate, Built from, work-result and view check output. Correction owner: positioning-strategist's generating operation or canonical source.

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

**Verification.** Class: structural. Method: compare actual writes and recorded commands with positioning-strategist's local scopes and effect bounds; apply existing authority and prepare reserved owner choices concretely. Inspect any effect confirmation and uncertain-outcome reconciliation before claiming completion or retrying. Evidence: work-result, write list and any command confirmations. Correction owner: the effecting operation or reserved decision.

### C7 Whole, useful and developed result

**Property.** The actual result fulfils the request, meets its contract and required domain properties, and is usable by its intended consumer. Specialist work develops the requested substance from the starting point the responsibility supports. Creative work develops useful possibilities and carries the chosen approach into a substantive result. Verification assesses the actual construction and strengthens it where needed. The answer leads with what was produced, what it enables and the next useful action, with relevant support and remaining dependencies proportionate to their consequences.

**Violation signature.** The result omits requested work; a concept is blocked by an irrelevant demand for operating history; paperwork replaces specialist production; critique removes substance without repairing the construction; a useful possibility is left as a plan despite available means to produce it; structure is used to claim specialist success; a consequential dependency is hidden; a reported result lacks the appropriate check or observation.

**Status.** Verified through the actual checks and specialist consumer-use evaluation below.

**Verification.** Determine acceptance from the required properties below and actual retained evidence, including specialist evaluation where needed. Check usefulness, substantive quality and correctness at the result's intended stage. Correction owner: the decision, method, operation or deliverable requiring strengthening or repair.

| Document type | Required properties | Evidence class / method |
| --- | --- | --- |
| `differentiation` | I1, I2, I3, C1–C7 | `positioning.py check`; `check.py`; specialist alternatives and consequence review; choose-targets and choose-frame can use the advantage |
| `positioning-decision` | I2, I4, I5, I7, C1–C7 | `positioning.py check --positioning --offers`; `check.py`; specialist comparison of all three frame kinds; Meaning can preserve accurate expectations |
| `category-definition` | I5, I6, C1–C7 | `check.py`; specialist boundary and adoption review; Meaning and Engagement can develop language and demonstrations |
