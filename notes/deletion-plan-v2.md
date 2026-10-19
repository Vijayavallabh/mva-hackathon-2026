# Current deletion obligation — correction, 19 October 2026

**Delete project data and confirm by 23 November 2026. Send the confirmation to
cnb@sagebase.org.** This supersedes the November 24 date and earlier recipient in
the historical deletion plan, frozen reports, releases and computation plans.

The [organizer's discussion 28](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/28)
explicitly names November 23. The [official rules at the reviewed revision](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/60e1c30e337ce6fe01813040dbe49979eb8c50aa/tabs/rules.py)
retain deletion within 30 days of close and update the confirmation address. The
submission deadline remains October 24, 23:59 UTC. The earlier date calculation
was wrong; immutable historical artifacts are preserved rather than silently edited.

The cleanup inventory covers `data/`, `results/`, `logs/`, dataset caches,
subject-bearing intermediates, recovery bundles and copies outside this checkout.
Include every owner-hosted project root below, with its environments, public inputs,
derived outputs, models, checkpoints, logs, archives and caches:

- `/home/prachh/v/mva-track2-pilot-20260920`
- `/home/prachh/v/mva-track2-expanded-20260920`
- `/home/prachh/v/mva-track2-expanded-latest-20260921`
- `/home/prachh/v/mva-track2-transcriptome-20260927`
- `/home/prachh/v/mva-track2-rnai-20260927-v23`
- `/home/prachh/v/mva-track2-crispr-20261001-v25`
- `/home/prachh/v/mva-track2-falsification-20261001-v27`
- `/home/prachh/v/mva-track2-orthogonal-20261006-v29`
- `/home/prachh/v/mva-track2-perturbseq-20261007-v31`
- `/home/prachh/v/mva-track2-optical-20261019-v33`

The remote campaigns used public resources and permitted derived outputs, never
source subject reads, VCF records or clinical narrative. Their inclusion in this
inventory is deliberately explicit. The public code and permitted tracked
summaries remain subject to the organizers' publication and retention terms;
do not infer permission to retain subject-bearing intermediate datasets.

This note updates the schedule and inventory. No deletion or email has occurred.
Feat-010 remains not started. Before cleanup, inventory all project copies and
separate unrelated owner files; after cleanup, verify removal before sending a
truthful confirmation. The owner has not authorized contacting the family.
