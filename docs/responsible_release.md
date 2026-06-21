# Responsible Release

## Purpose

StyleSwitch-BN is a safety-evaluation artifact. Its goal is to surface and help mitigate a deployment risk — that LLM safety behavior can change with ordinary Bengali writing style — so that builders can test and fix it. It is not a jailbreak toolkit.

## What we release

- Aggregate safety **labels** (per response: one of four safety categories).
- Recomputed aggregate **metrics** (rates, confidence intervals, a robustness leaderboard).
- **Figures** derived from the aggregates.
- **Abstract example summaries** that describe outcomes only.
- **Analysis code** that runs on the released labels.

## What we deliberately do NOT release

- Raw prompts.
- Raw model completions.
- Any operational harmful detail.
- Per-response text of any kind.

## Why aggregate-only

The phenomenon we document — that a legitimate-sounding writing style can draw partial engagement with a harmful request — is itself sensitive. Publishing the prompts or completions could lower the cost of misuse. Aggregate labels and redacted summaries convey the finding and support reproducibility without distributing harmful content. We therefore do not publish the underlying prompts or completions.

## Crisis-response safety

The crisis-response-safety category is included in aggregate metrics only. No examples — abstract or otherwise — are shown for it.

## Contact

Issues or takedown requests: raise via the hackathon submission channel.
