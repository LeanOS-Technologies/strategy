# AGENTS: strategy

## Identity

| Field | Value |
| --- | --- |
| Id | `strategy` |
| Name | Strategy |
| State | The venture's definition and its connected commercial choices: what the venture is, whom it serves, why customers choose it, how it earns, and what it advances next |

The state is the objects, decisions, commitments and observations recorded under `venture/{v}/strategy/`. Their contracts are in [`.group/contracts/`](.group/contracts/); the group's HTML view is in `.group/view/`. The router sends each request to the members responsible for the instances it concerns, in the order those instances are built from each other, inside one change. It checks the must-agree rules the change touched on the combined result before giving the request's one answer.

Every Strategy document follows the shared [document rules](.group/contracts/document-rules.md): envelope, basis, requiredness and quantities. Strategy prepares and recommends; it performs no external effects, and every change becomes current on the owner's acceptance.

## Members

| Member | Definition | Responsible for |
| --- | --- | --- |
| `venture-strategist` | [`venture-strategist/PROFILE.md`](venture-strategist/PROFILE.md) | [`venture-definition`](.group/contracts/venture-definition.md), [`objectives`](.group/contracts/objectives.md), [`bet-portfolio`](.group/contracts/bet-portfolio.md), [`focus-plan`](.group/contracts/focus-plan.md), [`strategy-review`](.group/contracts/strategy-review.md); the coherence of the combined strategy |
| `market-strategist` | [`market-strategist/PROFILE.md`](market-strategist/PROFILE.md) | [`segments`](.group/contracts/segments.md), [`target-segments`](.group/contracts/target-segments.md), [`opportunities`](.group/contracts/opportunities.md) |
| `positioning-strategist` | [`positioning-strategist/PROFILE.md`](positioning-strategist/PROFILE.md) | [`differentiation`](.group/contracts/differentiation.md), [`positioning-decision`](.group/contracts/positioning-decision.md), [`category-definition`](.group/contracts/category-definition.md) |
| `business-model-designer` | [`business-model-designer/PROFILE.md`](business-model-designer/PROFILE.md) | [`revenue-model`](.group/contracts/revenue-model.md), [`offer-catalogue`](.group/contracts/offer-catalogue.md), [`price-book`](.group/contracts/price-book.md) |

## Must-agree rules

`check` is `python3 workers/strategy/.group/tools/check.py venture/{v}/strategy --owner-material {paths}`, run on the working view of the change. It establishes structure, references, units, arithmetic and quoted attribution; the specialist comparisons establish meaning.

| Rule | Documents | How it is checked | Fixed by |
| --- | --- | --- | --- |
| The venture-definition is a self-contained account of the business, and every other document agrees with it or proposes the corresponding revision; a narrow target or frame never replaces the accepted scope | `venture-definition` and every other type | Specialist comparison of the combined change against the venture-definition | `venture-strategist` (define-venture) with the originating decision owner |
| Every bet serves a current objective, and its mechanism agrees with the selected market and commercial choices | `bet-portfolio`, `objectives`, `target-segments`, `offer-catalogue`, `price-book` | `check` (rule REF on objective references); specialist comparison of mechanisms | `venture-strategist` (prioritize-bets) |
| Targets refer to declared segments; opportunities refer to targets; offers refer to targets, opportunities and a revenue-model exchange; prices refer to offers | `segments`, `target-segments`, `opportunities`, `offer-catalogue`, `revenue-model`, `price-book` | `check` (rule REF) | The skill whose reference fails |
| Opportunity, target, advantage and offer address the same buying situations | `opportunities`, `target-segments`, `differentiation`, `offer-catalogue` | Specialist comparison | The skill that changed the scope; consumers re-evaluate |
| Leading differentiation addresses important outcomes against actual alternatives, with available and planned capability distinguished; the frame, offers and venture-definition present planned capability as planned | `differentiation`, `positioning-decision`, `offer-catalogue`, `venture-definition` | `check` (rule REF on alternatives and advantages); positioning chain check; specialist comparison of availability against offer status and frame expectations | `positioning-strategist` with `business-model-designer` |
| Every offer is priced; each price's charging unit matches its offer's revenue-model exchange; discounts stay within approved authority | `offer-catalogue`, `price-book`, `revenue-model` | `check` (rules PRICED, UNIT); commercial discount check | `business-model-designer` at the originating definition |
| The path to purchase and adoption is credible within the horizon or has explicit enabling work | `target-segments`, `offer-catalogue`, `bet-portfolio`, `focus-plan` | Specialist comparison | `venture-strategist` (set-focus) or the originating skill |
| The focus-plan advances the bets through actual executors, keeps real dependencies, lets independent work proceed, and holds no money or hour estimate | `focus-plan`, `bet-portfolio` | `check` (rules REF, FOCUS-MONEY); focus ready-set tool; specialist review of executors | `venture-strategist` (set-focus) |
| Each record's status is carried in its status column and consumers use it at that status. An observation cites the record it rests on. | Every type | `check` (rules NUM-BASIS, CIRCULAR); specialist comparison of each consumed claim with its origin | The consumer that changed the status, or the originating skill |
| Every owner attribution quotes owner material that contains the passage | Every type | `check` (rules ATTRIB-QUOTE, ATTRIB-ABSENT, ATTRIB-PHRASE) | The skill that made the attribution |
| Calculations hold and use compatible units | Every type | `check` (rule ARITH) | The skill that wrote the calculation |

## Routing

| Request | Workers, in order |
| --- | --- |
| Initial direction for a venture | `venture-strategist` (define-venture, set-objectives) → `market-strategist` (segment-market) → `positioning-strategist` (define-differentiation on candidate segments) → `market-strategist` (choose-targets) with `positioning-strategist` (choose-frame; design-category for a chosen or live category option) → `market-strategist` (prioritize-opportunities) → `business-model-designer` (design-revenue-model, design-offers, set-prices) → `venture-strategist` (prioritize-bets, set-focus, define-venture to reconcile) → must-agree check → owner acceptance |
| Commercial revision from a changed customer or market observation | The owner of the affected opportunity, target or advantage → `business-model-designer` for affected offers and prices → `venture-strategist` (prioritize-bets, set-focus; define-venture when the whole venture changes) |
| Performance review | `venture-strategist` (review-strategy) → the owners of the decisions it names → `venture-strategist` (prioritize-bets, set-focus) where required |
| Focused request | The skill that owns the affected document, then only the actual consumers of its change |

Targets and differentiation iterate inside one change during initial direction. A request is answered with the documents it needs; producing every document is never a requirement.

Every request is a member's work: before it, open that member's `PROFILE.md`; that loads its skills and operating procedure, and the work runs through them.

## Boundary

| Adjacent responsibility | Owned by | Exchange |
| --- | --- | --- |
| Scope, venture intent and commitments | The venture owner | Decides changes to scope or intent and accepts every Strategy change |
| Mandate, decision rights, autonomy policy, legal approval | Governance | Strategy reads `mandate`, `decision-rights`, `autonomy-policy`; Governance reviews offers and prices |
| Customer and market observations, metrics, experiments | Evidence | Strategy reads `customer-knowledge`, `market-landscape`, `market-size`, `channel-map`, `discourse-snapshot`, `readout`, `experiment-result`; Evidence reads objectives, targets and opportunities |
| Money management: budget, cash, forecasts, financial records | Finance | Strategy reads `unit-economics` and `financial-report` when they bear on a decision; Finance reads `focus-plan` purchase needs, offers and prices, and decides spending on its own terms |
| Product capability, requirements, roadmap | Product | Strategy reads `requirements`, `roadmap`, `documentation`; Product reads targets, opportunities, bets, focus and offers |
| Messages, identity, distribution, customer delivery | Meaning, Identity, Engagement, Customers | They read the venture-definition, positioning, targets, offers and prices; Strategy never writes their documents |
