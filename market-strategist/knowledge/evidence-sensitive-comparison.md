# Evidence-sensitive comparison

How to compare segments, targets and opportunities so that the strength of the evidence, the attractiveness of the option and the arithmetic of any score stay distinct.

Consumers: [segment-market](../.claude/skills/segment-market/SKILL.md) (commercial profile and size), [choose-targets](../.claude/skills/choose-targets/SKILL.md) (the comparison against the strongest alternative), [prioritize-opportunities](../.claude/skills/prioritize-opportunities/SKILL.md) (priority and uncertainty).

## Two axes, never one number

Every comparison carries two separate judgments:

- **Attractiveness:** how much the option would be worth if the premises hold.
- **Evidence strength:** how well the premises are supported.

Collapsing them (discounting attractiveness by confidence, or ranking by "evidence-weighted score") hides the decision. A promising, poorly evidenced opportunity often deserves a cheap discriminating action; a well-documented minor problem does not outrank it merely because it is documented. Keep both visible and let the decision rule say what to do with each combination:

| Attractiveness | Evidence | Typical next move |
| --- | --- | --- |
| High | Strong | Commit; watch the reversing condition |
| High | Weak | Act on it where action is cheap and reversible, or run the observation that would discriminate |
| Low | Strong | Defer; record why |
| Low | Weak | Drop from the comparison unless it is the status quo |

## Compare with the available basis

Recover the owner's direction and develop the valuable progress each option could enable. Compare customer utility, delivery fit, purchase path and contribution to ambition before deciding which uncertainty deserves attention.

Use the basis to choose the next action:

- A reported need identifies the customer's situation; inspect whether the proposed result would serve it.
- Observed behaviour supplies a comparison condition; check whether it covers the target and use being considered.
- A developed application can justify a specimen or prototype before customers have requested it.
- A source from a neighbouring segment suggests a transfer to test; build the comparison that exposes the important difference.

Put source records, owner quotes and reasoning in the relevant basis cells under [document rules](../../.group/contracts/document-rules.md). Trace observations to their confirming records; a sequence of proposals supplies a design, not independent confirmation.

## Create the evidence the decision needs

Identify the premise whose resolution could change the choice. Produce the most useful proportionate demonstration, prototype, calculation, comparison or test available within the autonomy policy. Prefer an action that creates value while exposing the premise: a converted template, an annotated report or a worked purchase path.

State the criterion before examining the result. Inspect what the construction enables, where it fails and which choice changes. Prepare consequential market actions for the authorised owner while independent construction continues. Record the result at its actual scope and use it to strengthen or revise the option.

## Scores and their arithmetic

Scoring is optional. Use it when it clarifies a comparison with several criteria; reason directly when two or three binding conditions decide.

When scoring:

- Declare the scale and what each end means before scoring ("1 = buyer cannot be reached through any channel we have; 5 = we already talk to them").
- Use criteria that are not restatements of each other. Pain, severity and urgency are usually correlated; summing them counts the same thing three times. Pick the one that discriminates, or combine them into one judged criterion.
- State the decision rule (highest weighted total; or any option failing a gating criterion is out).
- Check preference reversal: the smallest change to one weight that changes the top choice. If a plausible disagreement about one weight flips the ranking, the choice rests on that judgment and the document says so.
- Record a score’s declared scale, weights and derivation in Basis. Use the total to compare the chosen criteria and inspect the reversal condition; its role is a structured judgment.

The worker's scoring tool runs the arithmetic and the reversal check: `python3 workers/strategy/market-strategist/tools/market.py score OPTIONS.csv --scale 1-5 --weights …`.

## Estimates and ranges

A size estimate is a product of factors, each with a basis. Report a range, not a point, and name the factor that drives the range. When a factor has no basis, the estimate is unknown: the honest output is "size unknown; the deciding factor is the number of independent inspectors", followed by the action that would obtain it. The estimate tool refuses to produce a number in that case (`python3 workers/strategy/market-strategist/tools/market.py estimate FACTORS.csv`).

Ask whether size matters for this decision at all. When the choice is decided by the buying cycle, an unknown size changes nothing and can be omitted with that reason.

## Failure modes

| Failure | Signature | Correction |
| --- | --- | --- |
| Confidence blended into value | One "score" mixing worth and certainty | Separate the two columns; apply the decision table |
| Double counting | Pain + severity + frequency summed | Keep the discriminating criterion; drop correlates |
| Fabricated precision | "Market: 4,820 inspectors" with no source | `unknown`, or a range with its factors and basis |
| Circular support | A proposal cited as evidence by the next document | Trace the premise to its supporting record; produce the missing comparison or observation |
| Unstable ranking presented as robust | Small weight change reverses the choice, unreported | Report the reversal condition |

## Worked application

Illustrative fixture: fictional venture.

Brindlewick compares independent inspectors with firms and develops a report-teaching application from its ambition for professional adoption. The first commercial choice depends on the buying path and deliverable capability; population size does not decide it.

| Option | Value and choice | Basis | Strengthening action |
| --- | --- | --- | --- |
| Independent inspectors | Direct route to paid report production | [owner: "three inspectors we know use it on their own jobs"] [owner: "They have not paid for it."] | Produce a complete sample and prepare a paid offer; observe purchase response after authorised delivery |
| Inspection firms | Wider adoption per buying decision; needs a fitting trial | [owner: "decide slowly and want a trial on a few jobs first"] | Develop a trial outline and inspect its capability dependencies |
| Teaching application | Extends the reporting approach to colleagues and trainees | [proposed] application developed from the founder's professional ambition | Build an annotated report and test transfer to a different example |

The teaching application earns development through its useful possibility. Its demonstration supplies evidence for the next choice.
