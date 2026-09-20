# Data deletion obligation

Signed as part of gated access. **Due 2026-11-24** (30 days after the 2026-10-24 close).

Delete, from every environment:

- `data/` (the 85 GB download)
- `results/`, `logs/`
- the HF cache: `~/.cache/huggingface/hub/datasets--SageBio--mva-hackathon-2026-data`
- any copy synced to PrakashDGX_H2 or elsewhere
- the complete owner-hosted model directories on PrakashDGX_H2:
  `/home/prachh/v/mva-track2-pilot-20260920/` and
  `/home/prachh/v/mva-track2-expanded-20260920/` and
  `/home/prachh/v/mva-track2-expanded-latest-20260921/`, including inputs, outputs,
  environments, caches, logs and archives; these runs used public references and
  permitted derived candidates, never raw subject files
- any intermediate BAM/VCF outside this repo
- feat-007 recovery bundles, mirror clones and replacement maps in `results/feat007/`
- local unreachable Git objects and reflogs retained during feat-007 recovery; coordinate
  GitHub's removal of obsolete remote objects through Support before publication

Then email **RarediseaserealkidMVAhackathon2026@synapse.org** to confirm.
If not confirmed, the organizers will contact us.

The reference, VEP cache, ClinVar snapshot and HPO ontology installed by feat-003 live
under `data/resources/`, so deleting `data/` removes them with the gated dataset. Publicly
permitted tracked summaries and submission outputs may remain in Git; subject-bearing
intermediate files must remain under the local deletion targets above.
