# AGENTS: market-strategist

Operating procedure for this worker. [PROFILE.md](PROFILE.md) owns its declaration, domain model, interfaces and authority. [INVARIANTS.md](INVARIANTS.md) owns required properties and verification. This file owns routing, execution, recovery and delivery.

## Routing

Evaluate rows top to bottom; the first matching row determines entry. Combined work continues through the dependent rows.

| Request class | Executor / usable result |
| --- | --- |
| Evaluate existing segments, targets or opportunities | Read-only evaluation against INVARIANTS I1–I8 using the skill whose document is evaluated; the answer carries the evaluation; no write |
| Define or revise customer segments | [`.claude/skills/segment-market/SKILL.md`](.claude/skills/segment-market/SKILL.md) → `segments` |
| Choose or revise targets, qualification rules or segment sequence | [`.claude/skills/choose-targets/SKILL.md`](.claude/skills/choose-targets/SKILL.md) → `target-segments` |
| Qualify a specific prospect against the targets | `tools/market.py qualify` on the current `target-segments`; the answer gives the result and the unknown indicators |
| Identify or rank customer problems and progress for the targets | [`.claude/skills/prioritize-opportunities/SKILL.md`](.claude/skills/prioritize-opportunities/SKILL.md) → `opportunities` |
| Whole market selection (segments through opportunities) | segment-market → choose-targets → prioritize-opportunities, in that order, inside one change |
| Gather customer or market observations, size research, channel mapping | Deliver the supported part (the questions that would change a decision); the answer names Evidence for the rest |
| Advantage, alternatives as a comparison, competitive frame | Deliver the supported part; the answer names positioning-strategist |
| Offers, charging, prices | Deliver the supported part; the answer names business-model-designer |
| Objectives, bets, focus, venture scope | Deliver the supported market choices; the answer names venture-strategist and the prepared implications for objectives, scope and bets |
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
- Check dependencies required by the selected path: `python3 --version` (3.11 or later) when `market.py` or the group check will run. Preserve input snapshots and establish the mutation baseline appropriate to creation or update.
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
| A segment boundary changes no decision, or a segment is unrecognisable | segment-market; recheck targets that reference it |
| A size or count without factors and basis | segment-market: `unknown` or `market.py estimate` with factors |
| Target chosen without binding condition, horizon fit or strongest alternative | choose-targets; recheck opportunities, offers and bets referencing it |
| Focus replaces the venture's accepted scope | choose-targets restores the focus as a route; a scope change is proposed to define-venture |
| Prospect rejected for a missing fact | choose-targets: add the "When unknown" treatment; rerun `market.py qualify` |
| Opportunity stated as a solution, or evidence status promoted | prioritize-opportunities; inform design-offers and Product of changed priorities |
| Attribution the material does not contain (`check` ATTRIB errors) | The skill that wrote it; re-evaluate dependent conclusions |
| `market.py` or `check.py` fails to run | Report the failure with its output; fall back to self-review against the contract, labelled as such |
| Defect in another owner's material (Evidence, positioning, offers, objectives) | Prepare the correction for venture-strategist or the named source owner; continue the valid owned work |

### 5. Deliver

- Write each owned decision or construction as a candidate of the request's change at its declared path and contract. Its class's decider accepts it under existing authority. Write a confirmed observation into current state with its source.
- Record the work-result: revisions read, candidates and effects with their state, completed work and any condition required to continue.
- As a member of a group request, report to the router; the router gives the one answer.
- Lead with the usable result, what it enables and the next useful action. Return output references and keep supporting evidence accessible where its reader needs it.
- State remaining dependencies and departures from the request at the weight their consequences deserve.
- Report an external effect on confirmation. Reconcile an unknown outcome before any retry.

## Delivery

Each document goes at its declared path, in the form its contract's Representation declares. A decision changes through a candidate of its change. Creation uses an absent-base marker; update uses the revision read. Acceptance follows the declared decision rights, including delegated acceptance. An observation is written to current state by its confirming operation. An instance with an open candidate in another change is joined to that change or waits for it, never merged silently.

Write scopes: `venture/{v}/strategy/{segments,target-segments,opportunities}.md` through their candidates at `venture/{v}/strategy/candidate/`; the request's work-result; scratch. Input snapshots remain unchanged. Ordinary execution never alters installed knowledge, skills, tools or contracts.

## Operating rules

- Construct and evaluate the actual requested result; documentation and packaging support the specialist work.
- Develop from the starting points this responsibility supports, including intention, concepts and launch preparation where applicable.
- Preserve canonical editable sources and source relationships. Regenerate deterministic exports; retain accepted generated candidates and relevant settings.
- Apply declared effect bounds and permission levels. Credentials stay outside the worker.
- Keep observations, computed results and proposals accurate in their relevant context. Present useful ideas and completed capabilities directly, with support appropriate to the statements being made.
