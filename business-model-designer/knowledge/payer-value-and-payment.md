# Payer, value and payment

How the people around a purchase, the value it creates and the payment that captures part of that value relate. Used by [design-revenue-model](../.claude/skills/design-revenue-model/SKILL.md) to choose who pays, when and for what, and by [set-prices](../.claude/skills/set-prices/SKILL.md) to judge what a price is anchored to and how payment timing changes the buyer's decision.

## 1. Four roles, often different people

| Role | Question it answers | What changes when it differs from the payer |
| --- | --- | --- |
| User | Who operates the product or receives the service | Usage value is felt by someone who does not sign; adoption effort falls on the user while the price falls on the payer |
| Beneficiary | Who gains from the outcome | Value can be claimed only through the payer's own revenue or cost; the price argument runs through the payer's economics |
| Decision-maker | Who chooses to buy | Procurement steps, approval thresholds and evaluation criteria come from this person, not the user |
| Payer | Whose money leaves | Budget line, payment method and timing preferences are the payer's |

Decision rules:

- Write the four roles for each exchange before choosing a charging basis. When all four are one person (a sole practitioner buying a tool), purchase friction is low and the price argument is direct; say so, because it permits a simple direct purchase.
- When the beneficiary is not the payer, the payer buys only the part of the beneficiary's gain that returns to them (higher fees, more referrals, fewer complaints, less time). Price against that returned value, never against the beneficiary's total gain.
- When the decision-maker is not the user (a firm owner buying for staff), expect a trial or evaluation step and a slower purchase; treat it as a buying condition of that segment, not a defect of the offer.

## 2. The purchase event and the obligation it creates

A charging rule is coherent when the event that triggers payment, the entitlement it grants and the obligation the venture takes on line up.

| Purchase event | Typical entitlement | Obligation created |
| --- | --- | --- |
| One-off purchase | Perpetual use of a version | Deliver that version; any update or support promise is a separate, stated term |
| Start of an access period | Use during the period | Keep the product available and working for the period |
| Each unit of use (report, seat, job) | That unit | Meter the unit accurately; the customer can predict cost only if they can predict usage |
| Service engagement | A defined deliverable | Deliver the scoped work; scope creep is a cost driver |
| Outcome achieved | Payment when the outcome is verified | Agree how the outcome is measured before work starts |

Decision rules:

- Name the event and the obligation together. A "licence" that implies free updates forever is an access subscription without the revenue; state which it is.
- Recurrence follows the customer's recurring use or recurring value. A subscription is justified when the customer keeps receiving something new (service, hosting, updates they need, data); it is not justified by the seller's preference for predictable revenue.
- Usage pricing fits when usage tracks the customer's own revenue or value and the customer can forecast it; it adds metering and invoice-surprise risk.

## 3. Comparing charging bases

| Criterion | Ask | Consequence for the choice |
| --- | --- | --- |
| Measurability | Can both sides observe the unit without dispute? | An unmeasurable unit needs a proxy or a different basis |
| Budget predictability | Can the payer know the cost before committing? | Unpredictable cost raises approval friction, most for small buyers |
| Procurement fit | Does the amount and form fit how this payer buys (card, invoice, approval threshold)? | A form that triggers a procurement process slows the first sale |
| Cost-value alignment | Does what the customer pays rise with what they receive and what it costs to serve them? | Misalignment either leaves value uncaptured or makes heavy users unprofitable |
| Expansion path | Does more use or more people naturally increase payment? | Expansion without a renegotiation helps growth; it must not punish the behaviour the venture wants |

Compare at least the strongest two bases on these criteria and state the condition under which the second would win. Revenue need not rise with every unit of a customer's realised value; growth can come from more customers, more scope or add-on services.

## 4. Payment timing

- Upfront payment reduces the venture's collection risk and raises the buyer's commitment barrier; split or monthly payment lowers the barrier and adds collection and churn exposure. Use the commercial tool's `timing` command to lay out what each schedule collects per period.
- For a service, a deposit before work and a balance on delivery ties payment to the obligation and limits unpaid work.
- Payment timing is a proposed term until accepted; financial treatment of it belongs to Finance.

## 5. Worked application

Illustrative fixture: fictional venture, not evidence.

Brindlewick sells to independent home inspectors [owner: "Brindlewick makes report software for home inspectors: the inspector walks the property, records findings on a tablet, and the app assembles a client-ready report."]. For a sole inspector, user, decision-maker and payer are one person [derived: role analysis of the brief]; the inspector's client (the homebuyer) benefits from a clearer report but pays the inspector, not Brindlewick. The returned value to the payer is time saved per report and a report that wins referrals [hypothesis: affects the charging basis and price]. Because the product is a desktop app [owner: "We sell a desktop report app"], a one-off licence matches the purchase event a sole buyer expects; per-report charging would align with the inspector's per-inspection income but needs metering the desktop app does not have. A subscription is justified only if Brindlewick commits to something recurring, such as updates the inspector needs; that commitment is an open design choice, not a fact.

Firms with several inspectors differ in role structure: the owner decides and the inspectors use [owner: "their owners decide slowly and want a trial on a few jobs first"]. That changes the purchase event (trial, then a multi-seat purchase) and the timing of revenue.

## Sources and scope

- Thomas T. Nagle and Georg Müller, *The Strategy and Tactics of Pricing*, 6th ed. (Routledge, 2018): value-based pricing and the distinction between the value created for a customer and the price captured. Used for pricing against the payer's returned value; it does not validate any particular price here.
- Madhavan Ramanujam and Georg Tacke, *Monetizing Innovation* (Wiley, 2016): choosing the monetisation model (licence, subscription, usage, outcome) alongside the product rather than after it. Used for the charging-basis comparison; their survey-based willingness-to-pay methods are evidence-gathering methods, not evidence by themselves.
