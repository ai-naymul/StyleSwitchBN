#!/usr/bin/env python3
"""
Render report/report.md (+ references.md) to report/report.pdf with embedded
figures. Pure-Python (fpdf2), no system dependencies. Core-font safe: Unicode
punctuation is sanitized to ASCII so no TTF bundling is needed.
"""
import re
from pathlib import Path
from fpdf import FPDF

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "report" / "report.md"
REFS = ROOT / "report" / "references.md"
OUT = ROOT / "report" / "report.pdf"

_SUB = {"—": "-", "–": "-", "−": "-", "·": "*",
        "“": '"', "”": '"', "‘": "'", "’": "'",
        "…": "...", "≈": "~", "×": "x", "≥": ">=",
        "≤": "<=", " ": " ", "′": "'"}


def ascii_san(s: str) -> str:
    for k, v in _SUB.items():
        s = s.replace(k, v)
    return s.encode("latin-1", "replace").decode("latin-1")


IMG_RE = re.compile(r"^!\[(.*?)\]\((.*?)\)\s*$")


def render():
    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(18, 16, 18)
    pdf.add_page()
    cw = pdf.w - pdf.l_margin - pdf.r_margin

    lines = REPORT.read_text().splitlines()
    # append references
    lines.append("")
    for rl in REFS.read_text().splitlines():
        if rl.startswith("# "):
            continue
        lines.append(rl)

    def cell(h, txt, style="", size=10.5, md=False, align="L"):
        if md:
            txt = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"\1", txt)  # drop single-* italics
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Helvetica", style, size)
        try:
            pdf.multi_cell(cw, h, txt, markdown=md, align=align)
        except Exception:
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(cw, h, txt, markdown=False, align=align)

    for raw in lines:
        line = ascii_san(raw.rstrip())
        if not line:
            pdf.ln(2.5)
            continue
        m = IMG_RE.match(raw.strip())
        if m:
            caption, path = m.group(1), m.group(2)
            img = (ROOT / "report" / path).resolve()
            if img.exists():
                pdf.ln(1)
                w = min(cw, 165)
                x = pdf.l_margin + (cw - w) / 2
                pdf.image(str(img), x=x, w=w)
                pdf.ln(1)
                cell(4.2, ascii_san(caption), style="I", size=8.5, align="C")
                pdf.ln(2)
            continue
        if line.startswith("# "):
            cell(7.5, line[2:], style="B", size=16); pdf.ln(1)
        elif line.startswith("## "):
            pdf.ln(1.5); cell(6, line[3:], style="B", size=12.5); pdf.ln(0.5)
        elif line.startswith("### "):
            cell(5.5, line[4:], style="B", size=11)
        elif line.startswith("- "):
            cell(5, "  -  " + line[2:], md=True)
        elif re.match(r"^\d+\.\s", line):
            cell(5, line, md=True)
        else:
            cell(5, line, md=True)

    pdf.output(str(OUT))
    print(f"wrote {OUT}  ({OUT.stat().st_size//1024} KB, {pdf.page_no()} pages)")


if __name__ == "__main__":
    render()
