# Registration and implementation review

The v25 plan was fixed after reviewing LINCS2020 metadata and the previous v19/v23
results, before opening the new expression matrices. It is an exploratory follow-up,
not a new prospective or independent biological study.

One wording error in the registered plan needs explicit correction: subtracting
140,945 annotated CRISPR treatments from 142,901 matrix columns gives 1,956, but this
does **not** establish that those columns lack metadata. They could include controls.
Preparation records the actual exact-ID join and perturbation types. The code neither
forces 1,956 missing records nor assigns invented labels. The original plan is retained.

A pre-run unit test exposed a numerical guard omission: ranking could turn infinity
into an ordinary finite rank. The helper now rejects nonfinite values **before** ranking.
Source preparation also rejects nonfinite expression matrices. The failed test and its
passing rerun are recorded; no scientific result was used to select this correction.

The plan's reference to isomeric SMILES is implemented using the source's
`canonical_smiles` field together with its `inchi_key`; the column name alone does not
guarantee resolved stereochemistry. The earlier InChIKey adjudication remains the
reference, and all compound IDs are kept separate. This is metadata verification,
not independent chemical analysis of experimental vials.

Ranks count only scores exceeding the target by more than 1e-6 to avoid float32
roundoff breaking numerical ties. They are descriptive retrieval ranks, not p-values.
Cross-batch eligibility excludes every reference sharing a source well with a query.
Repeated batches of one guide cannot satisfy independent-guide qualification.

The generic-response sensitivity subtracts a mean CRISPR rank vector, excluding BUB1B,
from both query and compound profiles. It can remove biological signal or introduce
common alignment. Agreement or disagreement after this transformation is a robustness
check, not proof that confounding has been removed.

The registered column-count question resolves to 140,945 CRISPR treatments plus 1,128
vector controls and 828 untreated controls; **no matrix columns lack metadata**.
The initial low-dose summary found no exact signature-ID matches. A source-well audit
then identified regrouping under changed IDs, as the plan required. Its first scope
sentence incorrectly named both old releases: the corrected `continuity-final.json`
limits this detailed regrouping check to GSE70138. Preparation separately checks
GSE92742. Both attempts remain in the archive; no result was discarded.

The first archive attempt safely rejected a Python cache directory encountered by
its file-only check. The final archiver enumerates regular files, still rejects
symlinks, and omits its own active output log. The failed attempt and source are
retained; the scientific results and original-coordinate validation are unchanged.

Full source matrices remain private to the working directories, with source URLs and
checksums. Public deliverables contain original analysis code and derived findings.
No raw subject data, clinical narrative, credentials, hosted inference or experimental
intervention is used. These are internal reviews, not independent specialist review.
