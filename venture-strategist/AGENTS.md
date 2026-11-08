# AGENTS: venture-strategist

Operating procedure for this worker. [PROFILE.md](PROFILE.md) owns its declaration, domain model, interfaces and authority. [INVARIANTS.md](INVARIANTS.md) owns required properties and verification. This file owns routing, execution, recovery and delivery.

## Routing

Evaluate rows top to bottom; the first matching row determines entry. Combined work continues through the dependent rows.

| Request class | Executor / usable result |
| --- | --- |
| What the venture is; define, explain or revise the business; reconcile after commercial choices | [define-venture](.claude/skills/define-venture/SKILL.md) → `venture-definition` |
| Goals, outcomes, targets, horizon, what to concentrate on | [set-objectives](.claude/skills/set-objectives/SKILL.md) → `objectives`; runs define-venture first when no venture-definition exists |
| Which bets or initiatives to run, grow, hold or close | [prioritize-bets](.claude/skills/prioritize-bets/SKILL.md) → `bet-portfolio`; needs `objectives` |
| What to do now, next, in parallel; what is blocked and how to unblock it | [set-focus](.claude/skills/set-focus/SKILL.md) → `focus-plan`; needs `bet-portfolio` |
| A result, readout, missed target or new condition: what it means and what to change | [review-strategy](.claude/skills/review-strategy/SKILL.md) → `strategy-review`; named changes go to their owning skills |
| Evaluate existing Strategy documents | The skill owning each document, read-only; the evaluation is given in the answer |
| Segments, targets, qualification, opportunities | Deliver the supported part; the answer names market-strategist for the rest |
| Differentiation, frame, category | Deliver the supported part; the answer names positioning-strategist for the rest |
| Revenue model, offers, prices | Deliver the supported part; the answer names business-model-designer for the rest |
| Money: spending, cash, budget, forecast, runway | The answer names Finance; set-focus may name the purchase an action needs |
| Mandate, decision rights, legal terms | The answer names Governance |
| Executing work: campaigns, product builds, outreach | Deliver the supported strategy; the answer names the executing group and the prepared focus-plan with outputs, prerequisites and executors |
| Any other request | Identify the intended outcome; route its supported part, or name the adjacent owner and what that owner needs |

Use the simplest supported executor. Do not create additional agents for a request that a skill can complete. This worker never invokes another worker.

## Process

**Resolve → Validate → Develop and execute → Verify and strengthen → Deliver.** Iterate development and evaluation when the domain method benefits from it.

### 1. Resolve

- Read the request using PROFILE Inputs. Establish the owner's purpose, starting point, intended result, material constraints and existing authority.
- Recover relevant owner material, convictions, ambition, decisions and available capabilities. Select the route that can develop the requested result from this starting point.
- Resolve missing information: retrieve, research, produce, propose, use a legitimate reversible assumption or prepare a necessary owner decision. Identify which dependent operation actually needs the information.
- Exercise the choices delegated to this worker. Prepare consequential choices reserved to the owner in concrete form and continue independent work.
- Resolve the owned targets to create or update; establish scratch. Creation establishes that the target is absent; update reads its current revision.

### 2. Validate

- Interpret input structure and meaning through PROFILE Domain model. Apply declared precedence and existing decisions. Resolve ordinary ambiguity through specialist judgment; make consequential working assumptions identifiable where they affect use.
- Read from the working view: current state with this change's candidates laid over it. Check the scope, role, revision and meaning relevant to the operation. Record consumed revisions in the document's *Built from* line.
- Accept intent, concepts and proposed designs as inputs to the transformations they can support. Require observations or operating history only where the selected operation depends on them.
- Check dependencies required by the selected path: `python3 --version` (3.11+) and `python3 workers/strategy/venture-strategist/tools/focus.py --help` for set-focus and review-strategy; `python3 workers/strategy/.group/tools/check.py --help` for every path. Preserve input snapshots and establish the mutation baseline appropriate to creation or update.
- Resolve obtainable or constructible inputs before returning NeedData. For a remaining dependency, name the affected operation, the input and the route to obtain it. Continue every supported independent step.
- Use an equivalent capability when interface meaning, effects and acceptance remain valid. Record a material substitution. Otherwise deliver the usable work available and the concrete continuation needed.

### 3. Develop and execute

Run the routed executor from PROFILE Operations. The skill or tool owns its specialist method, decisions and acceptance. Creative methods develop useful possibilities and carry the chosen approach into the requested result. Declarative methods resolve applicable constructions within their space and develop extension proposals where useful. Procedural methods execute their implemented operations.

Use available material and tools to produce the available useful result. Every run returns one of four outcomes. A Candidate proceeds to verification. NeedData names the affected operation, the required input and who or what can supply it. Conflict applies declared precedence and prepares the concrete choice for its owner. Failure is corrected at the owning operation or through an equivalent capability; otherwise the result names the step the work stopped at and the condition to continue. Continue every step whose inputs and authority hold; candidates proceed to verification.

### 4. Verify and strengthen

- Apply the domain and contract properties INVARIANTS C7 requires for the actual changed artifacts or state. Assess substantive fitness, usefulness and consumer usability alongside structural and computational correctness.
- Review what the result makes possible within this worker's responsibility. Develop useful substance, improve the construction and correct defects through their owning decisions or operations.
- Use the lightest suitable check for each required property. Keep structural, computational, specialist and empirical evidence appropriate to the property examined. Retain the target, criterion, method or evaluator, observation, verdict and locator where needed for acceptance.
- Recheck the changed result and affected descendants after correction. Check input preservation, write scopes, source and export relationships, update integrity and any external-effect confirmation.
- Express intent and ambition faithfully. Establish factual support and consequential assumptions where they matter. Report observed outcomes through actual observations and use visible qualifications where they affect understanding or action.

| Defect or strengthening opportunity | Correction owner / next action |
| --- | --- |
| Venture-definition reads as a slogan, inventory or narrow target | define-venture; recheck documents that cite it |
| Objective is an activity; target lacks status or rationale; baseline invented | set-objectives; recheck bets that reference it |
| Bet without objective contribution, falsifiable mechanism or alternative | prioritize-bets; recheck focus-plan |
| Focus gated on money or hours; independent work held; unavailable executor without enabling step; ready set disagrees with timing | set-focus; recheck with `focus.py ready` |
| Disposition without observation or exposure; review rewriting another owner's decision | review-strategy |
| Owner attribution without a quote, or quote absent from owner material | The skill that wrote it; re-evaluate dependent conclusions |
| `check.py` or `focus.py` error | The operation that failed; rerun after correction |
| Defect in another owner's material (segments, offers, prices, observations) | Prepare the correction for market-strategist, positioning-strategist, business-model-designer or the observation owner; continue the valid owned work |

### 5. Deliver

- Write each owned decision or construction as a candidate of the request's change at its declared path and contract. Its class's decider accepts it under existing authority. Write a confirmed observation into current state with its source.
- Record the work-result: revisions read, candidates and effects with their state, completed work and any condition required to continue.
- As a member of a group request, report to the router; the router gives the one answer.
- Lead with the usable result, what it enables and the next useful action. Return output references and keep supporting evidence accessible where its reader needs it.
- State remaining dependencies and departures from the request at the weight their consequences deserve.
- Report an external effect on confirmation. Reconcile an unknown outcome before any retry.

## Delivery

Each document goes at its declared path, in the form its contract's Representation declares. A decision changes through a candidate of its change. Creation uses an absent-base marker; update uses the revision read. Acceptance follows the declared decision rights, including delegated acceptance. An observation is written to current state by its confirming operation. An instance with an open candidate in another change is joined to that change or waits for it, never merged silently.

Write scopes: `venture/{v}/strategy/candidate/{venture.md, objectives.md, bet-portfolio.md, focus-plan.md, strategy-review/{period}.md}` and the request's `work-result.md`; scratch. Input snapshots remain unchanged. Ordinary execution never alters installed knowledge, skills, tools or contracts.

## Operating rules

- Construct and evaluate the actual requested result; documentation and packaging support the specialist work.
- Develop from the starting points this responsibility supports, including intention, concepts and launch preparation where applicable.
- Preserve canonical editable sources and source relationships. Regenerate deterministic exports; retain accepted generated candidates and relevant settings.
- Apply declared effect bounds and permission levels. Credentials stay outside the worker.
- Keep observations, computed results and proposals accurate in their relevant context. Present useful ideas and completed capabilities directly, with support appropriate to the statements being made.
