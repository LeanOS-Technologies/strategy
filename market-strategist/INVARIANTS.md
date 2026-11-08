# INVARIANTS: market-strategist

Each invariant states a required property, its observable violation, its status and verification appropriate to that property. Verification examines actual artifacts, operations or observations. Use the lightest suitable checks that establish the required properties and strengthen the usable result.

Status: **Enforced**, invalid construction or transition is prevented within the stated boundary; **Verified**, the stated check establishes the property under relevant premises; **Assumed**, correctness depends on a named condition not established here. These are verification statuses, not labels required on the worker's prose.

Notation: `D` = the owned document paths and their candidates (`venture/{v}/strategy/{segments,target-segments,opportunities}.md` and the same paths under `candidate/`); `T` = scratch scope; `U` = none. `SEG`, `TGT`, `QR`, `OPP` are the record sets of the owned documents; `check` = `python3 workers/strategy/.group/tools/check.py venture/{v}/strategy --owner-material {paths}`; `market` = `python3 workers/strategy/market-strategist/tools/market.py`.

## Domain invariants and laws

### I1 Segment boundaries change decisions

**Property.** For every pair of neighbouring segments in `SEG`, at least one of trigger, buyer, alternative, delivery or value differs in a way that changes a targeting, offer, channel or product decision; that difference is stated.

**Violation signature.** Two segments that would receive the same target, offer and channel decision; segments separated only by demographic or firmographic labels; a segment named after the product's feature.

**Status.** Verified per request.

**Verification.**

- Class: specialist evaluation.
- Target and method: the candidate `segments`; for each neighbouring pair, name the downstream decision the distinction changes.
- Acceptance: every pair has a named decision; criterion fixed in segment-market step 6.
- Evidence: the evaluation recorded in the request's work-result.
- Correction owner: segment-market (merge or restate); choose-targets and prioritize-opportunities recheck references.

### I2 Segments are recognisable

**Property.** Every segment has recognition criteria that Evidence can test, Engagement can use to reach a member and Product can turn into requirements; proposed criteria are labelled `[proposed]`.

**Violation signature.** Criteria only the venture can apply ("values our approach"); criteria presented as established without an origin.

**Status.** Verified per request.

**Verification.**

- Class: specialist evaluation; structural for labels.
- Target and method: `Recognition criteria` cells of `segments`; the three-consumer usability test of segment-market step 5; `check` (NUM-BASIS, ATTRIB rules).
- Acceptance: each criterion names an observable or askable indicator.
- Evidence: work-result evaluation; `check` output.
- Correction owner: segment-market.

### I3 Estimates rest on grounded factors

**Property.** A size or range in `segments` is the product of factors that each carry a value and a basis, with compatible units; otherwise the cell is `unknown` or `n/a: {reason}`.

**Violation signature.** A population, market size or rate with no factors or basis; an estimate whose missing factor was replaced by a guess; a size presented as observed.

**Status.** Enforced for estimates computed with `market estimate` (it returns `unknown` and names the missing factor when any value or basis is absent); Verified by specialist evaluation that every size cell came from that tool or is `unknown`/`n/a`.

**Verification.**

- Class: computational; specialist evaluation.
- Target and method: `market estimate FACTORS.csv` for each estimate; comparison of the `Size` cells with its output; tests `python3 -m unittest discover -s workers/strategy/market-strategist/tools -p 'test_*.py'` cover the unknown paths.
- Acceptance: every numeric size equals a tool result with the factors recorded; tests pass.
- Evidence: tool output and test run in the request's work-result.
- Correction owner: segment-market; dependent target comparisons rechecked.

### I4 Opportunities include ones developed beyond the owner's list

**Property.** The market work develops additional customer situations and progress from the owner's direction and venture capabilities, and compares their value with supplied opportunities.

**Violation signature.** The result repeats the owner's list; a valuable application is dismissed solely because no customer has requested it; added segments change no decision.

**Status.** Verified by specialist evaluation per request.

**Verification.**

- Class: specialist evaluation; structural where the group check applies.
- Target and method: Trace a developed opportunity to the direction and capability that enable it; compare who benefits, what becomes possible and the action that establishes its usefulness.
- Acceptance: The result contains substantive additional possibilities with a usable development or testing action.
- Evidence: the candidate, cited owner material, check output and evaluation in the request's work-result.
- Correction owner: segment-market or prioritize-opportunities; recheck targets and offer implications.

### I5 Target choice beats the strongest alternative within the horizon

**Property.** Every target in `TGT` references a declared segment, names its binding condition, fits the objective's horizon or names its enabling work, and is compared with the strongest real alternative segment with the reversing assumption stated.

**Violation signature.** A target chosen on pain or size with purchase timing ignored; a rejected alternative nobody would choose; no reversing assumption; a segment whose buying cycle exceeds the horizon presented as contributing within it.

**Status.** Enforced for segment references by `check` (REF); Verified by specialist evaluation for the comparison.

**Verification.**

- Class: structural; specialist evaluation; computational when scores are used.
- Target and method: `check`; the choose-targets step 7 table; `market score … --scale … --weights …` when scored, with its reversal condition reported.
- Acceptance: each target has binding condition, horizon fit, strongest alternative and reversing assumption.
- Evidence: work-result evaluation; tool outputs.
- Correction owner: choose-targets; opportunities, offers and bets referencing the target rechecked.

### I6 Focus stays inside the venture's scope

**Property.** `target-segments` narrows current focus without removing an accepted customer group or product line from the venture-definition; a scope change appears only as a proposal routed to define-venture.

**Violation signature.** The target choice reads as what the venture is; an accepted segment is excluded without a proposed venture-definition revision.

**Status.** Verified per request.

**Verification.**

- Class: specialist evaluation.
- Target and method: comparison of `target-segments` with `venture-definition` Scope and current form.
- Acceptance: every accepted part of the scope is still present or covered by an explicit proposed revision.
- Evidence: work-result evaluation.
- Correction owner: choose-targets; define-venture for a proposed scope change.

### I7 Qualification distinguishes rejection from unknown

**Property.** Every rule in `QR` has a kind, an observable indicator and a treatment when unknown; applying the rules to a prospect yields disqualified only when a qualifier is observed false or a disqualifier observed true, and unknown when any needed indicator is missing.

**Violation signature.** A rule without "When unknown"; a prospect excluded because a fact was not collected; a rule claimed predictive without observed outcomes.

**Status.** Enforced by `market qualify` (its decision function); Verified that each rule has a treatment by `check` (REASONING on `When unknown`) and specialist evaluation of the indicators.

**Verification.**

- Class: computational; structural; specialist evaluation.
- Target and method: `market qualify target-segments.md PROSPECT.json --target TGT-n` on sample prospects including one with missing indicators; unit tests `QualifyTest`.
- Acceptance: the missing-indicator prospect yields unknown; tests pass.
- Evidence: tool output and test run.
- Correction owner: choose-targets.

### I8 Opportunities are customer progress, developed from the venture's direction and capabilities, each with its basis and the action that strengthens it

**Property.** Each opportunity names a target, situation and valuable customer progress. Attractiveness leads comparison; Basis and status records support and the fastest action that strengthens it.

**Violation signature.** A feature replaces progress; evidence quantity determines priority without value comparison; a promising opportunity has no development action; correlated benefits are counted twice.

**Status.** Verified by specialist evaluation per request.

**Verification.**

- Class: specialist evaluation; structural where the group check applies.
- Target and method: Run the group reference check; inspect Opportunity definitions, Comparison and Uncertainty and action against owner direction and capability.
- Acceptance: Each priority has a customer and venture rationale, a basis and an executable action that improves the decision.
- Evidence: the candidate, cited owner material, check output and evaluation in the request's work-result.
- Correction owner: prioritize-opportunities; recheck design-offers and Product implications.

## Contract invariants

### C1 Ownership and write scopes

**Property.** Input snapshots and unrelated state remain unchanged. Writes are confined to `D`, `T` and any declared `U`. An authorised update affects only worker-owned targets. Corrections to another owner's state are prepared for that owner through the declared interface.

**Violation signature.** Input snapshot changed; an unrelated object was modified; a write exceeded its declared scope; another owner's state was silently corrected.

**Status.** Verified per request by comparison of writes with the declared scopes.

**Verification.** Class: structural. Method: record the current revisions and relevant write scope at intake, then compare the actual writes with `D`, `T` and any declared `U`; confirm input snapshots and unrelated state are unchanged. Prepare corrections outside market-strategist's ownership for the named source owner. Evidence: intake revisions and the work-result's write list; endpoint equality establishes preservation at those endpoints. Correction owner: the operation that wrote out of scope.

### C2 Request distinction and update integrity

**Property.** Creation confirms that its target is absent and does not overwrite another result. An update has an explicit owned target, is based on its current revision and preserves unrelated content. Request inputs, outputs and material changes remain distinguishable. Creation needs no prior instance.

**Violation signature.** A collision overwrites a prior result; an update target lacks authority; its base moved without reconciliation; unrelated content changes; a result cannot be tied to its request; creation is blocked merely because no prior instance exists.

**Status.** Verified through creation or update preflight and final comparison.

**Verification.** Class: structural. Method: creation checks that the target is absent; inspect `candidate/` for another change before writing. For updates, compare the target's current revision with the revision read using `strategy_docs.py rev`, reconcile movement and inspect the candidate for unrelated changes. Tie each output to its request. Evidence: preflight revisions and work-result. Correction owner: market-strategist's delivery step.

### C3 Canonical sources and derived representations

**Property.** Each object has one declared authority for its concern. Deterministic exports are regenerated from canonical sources. Accepted nondeterministic candidates are retained with relevant inputs and settings. Derived representations preserve their source relationship; exact regeneration is claimed when a supporting mechanism establishes it.

**Violation signature.** An export disagrees with its source; an unrecorded edit changes a derived representation; a generated result is claimed reproducible without a supporting mechanism; competing authorities govern the same concern.

**Status.** Verified for canonical documents and regenerated views; generated prose is retained with its inputs.

**Verification.** Class: structural and computational. Method: treat the owned Markdown as canonical, retain the selected candidate and consumed revisions, regenerate the group view with `workers/strategy/.group/tools/view.py` and compare using `--check`. Inspect source relationships for any generated material; exact replay is asserted only for a checked deterministic operation. Evidence: candidate, Built from, work-result and view check output. Correction owner: market-strategist's generating operation or canonical source.

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

**Verification.** Class: structural. Method: compare actual writes and recorded commands with market-strategist's local scopes and effect bounds; apply existing authority and prepare reserved owner choices concretely. Inspect any effect confirmation and uncertain-outcome reconciliation before claiming completion or retrying. Evidence: work-result, write list and any command confirmations. Correction owner: the effecting operation or reserved decision.

### C7 Whole, useful and developed result

**Property.** The actual result fulfils the request, meets its contract and required domain properties, and is usable by its intended consumer. Specialist work develops the requested substance from the starting point the responsibility supports. Creative work develops useful possibilities and carries the chosen approach into a substantive result. Verification assesses the actual construction and strengthens it where needed. The answer leads with what was produced, what it enables and the next useful action, with relevant support and remaining dependencies proportionate to their consequences.

**Violation signature.** The result omits requested work; a concept is blocked by an irrelevant demand for operating history; paperwork replaces specialist production; critique removes substance without repairing the construction; a useful possibility is left as a plan despite available means to produce it; structure is used to claim specialist success; a consequential dependency is hidden; a reported result lacks the appropriate check or observation.

**Status.** Verified through the actual checks and specialist consumer-use evaluation below.

**Verification.** Determine acceptance from the required properties below and actual retained evidence, including specialist evaluation where needed. Check usefulness, substantive quality and correctness at the result's intended stage. Correction owner: the decision, method, operation or deliverable requiring strengthening or repair.

| Document type | Required properties | Evidence class / method |
| --- | --- | --- |
| `segments` | I1, I2, I3, I4, C1–C7 | `market estimate` and `check`; specialist neighbour contrast and recognition review; Evidence, Engagement and Product can identify and serve a member |
| `target-segments` | I5, I6, I7, C1–C7 | `check`; `market qualify`, `market score` where used; specialist horizon and alternative comparison; Engagement can qualify a prospect |
| `opportunities` | I4, I8, C1–C7 | `check`; specialist progress, attractiveness and development-action review; Product and design-offers can construct a response |
