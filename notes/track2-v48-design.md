# V48 presentation rewrite

22 October 2026. This is a presentation-layer rewrite of v47 requested after the
design and prose reviews. It changes no scientific number, citation, decision,
drug disposition, evidence state, recording state, or biological claim. The v47
inputs, render audits, exports, snapshot, and bundle remain preserved unchanged.

## Report

The report now answers the four questions a judge asks first: what is proposed,
what order the work follows, what this team contributes, and what remains
outside the evidence. The title is direct: "Qualify function before testing an
approved drug." The opening section is "Proposal in one minute" with four bold
run-in labels: What we propose, The decision order, What we contribute, and
Current boundaries.

This replaces the previous opening paragraph, which buried the candidate and
the decision order in a wall of caveats. The caveats remain, but they now follow
the proposal instead of preceding it. One phrase was tightened: "uniform
robustness" became "uniform stability" because the finding concerns consistency
across guides, plates, aggregations, and seeds, not a general strength claim.

Every inherited boundary phrase, numerical result, citation, methods answer, and
the acknowledgement remains. The methods workbook still has 11 fields and a
335-word abstract.

## Slides

Slide 1 now says "Qualify function first." and states the proposal in three
lines: conditional approved-drug hypothesis; everolimus, an mTORC1 inhibitor,
on HOLD until endogenous BUB1B function is qualified. The note leads with the
next experiment—endogenous function, not exposure—and retains the no-rescue,
no-clinical-consideration boundary. The type scale and vertical rhythm were
adjusted to avoid overlap while keeping minimum 24 px text.

Slide 8 now separates "Reusable now" from "Qualify next." The reusable side
names the 18 offline evidence cases, CPU replay, no subject files or GPUs, and
the exact schema, reasons, and stop rules. The qualification side names
endogenous deficit plus independent restoration, joint-treatment benefit,
injury, and recovery, and fresh qualification for new tissues.

All other slide order, diagrams, palette, vector figures, contrast, links, and
acknowledgement are unchanged. No animation, gradient, shadow, or external
asset was added.

## Verification

`scripts/track2_public_review_v48.py` inherits all v47 checks, adds the report
hierarchy requirements, exact v48 route checks, the no-slop scan, and the new
slide boundary phrases. The BEACON acknowledgement is exempt from the word scan
because it is the sponsor's name.

The new deck rendered with zero outside text, zero overlaps, and minimum 24 px
text. The report PDF and methods workbook were exported and round-trip checked.
The v48 recording-materials bundle contains 107 files. The second v48 verified
snapshot preserves both v48 iterations and all historical releases.

Passing checks establish consistency and implementation quality, not biology,
upload readiness, or prize eligibility.
