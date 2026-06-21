#!/usr/bin/env python3
"""
StyleSwitch-BN — figures from the public results CSVs. No raw text, public-safe
labels only. Outputs PNGs into figures/.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGS = ROOT / "figures"

STYLE_ORDER = ["English baseline", "News-style Bengali",
               "Casual code-mixed Bengali", "Institutional-style Bengali"]
SHORT = {"English baseline": "English\nbaseline",
         "News-style Bengali": "News-style\nBengali",
         "Casual code-mixed Bengali": "Casual\ncode-mixed",
         "Institutional-style Bengali": "Institutional\nBengali"}
# colourblind-safe (Okabe-Ito)
C_REFUSE, C_POLICY, C_PARTIAL, C_DIRECT = "#0072B2", "#56B4E9", "#E69F00", "#D55E00"
C_BAR = "#0072B2"
C_NEWS, C_CASUAL = "#D55E00", "#009E73"
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})


def load_agg():
    a = pd.read_csv(RESULTS / "aggregate_results.csv")
    a["style"] = a["scope"].str.replace("style:", "", regex=False)
    return a


def fig_uer_by_style():
    a = load_agg()
    rows = [a[a["style"] == s].iloc[0] for s in STYLE_ORDER]
    uer = [r["uer"] * 100 for r in rows]
    lo = [(r["uer"] - r["uer_ci_lo"]) * 100 for r in rows]
    hi = [(r["uer_ci_hi"] - r["uer"]) * 100 for r in rows]
    colors = [C_CASUAL if s == "Casual code-mixed Bengali"
              else (C_NEWS if s == "News-style Bengali" else C_BAR) for s in STYLE_ORDER]
    fig, ax = plt.subplots(figsize=(7.2, 4.3))
    x = range(len(STYLE_ORDER))
    bars = ax.bar(x, uer, yerr=[lo, hi], capsize=5, color=colors, edgecolor="black", linewidth=0.6)
    for i, v in enumerate(uer):
        ax.text(i, v + max(hi) + 1.5, f"{v:.1f}%", ha="center", fontweight="bold")
    ax.set_xticks(list(x)); ax.set_xticklabels([SHORT[s] for s in STYLE_ORDER])
    ax.set_ylabel("Unsafe Engagement Rate (%)")
    ax.set_ylim(0, max(uer) + 14)
    ax.set_title("Unsafe Engagement Rate by Bengali writing style\n(same intent; 95% bootstrap CI)", fontsize=12)
    fig.tight_layout(); fig.savefig(FIGS / "uer_by_style.png", dpi=200); plt.close(fig)


def fig_label_distribution():
    a = load_agg()
    rows = [a[a["style"] == s].iloc[0] for s in STYLE_ORDER]
    ref = [r["pct_safe_refusal"] * 100 for r in rows]
    pol = [r["pct_safe_policy"] * 100 for r in rows]
    par = [r["pct_partial_unsafe"] * 100 for r in rows]
    ddirect = [r["pct_direct_unsafe"] * 100 for r in rows]
    fig, ax = plt.subplots(figsize=(7.2, 4.5))
    x = range(len(STYLE_ORDER)); b = [0] * len(STYLE_ORDER)
    for vals, c, lab in [(ref, C_REFUSE, "safe refusal"),
                         (pol, C_POLICY, "safe policy guidance"),
                         (par, C_PARTIAL, "partial unsafe engagement"),
                         (ddirect, C_DIRECT, "direct unsafe compliance")]:
        ax.bar(x, vals, bottom=b, color=c, label=lab, edgecolor="white", linewidth=0.5)
        b = [bi + vi for bi, vi in zip(b, vals)]
    ax.set_xticks(list(x)); ax.set_xticklabels([SHORT[s] for s in STYLE_ORDER])
    ax.set_ylabel("Share of responses (%)"); ax.set_ylim(0, 100)
    ax.set_title("Safety-label distribution by writing style", fontsize=12)
    ax.legend(ncol=2, fontsize=9, loc="lower center", bbox_to_anchor=(0.5, -0.32), frameon=False)
    fig.tight_layout(); fig.savefig(FIGS / "label_distribution.png", dpi=200, bbox_inches="tight"); plt.close(fig)


def fig_style_gap_table():
    a = load_agg()
    rows = [a[a["style"] == s].iloc[0] for s in STYLE_ORDER]
    cell = [[s, f"{r['n']}", f"{r['uer']*100:.1f}%", f"{r['dcr']*100:.1f}%"]
            for s, r in zip(STYLE_ORDER, rows)]
    gap = pd.read_csv(RESULTS / "style_gap_summary.csv").iloc[0]
    fig, ax = plt.subplots(figsize=(9.6, 3.0)); ax.axis("off")
    t = ax.table(cellText=cell,
                 colLabels=["Writing style", "N", "Unsafe Eng.\nRate", "Direct\nCompliance"],
                 cellLoc="center", loc="center",
                 colWidths=[0.40, 0.10, 0.25, 0.25])
    t.auto_set_font_size(False); t.set_fontsize(9.5); t.scale(1, 1.9)
    for (r, c), cellobj in t.get_celld().items():
        if r == 0:
            cellobj.set_facecolor("#0072B2"); cellobj.set_text_props(color="white", fontweight="bold")
    ax.set_title("Per-style safety summary", fontsize=12, pad=14)
    cap = (f"Style-conditioned safety gap (News-style − Casual code-mixed): "
           f"{gap['style_conditioned_safety_gap']*100:+.1f} pp "
           f"[{gap['gap_ci_lo']*100:.1f}, {gap['gap_ci_hi']*100:.1f}]")
    fig.text(0.5, 0.04, cap, ha="center", fontsize=10, fontstyle="italic")
    fig.savefig(FIGS / "style_gap_table.png", dpi=200, bbox_inches="tight"); plt.close(fig)


def fig_leaderboard():
    lb = pd.read_csv(RESULTS / "model_robustness_leaderboard.csv")
    cell = [[r["model"], f"{r['overall_UER']*100:.0f}%", f"{r['news_style_UER']*100:.0f}%",
             f"{r['casual_codemixed_UER']*100:.0f}%", f"{r['style_conditioned_safety_gap']*100:+.0f}",
             f"{r['Direct_Compliance_Rate']*100:.0f}%", f"{r['Style_Robustness_Risk_Score']:.3f}"]
            for _, r in lb.iterrows()]
    fig, ax = plt.subplots(figsize=(9.2, 3.0)); ax.axis("off")
    t = ax.table(cellText=cell,
                 colLabels=["Model", "UER", "News", "Casual", "Gap pp", "DCR", "Risk score"],
                 cellLoc="center", loc="center",
                 colWidths=[0.26, 0.10, 0.10, 0.11, 0.11, 0.10, 0.15])
    t.auto_set_font_size(False); t.set_fontsize(9.5); t.scale(1, 1.6)
    for (r, c), cellobj in t.get_celld().items():
        if r == 0:
            cellobj.set_facecolor("#444"); cellobj.set_text_props(color="white", fontweight="bold")
        elif c == 6 and r == 1:
            cellobj.set_facecolor("#d9f0e3")  # most robust
    ax.set_title("Pilot Model Robustness Leaderboard\n(robustness under Bengali writing-style variation; lower risk = more robust)", fontsize=11, pad=12)
    fig.text(0.5, 0.02, "Not a general model safety ranking; pilot ranking for style robustness on a redacted Bengali subset.",
             ha="center", fontsize=8.5, fontstyle="italic")
    fig.savefig(FIGS / "leaderboard.png", dpi=200, bbox_inches="tight"); plt.close(fig)


def main():
    FIGS.mkdir(parents=True, exist_ok=True)
    fig_uer_by_style()
    fig_label_distribution()
    fig_style_gap_table()
    fig_leaderboard()
    print("wrote:", ", ".join(p.name for p in sorted(FIGS.glob("*.png"))))


if __name__ == "__main__":
    main()
