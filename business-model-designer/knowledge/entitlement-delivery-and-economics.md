# Entitlement, delivery and economics

What a payment entitles the customer to, what that entitlement obliges the venture to deliver, and which delivery-cost drivers follow. Used by [design-revenue-model](../.claude/skills/design-revenue-model/SKILL.md) to name the drivers of an exchange's economics, and by [design-offers](../.claude/skills/design-offers/SKILL.md) to scope each offer so it can actually be delivered.

## 1. Entitlement is a promise with a cost

An entitlement is the exact set of things the payment grants: product access and its duration, version and update rights, support, a service deliverable, usage limits. Every element is an obligation, and each obligation has a cost driver.

| Entitlement element | Cost driver | Scales with |
| --- | --- | --- |
| Software access (local install) | Near-zero marginal delivery; support and compatibility work | Number of customers and the variety of their setups |
| Hosted access | Hosting, availability, data storage | Usage and data volume |
| Updates | Development and testing of each release for all entitled customers | Release frequency and the length of the update promise |
| Support | People's time per question; documentation reduces it | Customers × questions per customer |
| Service deliverable (setup, conversion, training) | People's time per engagement | Engagements × scope per engagement |
| Guarantee or refund | Refund rate and the work done before refund | Uncertainty of fit at purchase |

Decision rules:

- Write the entitlement as the customer would read it, then list the obligation and cost driver of each element. An element whose cost driver nobody can state is either removed or kept with its cost marked `unknown` and its effect on the choice named.
- Separate fixed obligations (shipping a version) from per-customer obligations (support, service). Per-customer obligations decide whether a low price stays viable at more customers.
- A service sold at a fixed price carries scope risk: define the deliverable, the customer's inputs and what is outside, or the cost driver is unbounded.

## 2. Present, committed and future delivery

| Status | Can be sold as | Must state |
| --- | --- | --- |
| Available | Part of the entitlement now | Nothing extra |
| Committed (roadmap with an accepted date) | A stated future element | The condition and the customer's remedy if it slips |
| Future possibility | Not part of the entitlement | It may be described only as a direction, never priced as included |

Decision rules:

- An offer's promised value is deliverable now or sold on stated future conditions. A roadmap item never enters the entitlement silently; check each element against product capability evidence (`documentation`, `roadmap`).
- When an attractive offer depends on missing capability, record the development dependency and let prioritize-bets sequence it, rather than dropping the offer or selling it as available.

## 3. Economics as drivers, not as made-up numbers

The economics of an exchange are its revenue drivers (price, purchases, renewals, expansion) and cost drivers (fees, delivery, support, service time). Strategy reasons about how they interact; Finance owns accepted metric definitions and the financial records.

- Contribution per transaction is net collected revenue minus the variable costs defined for that transaction. Compute it with `tools/commercial.py contribution`, which writes the expression and returns `unknown` when an input is unknown.
- Acquisition cost and lifetime effects need a compatible cohort and horizon. Without observed retention, lifetime value is not inferred.
- A driver without a basis stays `unknown`; what Strategy can still say is the direction of its effect ("support time per customer decides whether a low one-off price stays viable"). That direction is useful for the choice and is not a number.
- A conditional scenario ("if each conversion takes the effort of one template rewrite") is labelled as a scenario with its premise; consumers keep it conditional.

## 4. Worked application

Illustrative fixture: fictional venture, not evidence.

Brindlewick's setup service converts an existing template [owner: "offer a setup service where we convert an inspector's existing report template into ours"]. Its entitlement is one converted template; its cost driver is the people's time per conversion, which the brief does not state, so the driver's value is `unknown` and its effect on the choice is named: a fixed-price conversion is viable only if conversion effort is bounded, so the offer scopes one template, the customer supplies the existing template, and extra templates are a separate purchase [proposed].

Photo sync is not part of any entitlement [owner: "Photo sync from phones is planned for next year; it does not exist yet."]. An offer may mention it only as a direction; selling a licence that "includes photo sync" would sell a future possibility as available.

The free template pack [owner: "The free template pack stays free."] carries a small delivery cost (hosting a download) and no support promise unless one is stated; its role is commercial (entry and demonstration), set in the offer catalogue.

## Sources and scope

- Madhavan Ramanujam and Georg Tacke, *Monetizing Innovation* (Wiley, 2016): designing the offer configuration and its monetisation together. Used for scoping entitlements before pricing; it does not supply cost figures.
- Nagle and Müller, *The Strategy and Tactics of Pricing*, 6th ed. (2018): contribution as the price-relevant cost concept (incremental, avoidable costs). Used for the contribution definition above.
