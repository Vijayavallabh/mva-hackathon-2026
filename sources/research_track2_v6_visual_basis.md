# Source checks for the Track 2 v6 story and figures

2026-09-19. Reuses the unchanged v4 evidence ledger and v5 validation plan.
This is a bounded source check for presentation, not a new systematic search,
new experiment or candidate-ranking update. Only public sources were browsed.

## Mouse rationale

Reopened [Sieben et al.](https://www.jci.org/articles/view/126863), especially
the Figure 5 results/legend and Methods statistics paragraph. The muscle comparison
measures phospho-p70 S6 kinase and phospho-4EBP1 in different-allele mice; Figure 5C
shows two mice per genotype. Experiments were not randomized or blinded. The study
does not establish everolimus rescue. The diagram preserves these limitations and
does not invent an effect size. The
[corrigendum](https://www.jci.org/articles/view/144781) remains linked. This check
does not claim a new complete reading of all figures or supplementary experiments.

## Trial plot

Reopened the [primary indexed abstract, PMID 38936378](https://pubmed.ncbi.nlm.nih.gov/38936378/),
DOI [10.1016/S1470-2045(24)00255-9](https://doi.org/10.1016/S1470-2045(24)00255-9).
The reported ARST1431 event-free survival HR is 0.86 (95% CI 0.58-1.26), log-rank
p=0.44, among 297 evaluable participants. This randomized intermediate-risk RMS
study compared VAC/VI with versus without temsirolimus, followed by maintenance.
It did not establish an EFS benefit; the interval crossing 1 is not proof of no
effect. It does not test constitutional everolimus rescue.

The PMC route was reachable initially but a follow-up returned a browser challenge;
the PubMed query URL also failed once. The direct PMID page/indexed primary abstract
supplied the bounded check. No claim of a new full-paper review follows. Earlier
selected-section checks remain in `notes/track2-v4-primary-review.md`.

The slide plots the point and confidence interval on a logarithmic 0.5-2 axis.
For SVG x limits 80 and 1072, x = 80 + log(value/0.5)/log(4) * 992:
0.58 maps to 186.21; 0.86 to 468.08; 1 to 576; 1.26 to 741.38.
The release tests check these positions, tick labels and the exact primary DOI.
The plot redraws aggregate published values; it contains no participant records
and is not a reanalysis. A standalone Matplotlib SVG/PDF redraw is also generated
for export using the command below.

## Other figures

Slide 1 separates two objectives; slide 2 marks the unresolved transfer to the
selected-pair model; slide 4 shows proposed controlled comparisons; slide 5
requires every advancement criterion. These are schematics, not measurements.
The unchanged `notes/track2-validation-v5.md` specifies first-division outcomes,
separate daughter survival, tracking loss, exposure, replication and safety.
No engineered model is asserted to exist or to resolve the subject's phase.

## Reproduce the standalone trial graphic

Run after the local slide renderer has created the stated directory. The command
refuses existing figure outputs. It uses only the public numbers above.

```bash
uv run python - <<'PY'
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator

out = Path('results/feat009/v6-slide-review-final-20260919')
assert out.is_dir()
targets = [out / ('arst1431-published.' + suffix) for suffix in ('svg', 'pdf')]
assert not any(p.exists() for p in targets)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 14, 'svg.fonttype': 'none'})
fig, ax = plt.subplots(figsize=(12, 4.5))
fig.subplots_adjust(left=.12, right=.9, bottom=.32, top=.68)
ax.set_xscale('log')
ax.set_xlim(.5, 2)
ax.set_ylim(-.6, .6)
ax.errorbar(.86, 0, xerr=[[.86-.58], [1.26-.86]], fmt='o',
            color='#70418a', markersize=10, capsize=8, linewidth=3)
ax.axvline(1, color='#241b2d', linestyle='--', linewidth=1.5)
ax.xaxis.set_major_locator(FixedLocator([.5, 1, 2]))
ax.xaxis.set_major_formatter(FixedFormatter(['0.5', '1', '2']))
ax.xaxis.set_minor_locator(NullLocator())
ax.set_yticks([])
for side in ('left', 'top', 'right'):
    ax.spines[side].set_visible(False)
ax.set_xlabel('Event-free survival hazard ratio (logarithmic axis)', labelpad=12)
fig.suptitle('ARST1431: temsirolimus added to VAC/VI', y=.94, fontsize=19)
fig.text(.5, .8, 'HR 0.86 (95% CI 0.58-1.26); p=0.44; 297 evaluable', ha='center')
fig.text(.12, .14, 'Favours temsirolimus addition', ha='left')
fig.text(.9, .14, 'Favours control', ha='right')
fig.text(.5, .04, 'Published aggregate redraw; Gupta 2024, DOI: 10.1016/S1470-2045(24)00255-9',
         fontsize=11, ha='center')
for target in targets:
    with target.open('xb') as handle:
        fig.savefig(handle, format=target.suffix[1:])
plt.close(fig)
print('Saved public ARST1431 SVG and PDF')
PY
```
