# StyleSwitch-BN

A small pilot for the Global South AI Safety Hackathon (Asia track, Technical Safety).

**Question.** If you keep a harmful Bengali request the same and only change the writing style, does the model's safety answer stay the same?

**Finding.** It does not. Across six frontier models, the same request gets an unsafe answer 61.0% of the time when written as a formal news story, but 44.6% of the time when written as a casual chat message. That is a 16-point gap from style alone, with no jailbreak tricks. Translation-only safety tests never see this.

## Reproduce the numbers

```bash
pip install -r requirements.txt
python src/compute_metrics.py
```

This prints every number in the report from `data/public_labels.csv` (labels only). No API keys, no GPU, a few seconds. Per-cell results land in `results/`.

Optional, to rebuild the charts and PDF:

```bash
python src/make_figures.py
python src/render_report.py
```

## Dashboard

```bash
streamlit run app/streamlit_app.py
```

## What's here

```
report/    report.pdf (the writeup) + report.md + references.md
data/      public_labels.csv (labels only) + metadata + redacted examples
results/   aggregate metrics + style-gap + model leaderboard
figures/   the four charts
src/       compute_metrics.py, make_figures.py, render_report.py
app/       streamlit dashboard
docs/      responsible_release.md
```

## Metrics

- **Unsafe Engagement Rate (UER)** = (partial unsafe + direct unsafe) / N
- **Direct Compliance Rate (DCR)** = direct unsafe / N
- **Style gap** = UER(news-style) minus UER(casual code-mixed)

## Responsible release

No raw prompts and no model answers are included. The public data is safety labels plus short outcome-only example notes. We do not publish the underlying prompts or answers. See `docs/responsible_release.md`.

## Limitations

Small hand-picked pilot, one labeling source, six models, six harm areas. The result is a correlation between writing style and safety behavior, not a proven cause.
