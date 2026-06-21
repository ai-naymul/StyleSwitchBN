#!/usr/bin/env python3
"""
StyleSwitch-BN research dashboard. Reads the public aggregate CSVs + figures.
No raw prompts or completions. Run:  streamlit run app/streamlit_app.py
"""
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "results"
D = ROOT / "data"
F = ROOT / "figures"

st.set_page_config(page_title="StyleSwitch-BN", layout="wide")

st.title("StyleSwitch-BN")
st.subheader("Auditing Bengali LLM safety across real-world writing styles")
st.markdown(
    "**Thesis:** LLM safety behavior changes across ordinary Bengali writing styles, "
    "so clean-translation safety benchmarks miss South Asian deployment risks."
)

agg = pd.read_csv(R / "aggregate_results.csv")
gap = pd.read_csv(R / "style_gap_summary.csv").iloc[0]
lb = pd.read_csv(R / "model_robustness_leaderboard.csv")
meta = pd.read_csv(D / "public_metadata.csv")
overall = agg[agg["scope"] == "overall"].iloc[0]

def style_uer(name):
    row = agg[agg["scope"] == f"style:{name}"]
    return float(row["uer"].iloc[0]) if len(row) else float("nan")

total_n = int(meta[meta["dimension"] == "total"]["n_responses"].iloc[0])
n_models = int((meta["dimension"] == "model").sum())
n_cats = int((meta["dimension"] == "harm_category").sum())

c1, c2, c3, c4 = st.columns(4)
c1.metric("Labeled responses", f"{total_n:,}")
c2.metric("Models", n_models)
c3.metric("Harm categories", n_cats)
c4.metric("Writing conditions", 4)

st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("Riskiest style (News-style) UER", f"{style_uer('News-style Bengali')*100:.1f}%")
c2.metric("Safest style (Casual) UER", f"{style_uer('Casual code-mixed Bengali')*100:.1f}%")
c3.metric("Style-conditioned safety gap",
          f"{gap['style_conditioned_safety_gap']*100:+.1f} pp")
st.caption(f"Style gap 95% confidence interval: "
           f"[{gap['gap_ci_lo']*100:.1f}, {gap['gap_ci_hi']*100:.1f}] points.")

st.divider()
left, right = st.columns(2)
with left:
    st.markdown("#### Unsafe engagement by writing style")
    st.image(str(F / "uer_by_style.png"))
with right:
    st.markdown("#### Safety-label distribution by style")
    st.image(str(F / "label_distribution.png"))

st.divider()
st.markdown("#### Pilot Model Robustness Leaderboard")
st.caption("Robustness under Bengali writing-style variation. Lower risk score = more style-robust. "
           "This is **not** a general model safety ranking; it is a pilot ranking for style robustness on a redacted Bengali subset.")
st.dataframe(lb, use_container_width=True, hide_index=True)

st.divider()
st.markdown("#### Redacted example outcomes (same intent, different style)")
ex_path = D / "redacted_examples.csv"
if ex_path.exists():
    ex = pd.read_csv(ex_path)
    for _, e in ex.iterrows():
        st.markdown(
            f"**{e['harm_area']}** — {e['style_news']} → *{e['outcome_news']}*; "
            f"{e['style_casual']} → *{e['outcome_casual']}*.  \n{e['summary']}"
        )

st.divider()
st.info(
    "Responsible release: this dashboard shows aggregate labels and redacted summaries only. "
    "No raw prompts or model completions are included; the underlying prompts and completions are not published."
)
