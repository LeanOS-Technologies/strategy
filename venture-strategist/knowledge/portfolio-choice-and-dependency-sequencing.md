# Portfolio choice and dependency sequencing

How to compare bets under uncertainty, choose a set that works together, and turn the chosen bets into a sequence where independent work starts now. Consumers: [prioritize-bets](../.claude/skills/prioritize-bets/SKILL.md) compares and selects bets; [set-focus](../.claude/skills/set-focus/SKILL.md) sequences their actions.

## 1. What a bet is

A bet is an intervention with a proposed mechanism: **condition → intervention → hypothesised response → contribution to an objective.** Three kinds differ in what success means:

| Kind | Purpose | Success |
| --- | --- | --- |
| Establish | Create a capability or position the venture lacks | The capability exists and works for a customer |
| Exploit | Use an existing advantage to produce the outcome | The outcome moves |
| Resolve | Reduce an uncertainty that blocks a consequential choice | The later decision changes, or is confirmed, on the evidence |

A resolve bet names the decision it informs. Information that would not change any commitment is not worth a bet.

## 2. Comparing bets without fabricated precision

Compare on the dimensions that differ between the real alternatives: contribution to the objective, time to a readable result, delivery conditions, dependencies, reversibility, and the options it opens or closes.

- **Expected value** is usable only when outcomes, horizon and probabilities each have a defensible basis (observed rates, comparable cases). With invented probabilities it launders a preference into a number.
- **Scenarios** are the honest default: state what each bet yields if the hardest assumption holds and if it fails, and look for a **preference reversal**: the condition under which the ranking flips. That condition is what to watch.
- **Do not double count.** Learning value is counted once, as the better later choice it enables. An intermediate benefit (a trial user) and its downstream benefit (a paying user) are one chain, not two gains.
- **Cheap and reversible** work earns priority when it improves the sequence of commitments (it resolves something before a hard-to-reverse step), not as a universal preference.

Continuing current work is always one of the alternatives.

## 3. Portfolio fit

Bets reinforce when one produces an input another needs (a trial produces the case evidence an outreach bet uses), and compete when they draw on the same customers' attention, the same product changes or the same owner decisions. Select a set whose combined demands on those shared inputs are feasible, and name the strongest forgone bet with the condition that would bring it back.

Control conditions are set before results: what observation, by which horizon, earns continuation, more emphasis, a change or a stop. A threshold set where the bet already passes is not a control.

## 4. Dependency versus preference

| Relation | Test | Effect on sequence |
| --- | --- | --- |
| Dependency | Action B needs an output, access or authority that action A produces | B waits for A |
| Preference | B is more valuable after A, but can be done without it | Priority only; B may start |
| Shared input | A and B use the same scarce input | Ordering by priority; both remain possible |

Calling a preference a dependency stalls work for no reason; calling a dependency a preference produces work that has to be redone.

## 5. The ready set

$$
Ready(A) = \{a \in A : \text{prerequisites}(a) \text{ are satisfied}\}
$$

A contains the concrete next actions, including enabling actions and preparation. Prerequisites are the actual inputs, access and action-specific authority. Order the ready actions by strategic contribution and enabling value; run independent ones in parallel. One blocked action never removes the others from the ready set. When nothing useful is ready, name the missing condition and its owner.

Executors are real: an installed worker, an available tool, a named person. An unbuilt group or unavailable tool is a missing prerequisite with an enabling step, not an executor. Work done by AI is described by its output and elapsed execution; a human appears only as a specific decision or contribution that an action needs. When an action needs a purchase, name the purchase and the action that needs it; Finance decides, and independent actions proceed.

`tools/focus.py ready` computes the ready set from the focus-plan's Prerequisite column and checks it against the Timing column.

## 6. Worked application

*Illustrative fixture: fictional venture, not evidence.* Brindlewick could bet on (a) converting the three non-paying users and their peers to paid use, (b) a trial for multi-inspector firms, or (c) building photo sync first. Firms "decide slowly and want a trial on a few jobs first", so (b) cannot produce paying use by the owner's March horizon unless the trial starts at once; (c) delays every paid outcome behind an unbuilt feature. (a) contributes most directly to the March outcome. The reversal condition: if direct inspectors decline to pay because the app lacks photo sync, (c) moves ahead. In the focus-plan, contacting the three users and preparing the paid offer are ready now; a firm trial waits only on a trial version of the setup service, which is an enabling action, not a reason to stop the direct route.
