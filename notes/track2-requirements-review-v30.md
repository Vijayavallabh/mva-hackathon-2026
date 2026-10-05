# Track 2 official refresh, 6 October 2026

Anonymous GETs checked the running app, public source revision
`c9b4a7e6247574124cd5bbfd249af9af6f1bbac3`, rules, FAQ, Track 2 instructions,
configuration and methods workbook. Downloaded Python was parsed as data, never
executed. Live rules and submission instructions match their source strings.
Compared with September 24, the inspected requirement files and workbook are unchanged
except for the About-page judging schedule. This is an author review, not an
independent, organizer, clinical or legal assessment.

The [About page](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/blob/c9b4a7e6247574124cd5bbfd249af9af6f1bbac3/tabs/about.py)
and [announcement 26](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/26)
extend judging to December 17 and place the winner announcement on December 18.
The October 24 submission deadline remains unchanged. This does not extend the
repository's November 24 deletion deadline.

The complete listing has 26 public discussions, 14 closed, with 79 latest visible
comments. Every comment was compared with the earlier archive; twelve new/edited
comments were reread. The prior review covers unchanged text and three administrative
images. Hidden/deleted content and edit history were not reviewed.

- [Discussion 2](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/2):
  the latest organizer correction permits consumer tiers under the stated training
  opt-out, no-feedback and safety-review conditions, superseding an earlier reply
  preferring Business/API. Record provider, tier and settings accurately. This does
  not verify this project's accounts or relax its raw-data prohibition.
- [Discussion 24](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/24):
  organizers will not confirm candidate-specific transmission/phase during the
  challenge. Trans remains unconfirmed; no private clarification is assumed.
- [Discussion 25](https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/discussions/25):
  organizers describe FASTQ-only access, GRCh38, PCR-free Illumina preparation and
  NovaSeq sequencing; lane/library and fragment details remain unconfirmed. This
  does not alter established local measurements or trigger a new alignment.
- Discussion 20 refers an incidental-findings question to governance; no general
  disclosure exemption or permission to contact the family follows. Discussion 27
  concerns another team's administrative receipt and changes no quota assumption here.

The 35/25/25/15 rubric, PDF/Markdown report, GitHub URL, three-minute YouTube/Vimeo
pitch, three entries/latest-only rule, B9 disclosure and B17 500-word limit remain.
The workbook's one-entry wording is still stale. Quota was not queried; no callback,
login, message, submission or contact occurred. Provider and distribution questions
remain unresolved; preserve historical notices and public-first policy.

Reproduce the public captures with new output directories:

```bash
uv run python scripts/track2_challenge_review.py results/feat009/new-official-review
uv run python scripts/track2_community_review_v17.py results/feat009/new-community-review
```

This cycle's captures are `results/feat009/v30-official-20261006/` and
`v30-community-20261006/`. The versioned requirements/community JSON records URLs,
hashes, coverage and reading depth. No earlier review was overwritten.
