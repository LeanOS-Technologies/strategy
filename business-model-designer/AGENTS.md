# AGENTS: business-model-designer

Operating procedure for this worker. [PROFILE.md](PROFILE.md) owns its declaration, domain model, interfaces and authority. [INVARIANTS.md](INVARIANTS.md) owns required properties and verification. This file owns routing, execution, recovery and delivery.

## Routing

Evaluate rows top to bottom; the first matching row determines entry. Combined work continues through the dependent rows.

| Request class | Executor / usable result |
| --- | --- |
| Who pays, for what, when; charging basis, recurrence, expansion; a new or changed exchange | [`.claude/skills/design-revenue-model/SKILL.md`](.claude/skills/design-revenue-model/SKILL.md); continue to design-offers and set-prices when the exchange change alters their entitlement or unit |
| What the buyer gets: offers, packaging, entry offers, trials, guarantees, delivery scope | [`.claude/skills/design-offers/SKILL.md`](.claude/skills/design-offers/SKILL.md); continue to set-prices for changed or new offers |
| Prices, price tests, discounts, anchors, exceptions | [`.claude/skills/set-prices/SKILL.md`](.claude/skills/set-prices/SKILL.md) |
| A full commercial configuration for selected targets | design-revenue-model → design-offers → set-prices, then the group check on the assembled set |
| A contribution, payment schedule or concession check | [`tools/commercial.py`](tools/commercial.py) `contribution`, `timing` or `discount`; the answer states the inputs and their labels |
| Evaluation of the current revenue model, offers or prices | Read-only evaluation against INVARIANTS; the answer gives the findings and the owning skill for each |
| Billing, invoices, unit-economics records, budget, cash, forecasts | Deliver the supported part (the commercial reasoning); the answer names Finance for the rest |
| Legal terms, contract wording, commitments | Deliver proposed conditions; the answer names Governance for approved wording |
| A concession for an individual deal | Check it with `commercial discount` against the approved rule; the answer names Engagement to apply it within the rule, or the authority that must decide beyond it |
| Whether a capability exists or when it ships | Use the current capability status; the answer names Product for the evidence |
| Targets, opportunities, differentiation, frame, bets, focus | Deliver the supported commercial work; the answer names the owning Strategy member and the prepared choice with commercial consequences |
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
- Check dependencies required by the selected path: `python3 --version` (3.11 or later) when `commercial.py` or the group check is used. Preserve input snapshots and establish the mutation baseline appropriate to creation or update.
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
| Payer, event, entitlement and unit do not describe one purchase | design-revenue-model; recheck offers and prices |
| Price unit differs from the exchange unit (UNIT) | set-prices, or design-revenue-model when the exchange unit is wrong |
| Offer without a price row (PRICED) | set-prices |
| Offer promises planned capability as available | design-offers; positioning-strategist rechecks frame expectations |
| Amount without a basis, or a calculation that does not hold (NUM-BASIS, ARITH) | The skill that wrote it; rerun `commercial` |
| Owner attribution without a quote, or a quote absent from owner material (ATTRIB) | The skill that made the attribution; re-evaluate dependent conclusions |
| Concession outside its bound | set-prices states the concession for the authority that set the bound |
| `commercial.py` error or failed test | The tool; rerun its tests after the fix |
| Defect in a target, opportunity, differentiation or capability record | Prepare the correction for market-strategist, positioning-strategist or Product; continue the valid owned work |

### 5. Deliver

- Write each owned decision or construction as a candidate of the request's change at its declared path and contract. Its class's decider accepts it under existing authority. Write a confirmed observation into current state with its source.
- Record the work-result: revisions read, candidates and effects with their state, completed work and any condition required to continue.
- As a member of a group request, report to the router; the router gives the one answer.
- Lead with the usable result, what it enables and the next useful action. Return output references and keep supporting evidence accessible where its reader needs it.
- State remaining dependencies and departures from the request at the weight their consequences deserve.
- Report an external effect on confirmation. Reconcile an unknown outcome before any retry.

## Delivery

Each document goes at its declared path, in the form its contract's Representation declares. A decision changes through a candidate of its change. Creation uses an absent-base marker; update uses the revision read. Acceptance follows the declared decision rights, including delegated acceptance. An observation is written to current state by its confirming operation. An instance with an open candidate in another change is joined to that change or waits for it, never merged silently.

Write scopes: `venture/{v}/strategy/revenue-model.md`, `venture/{v}/strategy/offer-catalogue.md`, `venture/{v}/strategy/price-book.md` and their candidates under `venture/{v}/strategy/candidate/`; scratch. Input snapshots remain unchanged. Ordinary execution never alters installed knowledge, skills, tools or contracts.

## Operating rules

- Construct and evaluate the actual requested result; documentation and packaging support the specialist work.
- Develop from the starting points this responsibility supports, including intention, concepts and launch preparation where applicable.
- Preserve canonical editable sources and source relationships. Regenerate deterministic exports; retain accepted generated candidates and relevant settings.
- Apply declared effect bounds and permission levels. Credentials stay outside the worker.
- Keep observations, computed results and proposals accurate in their relevant context. Present useful ideas and completed capabilities directly, with support appropriate to the statements being made.
