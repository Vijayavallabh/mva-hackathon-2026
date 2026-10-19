"""Derive planned recording metrics from narration; never infer actual runtime."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def parse(pitch):
    spoken = pitch.split('## Narration\n')[1].split('## Recording notes')[0]
    rows = re.findall(r'### Slide ([^\n]+)\n\n(.*?)(?=\n\n###|\Z)', spoken.strip(), re.S)
    cues = []
    for number, (head, body) in enumerate(rows, 1):
        match = re.fullmatch(r'(\d+) / (\d+):([0-5]\d)-(\d+):([0-5]\d) / (.+)', head)
        if not match or int(match[1]) != number:
            raise ValueError('Narration slide order or cue format differs')
        start, end = 60*int(match[2])+int(match[3]), 60*int(match[4])+int(match[5])
        if start != (cues[-1]['end'] if cues else 0) or end <= start:
            raise ValueError('Noncontiguous timing or nonpositive cue duration')
        cues.append(dict(slide=number, start=start, end=end, title=match[6],
                         head=head, body=body.strip(), words=len(body.split())))
    if len(cues) != 9 or cues[-1]['end'] != 180:
        raise ValueError('Nine cues totaling 180 allocated seconds required')
    return cues


def summary(pitch):
    cues = parse(pitch)
    words = sum(c['words'] for c in cues)
    return dict(schema_version=40, narration_words=words, allocation_seconds=180,
                planned_words_per_minute=round(words/3, 1),
                cues=[dict(slide=c['slide'], start=c['start'], end=c['end'], words=c['words'],
                           planned_words_per_minute=round(c['words']*60/(c['end']-c['start']), 1)) for c in cues],
                runtime_measured=False, video_recorded=False)


def guide_metrics(pitch):
    stats = summary(pitch)
    lines = [f"The {stats['narration_words']}-word script allocates 180 seconds: "
             f"{stats['planned_words_per_minute']:.1f} words per minute overall.",
             'These are planned rates, not measured speech or video runtime.', '',
             '| Slide | Words | Allocated seconds | Planned words/min |',
             '|---|---:|---:|---:|']
    lines += [f"| {c['slide']} | {c['words']} | {c['end']-c['start']} | {c['planned_words_per_minute']:.1f} |" for c in stats['cues']]
    return '\n'.join(lines)


if __name__ == '__main__':
    print(json.dumps(summary((ROOT/'notes/track2-pitch-v40.md').read_text()), indent=2))
