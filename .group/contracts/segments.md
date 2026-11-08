# Contract: segments

Shared rules: [document-rules.md](document-rules.md).

## Meaning

The demand situations that justify different commercial decisions. A segment groups situations in which needs, triggers, alternatives, purchasing conditions or required delivery are similar enough to share a decision and differ from neighbouring groups enough to change one. A segment can be large without being actionable now. Target choice compares these segments; opportunity work and Evidence use their situations and boundaries.

A segment definition is an analytic construction. It does not establish that its population or buying behaviour has been observed.

## Identity and scope

One instance per venture, at `venture/{v}/strategy/segments.md`. Segments carry IDs `SEG-n`. Exhaustive classification of the market is not required; one person or organisation can appear in several situations.

## Required properties

- Each segment states the situation or need that distinguishes it and the basis for it.
- Recognition criteria are usable: Evidence can recognise a member, Engagement can reach one, Product can understand its requirements.
- The Basis columns carry the source or reasoning for segments, recognition criteria and commercial profiles, including owner quotes and observed demand records. The candidate document carries proposed decision status.
- A size or range carries an estimate method and grounded factors, or is omitted or `unknown`.
- Demographic or firmographic attributes appear as boundaries only where they mark a consequential difference.

## Consumer reliance

choose-targets may rely on the distinctions and their decision relevance. Evidence may rely on recognition criteria to test membership. No consumer may rely on a proposed segment as observed demand.

## Acceptance

- Specialist evaluation (segment-market): segments differ in a way that matters to targeting or delivery and are recognisable.
- Computational (market-strategist estimate tool): every size estimate recomputes from its factors and each factor has a basis.
- Structural (document check): envelope, sections, columns, quoted owner passages, amounts with basis, references.

## Representation

| Section | Form | Size | Requiredness |
| --- | --- | --- | --- |
| Segmentation logic | Prose | Up to 2 short paragraphs | required |
| Segment definitions | Table | One row per useful segment | required |
| Commercial profile | Table | One row per segment | required |
| Boundaries | List | One line per material ambiguity | required |

**Segmentation logic:** which distinctions change decisions and why.

**Boundaries:** each overlap, exclusion or provisional distinction and its consequence.

### Segment definitions columns

| Column | Holds | Kind |
| --- | --- | --- |
| `ID` | `SEG-n` | id SEG |
| `Situation and need` | The distinguishing situation and need | reasoning |
| `Recognition criteria` | Observable criteria, proposed or established | reasoning |
| `Trigger` | The buying trigger, supported or hypothesised, or `unknown` | factual |
| `User and buyer` | Who uses and who buys | factual |
| `Alternatives` | What they use or do now | factual |
| `Basis` | Source, quote or reasoning for the segment and its need | reasoning |

### Commercial profile columns

| Column | Holds | Kind |
| --- | --- | --- |
| `Segment` | The segment | ref segments |
| `Demand and value` | Demand and value indications with basis | factual |
| `Reach and purchasing` | How it is reached and how it buys | factual |
| `Size` | Estimate or range with method, `unknown`, or `n/a` | factual |
| `Delivery` | Delivery implications | factual |
| `Basis` | Evidence basis of the profile | reasoning |
