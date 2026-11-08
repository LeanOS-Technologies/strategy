# Price, packaging, response and friction

How buyers respond to a price and to the way offers are packaged, and what makes a purchase easy or hard. Used by [design-offers](../.claude/skills/design-offers/SKILL.md) to decide packaging, entry offers, trials and guarantees, and by [set-prices](../.claude/skills/set-prices/SKILL.md) to develop a price that is worth trying and to know what would change it.

## 1. What a price is anchored to

A buyer judges a price against a reference: what they pay now for the alternative, what the alternative costs them in time or lost business, and the prices of things they consider comparable.

- **Economic value to the buyer** = the cost of their next-best alternative (reference value) + the net value of what is different about this offer (differentiation value, positive or negative). The price sits below that ceiling to leave the buyer a reason to switch. This is a reasoning structure; each term needs its own basis or stays a hypothesis.
- **Equivalent scope first.** Compare prices only after aligning scope and time: a one-off licence against a monthly subscription is compared over the period the buyer would use it; a tool against a service is compared on the work the buyer still has to do.
- **The status quo is an alternative.** When the buyer currently does the work by hand or in a word processor, the reference value is their own time and the risk of errors, which they may not count as money. Expect the reference to be weak and the price argument to need a demonstration.
- **Public price claims** (a competitor's rate) need an inspected source with its date; otherwise they stay out of the reasoning.

## 2. Response is a hypothesis until observed

- A chosen price is a commercial proposal. Purchases at that price are the observation; owner acceptance of the price is not.
- Bounded tests resolve the uncertainty that matters: a stated price on the first offer page for a defined period, a price point offered to a defined set of prospects, a paid pilot. Each names the observation and the decision it changes.
- When there is no willingness-to-pay evidence, still recommend a price: derive it from the reference value, the differentiation and the delivery economics, state why it is worth trying, and name the observation that would move it. Leaving the price blank is not neutral; it blocks the offer.

## 3. Packaging

| Construct | Use when | Avoid when |
| --- | --- | --- |
| Single offer, direct purchase | Buyers have similar needs and buying conditions | Never avoid by default; it is often the right first offer |
| Variants or tiers | Distinct needs, entitlements, purchasing conditions or delivery costs separate buyers | Differences are cosmetic, or tiers exist only to anchor |
| Bundle | Parts are more valuable together and buyers want most of them | Buyers want one part and resent paying for the rest |
| Free standalone product | It delivers a useful outcome within its own boundaries and serves the owner's declared purpose, at bounded delivery cost | Delivery or support obligations cannot be sustained, or its conditions conflict with the owner's policy |
| Demonstration or entry component (free or low price) | It supports a stated evaluation or commercial purpose consistent with the owner's policy, at bounded delivery cost | Its scope or conditions fail that purpose or conflict with the owner's policy; full usefulness alone is not a defect |
| Trial | Value is visible only in use and the buyer's decision-maker requires proof | Setup effort makes a trial expensive for both sides |
| Guarantee | Fit is uncertain at purchase and the venture can bear refunds | Delivered work (a service) cannot be returned |

Decision rules:

- Each variant states what decision it lets the buyer make and the upgrade condition. A tier without a decision-relevant purpose is removed.
- Choose between a free standalone product and a demonstration, trial or entry component from the owner's policy and customer need. Free pricing alone does not imply an upgrade path. State the purpose, delivery costs and support boundaries; delivery cost must stay bounded, and a free offer need not make a profit by itself.
- A free product fully satisfying its intended need is not itself a defect. Do not narrow it or make it paid merely to induce another purchase. Any conversion goal is a commercial hypothesis until observed and remains subject to the owner's policy.
- Anchors are used only when the comparison is accurate and useful to the buyer.

## 4. Purchase friction

Friction is anything between intent and payment: approval steps, payment method, setup effort before first value, uncertainty about fit, switching cost from the current tool.

- For a sole buyer, card payment and a short path to first value keep friction low; a sales call or invoice adds it.
- For a multi-person buyer, the decision-maker's evaluation (trial on real jobs, references) is the main friction; design the trial or pilot as part of the offer.
- Switching cost is often the template or data the buyer already has. An offer that removes it (conversion, import) can matter more than the price.

## 5. Discount and exception rules

- A discount has a commercial reason (launch test, multi-seat, annual commitment), an eligibility, a bound and the authority that approved the bound. Use `tools/commercial.py discount` to check a proposed concession against the bound and any price floor.
- A discount that invalidates the delivery arrangement (the net no longer covers the service time it buys) is outside the rule regardless of the percentage.

## 6. Worked application

Illustrative fixture: fictional venture, not evidence.

Brindlewick has not set prices [owner: "We have not decided prices."]. The sole inspector's current alternative is writing reports with existing templates by hand [hypothesis: affects the reference value; to confirm with Evidence]. The reference value is their time per report, which nobody has measured, so it stays a hypothesis. Three inspectors use the app without paying [owner: "They have not paid for it."]: that is usage, not evidence of willingness to pay.

Packaging: one desktop licence for sole inspectors, a scoped template conversion as a separate service, and the free template pack as the entry component [owner: "The free template pack stays free."] whose role is to show the report format before purchase [proposed]. Tiers are not introduced for sole inspectors, because nothing in the brief separates their needs. Firms want a trial [owner: "want a trial on a few jobs first"], so a firm offer is a trial on a few jobs followed by a multi-seat purchase, deferred until the sole-inspector offer has buyers [proposed].

## Sources and scope

- Nagle and Müller, *The Strategy and Tactics of Pricing*, 6th ed. (2018): economic value estimation (reference value plus differentiation value) and price-response reasoning. Used as the reasoning structure above, not as evidence of any buyer's response.
- Ramanujam and Tacke, *Monetizing Innovation* (2016): packaging by distinct customer segments and needs, and the risk of bundling components buyers do not value. Used for the packaging table.
