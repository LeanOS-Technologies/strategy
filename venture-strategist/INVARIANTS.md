# INVARIANTS: venture-strategist

Each invariant states a required property, its observable violation, its status and verification appropriate to that property. Verification examines actual artifacts, operations or observations. Use the lightest suitable checks that establish the required properties and strengthen the usable result.

Status: **Enforced**, invalid construction or transition is prevented within the stated boundary; **Verified**, the stated check establishes the property under relevant premises; **Assumed**, correctness depends on a named condition not established here. These are verification statuses, not labels required on the worker's prose.

Notation: `D` = the owned document paths and their candidates (`venture/{v}/strategy/{venture.md, objectives.md, bet-portfolio.md, focus-plan.md, strategy-review/*.md}` and the same under `candidate/`); `T` = scratch scope; `U` = none. `V` = venture-definition; `O` = objectives; `B` = bet-portfolio; `F` = focus-plan; `R` = strategy-review; `M` = owner material; `check` = `python3 workers/strategy/.group/tools/check.py venture/{v}/strategy --owner-material M`; `ready` = `python3 workers/strategy/venture-strategist/tools/focus.py ready`.

## Domain invariants and laws

### I1 Venture coherence and scope authority

**Property.** `V` explains, on its own, what the venture does, who uses and buys it, what they receive, how it operates and how its activities form a business. Every part carries its status (available, accepted direction, proposed, future, excluded). A narrower current focus appears inside the accepted scope; changing the scope or excluding an accepted line is a separate proposal in `V`.

**Violation signature.** The Conclusion is a slogan or category label; the body is a product inventory or link list; planned capability reads as delivered; a beachhead target or a frame replaces what the venture is; prices or targets are copied into `V`.

**Status.** Verified by specialist evaluation per request.

**Verification.**

- Class: specialist evaluation; structural for envelope, sections and status column.
- Target and method: the candidate `V` read alone by the evaluator, who writes the venture's purpose, customers, offering, mechanism and exchange in their own words and compares them with `M` and accepted decisions; `check` for structure.
- Acceptance: the restatement matches `M` and accepted decisions without consulting other Strategy documents; every Scope row has a status; no planned part reads as present.
- Evidence: the request's work-result, with the evaluator's restatement and the `check` output.
- Correction owner: define-venture; the originating member when its document contradicts `V`.

### I2 Objective status

**Property.** Each objective in `O` is an observable outcome. Its target states its status (owner-set, proposed, accepted) and rationale; an owner-set target quotes `M`. A baseline is an observation with its source or `unknown`; a target is never written as a forecast or baseline.

**Violation signature.** An activity listed as an objective; a target with no rationale; "owner-set" with no quote; a baseline invented from the target; "we expect to reach" language for a chosen target; a date moved without stated reason.

**Status.** Enforced for status values, quotes and labels (`check` rules STATUS, ATTRIB-QUOTE, ATTRIB-ABSENT, ATTRIB-PHRASE, NUM-BASIS); Verified by specialist evaluation for the outcome/activity distinction and rationale.

**Verification.**

- Class: structural and specialist evaluation.
- Target and method: `check` on the working view; evaluator reads each row: outcome or activity, rationale present, baseline origin.
- Acceptance: zero `check` errors on `O`; every row passes the evaluator's reading.
- Evidence: `check` output and the work-result.
- Correction owner: set-objectives.

### I3 Bet mechanism and objective relevance

**Property.** Every bet in `B` references a current objective and states condition → intervention → hypothesised response → objective contribution, its hardest assumption, a relevant alternative and continue/change/stop conditions with their own basis. A response estimate carries an estimate label and basis; learning is valued once, as the decision it can change.

**Violation signature.** A bet whose objective reference does not resolve; a mechanism that restates the intended outcome; thresholds set exactly where the bet passes; expected value from invented probabilities; an exploration bet that names no later decision.

**Status.** Enforced for objective references (`check` rule REF); Verified by specialist evaluation for mechanism and comparison.

**Verification.**

- Class: structural and specialist evaluation.
- Target and method: `check`; evaluator traces each mechanism link and asks which observation would show it false.
- Acceptance: zero REF errors; each bet has a falsifiable mechanism and a named alternative.
- Evidence: `check` output and the work-result.
- Correction owner: prioritize-bets; set-objectives when the objective itself is inadequate.

### I4 Actionable focus

**Property.** In `F`, the actions timed `now` or `parallel` are exactly the ready set Ready(A) under the stated satisfied prerequisites; every blocked action has an enabling action; every executor is installed or a named person; independent work proceeds when one action is blocked; a needed purchase is named with the action that needs it. `F` holds no amount of money, reserve, budget line, hour estimate or headcount.

**Violation signature.** A `now` action waiting on an unproduced output; all work held behind one unavailable tool or purchase; an unbuilt group named as executor without an enabling action; amounts or hour estimates in the plan; a dependency cycle.

**Status.** Enforced for money and hour estimates (`check` rule FOCUS-MONEY) and bet references (REF); Enforced for ready-set agreement and cycles when `ready` runs with the request's satisfied prerequisites; Verified by specialist evaluation for executor availability.

**Verification.**

- Class: computational, structural, specialist evaluation.
- Target and method: `check`; `ready F --satisfied …` (exit 0 required); evaluator confirms each executor exists in the registry or is a named person.
- Acceptance: zero errors from both commands; every executor confirmed.
- Evidence: command outputs in the work-result.
- Correction owner: set-focus; prioritize-bets when the bet choice itself must change.

### I5 Diagnosis before prescription

**Property.** Each disposition in `R` compares the expected result with an actual observation and states whether the intervention ran with enough exposure. Material outcome gaps list competing explanations and the observation that discriminates them. Each required change names its artifact and owning skill. A plan or scenario is never counted as a result; sunk effort is never a reason to continue.

**Violation signature.** "Pivot" after one weak result with no exposure check; a disposition with `unknown` observed value and a firm conclusion; a review that rewrites prices or targets itself; continuing because effort was spent.

**Status.** Verified by specialist evaluation; Enforced for references and observation labels (`check` REF, NUM-BASIS).

**Verification.**

- Class: specialist evaluation; computational where `focus.py compare` computes gaps.
- Target and method: evaluator checks each disposition against its observation and exposure; `compare` for expected versus observed values.
- Acceptance: every disposition has an observation or an explicit next observation and decision point.
- Evidence: the work-result with `compare` outputs.
- Correction owner: review-strategy.

### I6 The venture-definition carries the owner's perspective and ambition

**Property.** The venture-definition develops the owner's worldview, convictions and ambition into a coherent purpose and scope. Perspective and ambition carries the owner's view at full strength with quotes in its basis line.

**Violation signature.** The definition opens with a product inventory; the owner's view is absent; current offers set the limit of ambition.

**Status.** Verified by specialist evaluation per request.

**Verification.**

- Class: specialist evaluation; structural where the group check applies.
- Target and method: Read Perspective and ambition against owner material; trace its implications into the venture's purpose, scope and operating mechanism.
- Acceptance: A consumer can explain the owner's view, the possibility it opens and how the venture pursues it.
- Evidence: the candidate, cited owner material, check output and evaluation in the request's work-result.
- Correction owner: define-venture; recheck dependent objectives and narrative.

### I7 The objective set serves the ambition

**Property.** Objectives express the owner's ambition for reach, adoption, authority or scale beside the first commercial outcomes. Each outcome has an observable criterion and a reasoned contribution to that ambition.

**Violation signature.** Only short-term sales appear despite a wider ambition; an ambition is replaced by an activity; a target supplies an invented baseline.

**Status.** Verified by specialist evaluation per request.

**Verification.**

- Class: specialist evaluation; structural where the group check applies.
- Target and method: Compare the objective set with Perspective and ambition; trace each commercial objective into the intended wider outcome and inspect Baseline and Basis.
- Acceptance: The set preserves the ambition and gives bets observable outcomes to serve; a new venture uses starting as its baseline.
- Evidence: the candidate, cited owner material, check output and evaluation in the request's work-result.
- Correction owner: set-objectives; recheck prioritize-bets and set-focus.

## Contract invariants

### C1 Ownership and write scopes

**Property.** Input snapshots and unrelated state remain unchanged. Writes are confined to `D`, `T` and any declared `U`. An authorised update affects only worker-owned targets. Corrections to another owner's state are prepared for that owner through the declared interface.

**Violation signature.** Input snapshot changed; an unrelated object was modified; a write exceeded its declared scope; another owner's state was silently corrected.

**Status.** Verified per request by comparison of writes with the declared scopes.

**Verification.** Class: structural. Method: record the current revisions and relevant write scope at intake, then compare the actual writes with `D`, `T` and any declared `U`; confirm input snapshots and unrelated state are unchanged. Prepare corrections outside venture-strategist's ownership for the named source owner. Evidence: intake revisions and the work-result's write list; endpoint equality establishes preservation at those endpoints. Correction owner: the operation that wrote out of scope.

### C2 Request distinction and update integrity

**Property.** Creation confirms that its target is absent and does not overwrite another result. An update has an explicit owned target, is based on its current revision and preserves unrelated content. Request inputs, outputs and material changes remain distinguishable. Creation needs no prior instance.

**Violation signature.** A collision overwrites a prior result; an update target lacks authority; its base moved without reconciliation; unrelated content changes; a result cannot be tied to its request; creation is blocked merely because no prior instance exists.

**Status.** Verified through creation or update preflight and final comparison.

**Verification.** Class: structural. Method: creation checks that the target is absent; inspect `candidate/` for another change before writing. For updates, compare the target's current revision with the revision read using `strategy_docs.py rev`, reconcile movement and inspect the candidate for unrelated changes. Tie each output to its request. Evidence: preflight revisions and work-result. Correction owner: venture-strategist's delivery step.

### C3 Canonical sources and derived representations

**Property.** Each object has one declared authority for its concern. Deterministic exports are regenerated from canonical sources. Accepted nondeterministic candidates are retained with relevant inputs and settings. Derived representations preserve their source relationship; exact regeneration is claimed when a supporting mechanism establishes it.

**Violation signature.** An export disagrees with its source; an unrecorded edit changes a derived representation; a generated result is claimed reproducible without a supporting mechanism; competing authorities govern the same concern.

**Status.** Verified for canonical documents and regenerated views; generated prose is retained with its inputs.

**Verification.** Class: structural and computational. Method: treat the owned Markdown as canonical, retain the selected candidate and consumed revisions, regenerate the group view with `workers/strategy/.group/tools/view.py` and compare using `--check`. Inspect source relationships for any generated material; exact replay is asserted only for a checked deterministic operation. Evidence: candidate, Built from, work-result and view check output. Correction owner: venture-strategist's generating operation or canonical source.

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

**Verification.** Class: structural. Method: compare actual writes and recorded commands with venture-strategist's local scopes and effect bounds; apply existing authority and prepare reserved owner choices concretely. Inspect any effect confirmation and uncertain-outcome reconciliation before claiming completion or retrying. Evidence: work-result, write list and any command confirmations. Correction owner: the effecting operation or reserved decision.

### C7 Whole, useful and developed result

**Property.** The actual result fulfils the request, meets its contract and required domain properties, and is usable by its intended consumer. Specialist work develops the requested substance from the starting point the responsibility supports. Creative work develops useful possibilities and carries the chosen approach into a substantive result. Verification assesses the actual construction and strengthens it where needed. The answer leads with what was produced, what it enables and the next useful action, with relevant support and remaining dependencies proportionate to their consequences.

**Violation signature.** The result omits requested work; a concept is blocked by an irrelevant demand for operating history; paperwork replaces specialist production; critique removes substance without repairing the construction; a useful possibility is left as a plan despite available means to produce it; structure is used to claim specialist success; a consequential dependency is hidden; a reported result lacks the appropriate check or observation.

**Status.** Verified through the actual checks and specialist consumer-use evaluation below.

**Verification.** Determine acceptance from the required properties below and actual retained evidence, including specialist evaluation where needed. Check usefulness, substantive quality and correctness at the result's intended stage. Correction owner: the decision, method, operation or deliverable requiring strengthening or repair.

| Document type | Required properties | Evidence class / method |
| --- | --- | --- |
| `venture-definition` | I1, I6, C1–C7 | `check`; specialist restatement of perspective, possibility and business mechanism; Meaning can develop a narrative from it |
| `objectives` | I2, I7, C1–C7 | `check`; specialist ambition-to-outcome trace; prioritize-bets can select routes to the outcomes |
| `bet-portfolio` | I3, I7, C1–C7 | `check`; specialist mechanism and assumption-test review; set-focus can sequence the next commitment |
| `focus-plan` | I4, C1–C7 | `check`; `ready`; executor confirmation and specialist dependency review; executors can start independent actions |
| `strategy-review` | I5, I6, I7, C1–C7 | `check`; `compare`; specialist diagnosis against exposure; decision owners can apply the named corrections |
