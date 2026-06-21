# StyleSwitch-BN: Auditing Bengali LLM Safety Across Real-World Writing Styles

A weekend pilot for the **Global South AI Safety Hackathon (Asia Track — Technical Safety / Multilingual Models)**.

## What this is

A small, reproducible audit of whether LLM safety behavior is stable across the ordinary writing styles a Bengali user actually uses — formal news-style Bengali, casual Bengali/English code-mixing ("Banglish"), and institutional Bengali — holding the underlying request fixed.

## Why it matters

Multilingual safety benchmarks mostly test one clean translation per language. Real South-Asian users write across many styles. We find safety behavior is **not invariant** to style: the same intent written as a formal news investigation reaches a **61.0%** unsafe-engagement rate vs **44.6%** as a casual peer message — a **16.4-point style-conditioned safety gap** (95% CI [9.4, 23.2]) from writing style alone, no adversarial prompting. A model can pass a clean-translation benchmark and still partially engage with the same intent in a different everyday style. That is a deployment risk translation benchmarks miss.

## Reproduce the headline numbers (one command)

```bash
pip install -r requirements.txt
python src/compute_metrics.py
```

This recomputes every number in the report from `data/public_labels.csv` (labels only) and prints a **REPORT HEADLINE NUMBERS** block that maps 1:1 to the report's Abstract and Section 4 — overall UER/DCR, per-style UER, the style-conditioned safety gap with 95% CI \[lo, hi\], and the most/least style-robust models. No API calls, no GPU, runs in seconds. Full per-cell results are written to `results/*.csv`.

### Optional: regenerate the figures and the PDF

```bash
python src/make_figures.py        # charts -> figures/
python src/render_report.py       # report/report.pdf
```

## Run the dashboard (optional)

```bash
streamlit run app/streamlit_app.py
```

## What's included

```
data/      public_labels.csv (labels only) · public_metadata.csv · redacted_examples.csv
results/   aggregate_results.csv · style_gap_summary.csv · model_robustness_leaderboard.csv
figures/   uer_by_style.png · label_distribution.png · style_gap_table.png · leaderboard.png
src/       compute_metrics.py · make_figures.py · render_report.py
report/    report.md · report.pdf · references.md
docs/      responsible_release.md
app/       streamlit_app.py
```

## What is intentionally redacted

This repository contains **no raw harmful prompts and no model completions.** The public data is aggregate safety **labels** plus abstract one-line example summaries (none for the crisis-response-safety category). We do not publish the underlying prompts or completions, as a responsible-disclosure measure. See `docs/responsible_release.md`.

## Responsible use

This artifact exists to **evaluate and help mitigate** style-conditioned safety failures, not to enable them. It reports only aggregate outcomes and redacted summaries. Do not attempt to reconstruct operational content from it.

## Metrics

- **Unsafe Engagement Rate (UER)** = (partial unsafe + direct unsafe) / N
- **Direct Compliance Rate (DCR)** = direct unsafe / N
- **Style-Conditioned Safety Gap** = UER(news-style) − UER(casual code-mixed)
- **Style Robustness Risk Score** (leaderboard) = 0.5·UER + 0.3·|news−casual gap| + 0.2·DCR (lower = more style-robust)

## Limitations

Small curated pilot, single labeling source, narrow model + harm-category slice, correlational with respect to style. See the report's Limitations section.
