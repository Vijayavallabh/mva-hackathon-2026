# Vendored Track 1 scorer

`evaluation.py` is an unmodified copy of the organizers' public Track 1 scorer at
Hugging Face Space revision `1c761cc23d90aebe6a011fd5b0b99517df42408c`, fetched
2026-09-03. `../track1_submission_template.csv` is the submission template from the
same revision.

Checksums:

- `evaluation.py` (official and tracked):
  `6d18b581e65a45e1ccc120071d588e740c2e42e983ff50704c60a40232b19180`
- official template bytes (CRLF):
  `7b3ed41c091d34fb6c5622d049c7a3f46124211fc7ec02947e69daef8752755a`
- tracked template after line-ending normalization (LF):
  `0c9cc378c6f8025b7fd538c37fd0331bff5a9f7dd53fd2e9ccbfe2a2da659643`

Source:
`https://huggingface.co/spaces/SageBio/rare-disease-real-kid-mva-hackathon-2026/tree/1c761cc23d90aebe6a011fd5b0b99517df42408c`

Do not add local validation behavior to this file. Put stricter checks in the wrapper so
the upstream scoring behavior remains auditable byte-for-byte.
