#!/usr/bin/env python3
"""Build a concise PDF report from the checked summary figures."""

from __future__ import annotations

import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image

from generate_figures import generate_figures
from validate_metrics import load_metrics, validate_metrics


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
REPORTS = ROOT / "reports"
REPORT = REPORTS / "final_report.pdf"
INK = "#17212B"
MUTED = "#5C6770"
BLUE = "#16324F"
TEAL = "#2A9D8F"
GOLD = "#E9C46A"


def _footer(fig: plt.Figure, page_number: int) -> None:
    fig.text(
        0.08,
        0.035,
        "Nanopore adapter screening · Aggregate values transcribed from supplied project documents",
        fontsize=7,
        color=MUTED,
    )
    fig.text(0.92, 0.035, f"{page_number}", ha="right", fontsize=8, color=MUTED)


def _new_page(title: str, subtitle: str | None = None) -> tuple[plt.Figure, plt.Axes]:
    fig = plt.figure(figsize=(8.27, 11.69), facecolor="white")
    ax = fig.add_axes([0.08, 0.08, 0.84, 0.84])
    ax.axis("off")
    fig.text(0.08, 0.94, title, fontsize=20, fontweight="bold", color=INK, va="top")
    if subtitle:
        fig.text(0.08, 0.90, subtitle, fontsize=10, color=MUTED, va="top")
    return fig, ax


def _text_page(pdf: PdfPages, page_number: int, title: str, sections: list[tuple[str, str]]) -> None:
    fig, _ = _new_page(title)
    y = 0.875
    for heading, body in sections:
        fig.text(0.08, y, heading, fontsize=12, fontweight="bold", color=BLUE, va="top")
        y -= 0.032
        wrapped = textwrap.fill(body, width=96)
        for line in wrapped.splitlines():
            fig.text(0.08, y, line, fontsize=9, color=INK, va="top")
            y -= 0.021
        y -= 0.022
    _footer(fig, page_number)
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def generate_report() -> Path:
    generate_figures()
    metrics = load_metrics()
    derived = validate_metrics(metrics)
    REPORTS.mkdir(parents=True, exist_ok=True)

    with PdfPages(REPORT) as pdf:
        # Page 1: cover and executive summary.
        fig = plt.figure(figsize=(8.27, 11.69), facecolor="white")
        fig.text(0.08, 0.91, "PROJECT REPORT", fontsize=10, color=TEAL, fontweight="bold")
        fig.text(
            0.08,
            0.84,
            "Detection and removal of\nadapter-contaminated reads",
            fontsize=25,
            color=INK,
            fontweight="bold",
            va="top",
            linespacing=1.15,
        )
        fig.text(
            0.08,
            0.71,
            "Oxford Nanopore sequencing · Summary reconstructed from supplied project documents",
            fontsize=11,
            color=MUTED,
        )
        cards = [
            ("215,176", "reads processed"),
            ("61,495", "reads passed · 28.6%"),
            ("38.10 M", "bases retained · 27.4%"),
        ]
        x_positions = [0.08, 0.37, 0.66]
        for x, (value, label) in zip(x_positions, cards):
            fig.text(x, 0.59, value, fontsize=19, color=BLUE, fontweight="bold")
            fig.text(x, 0.55, label, fontsize=8.5, color=MUTED)
            fig.add_artist(
                plt.Line2D([x, x + 0.24], [0.53, 0.53], transform=fig.transFigure, color=GOLD, linewidth=3)
            )
        fig.text(0.08, 0.45, "Executive summary", fontsize=14, fontweight="bold", color=BLUE)
        summary = (
            "The source report states that Cutadapt processed 215,176 reads, discarded 153,681 "
            "reads as trimmed, and retained 61,495 reads. The presentation includes six adapter-match "
            "length plots. Their numeric point tables and the raw FASTQ/POD5 inputs were not supplied, "
            "so this package reproduces the aggregate summary and preserves the source plots without "
            "digitizing them."
        )
        fig.text(0.08, 0.415, textwrap.fill(summary, width=96), fontsize=10, color=INK, va="top", linespacing=1.5)
        fig.text(0.08, 0.26, "Scope statement", fontsize=12, fontweight="bold", color=BLUE)
        scope = (
            "This is a reported-results summary, not an independent re-analysis or a validated "
            "read-level chimera classification. The documented --discard-trimmed option filters "
            "reads with configured matches; it does not split chimeric reads."
        )
        fig.text(0.08, 0.225, textwrap.fill(scope, width=96), fontsize=9.5, color=INK, va="top", linespacing=1.5)
        fig.text(0.08, 0.10, "Source: NGSproject report pp. 7–18; final presentation slides 12–19.", fontsize=8, color=MUTED)
        _footer(fig, 1)
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        # Page 2: exact aggregate figures.
        fig = plt.figure(figsize=(8.27, 11.69), facecolor="white")
        fig.text(0.08, 0.94, "Reported filtering outcomes", fontsize=20, fontweight="bold", color=INK, va="top")
        fig.text(0.08, 0.90, "Both charts use only values transcribed from the source summary.", fontsize=10, color=MUTED)
        for ypos, filename, height in [
            (0.55, "figure_01_read_filtering.png", 0.25),
            (0.18, "figure_02_base_pair_retention.png", 0.25),
        ]:
            ax = fig.add_axes([0.08, ypos, 0.84, height])
            ax.imshow(Image.open(FIGURES / filename).convert("RGB"))
            ax.axis("off")
        fig.text(
            0.08,
            0.10,
            f"Derived from reported totals: {derived['bases_removed']:,.0f} bp were not retained.",
            fontsize=8.5,
            color=MUTED,
        )
        _footer(fig, 2)
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        # Page 3: adapter plot sources.
        fig = plt.figure(figsize=(8.27, 11.69), facecolor="white")
        fig.text(0.08, 0.94, "Adapter-match distributions", fontsize=20, fontweight="bold", color=INK, va="top")
        fig.text(
            0.08,
            0.90,
            "Six source plots from the presentation; not redrawn from point-level data.",
            fontsize=10,
            color=MUTED,
        )
        ax = fig.add_axes([0.055, 0.16, 0.89, 0.69])
        ax.imshow(Image.open(FIGURES / "figure_04_source_adapter_distributions.png").convert("RGB"))
        ax.axis("off")
        fig.text(
            0.08,
            0.10,
            "Longer match-length patterns are interpreted in the source report as possible internal matches; "
            "read-level coordinates are needed to verify that interpretation.",
            fontsize=8.5,
            color=MUTED,
            wrap=True,
        )
        _footer(fig, 3)
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        _text_page(
            pdf,
            4,
            "Methods and interpretation",
            [
                (
                    "Workflow as reported",
                    "The project report states that MinKNOW high-accuracy basecalling was performed with "
                    "adapter and barcode trimming disabled. The resulting FASTQ files were combined and "
                    "processed with Cutadapt using six 5-prime/3-prime adapter models, reverse-complement "
                    "handling, and --discard-trimmed.",
                ),
                (
                    "What the filter means",
                    "The reported option discards reads that are trimmed against configured adapters and "
                    "writes reads without a detected configured match. It is not equivalent to splitting "
                    "a concatenated read into valid fragments, and it does not by itself classify a read "
                    "as a PCR chimera.",
                ),
                (
                    "What the plots show",
                    "The supplied slides show adapter-match length/count patterns. Per-adapter trim "
                    "occurrences are transcribed where visible in the source log snapshots. Such counts "
                    "may overlap across adapters and are not unique-read counts. The point tables and "
                    "match positions were not supplied.",
                ),
                (
                    "Evidence-based conclusion",
                    "The documented output supports a high rate of reads removed by the configured "
                    "sequence-matching filter. The source report proposes internal adapters, concatenation, "
                    "and PCR chimeras as explanations; those hypotheses require read-level sequence or "
                    "alignment evidence before they can be confirmed.",
                ),
            ],
        )

        _text_page(
            pdf,
            5,
            "Associated laboratory context",
            [
                (
                    "Separate evidence stream",
                    "A separate workflow document records extraction, gel electrophoresis, PCR, DNA "
                    "quantification, and Nanopore library-preparation steps. The supplied files do not "
                    "link these observations to the FASTQ dataset summarized in the NGS report.",
                ),
                (
                    "Reported QC concerns",
                    "The workflow notes describe an early gel run with a maximum voltage of 33 V and poor "
                    "separation, an unexpected band in the T1 no-template PCR control, uncertain "
                    "quantification calculations, and no visible DNA bands on the final library gel.",
                ),
                (
                    "Interpretation boundary",
                    "These are statements from the laboratory record, not independent validation. They "
                    "should not be used to explain the Nanopore read-filtering totals until sample IDs and "
                    "run provenance are linked. The source document lists possible causes but does not "
                    "resolve them.",
                ),
                (
                    "Public repository contents",
                    "The source PDFs and extracted text transcripts are intentionally omitted from this "
                    "public repository. The included report, figures, CSVs, and scripts are the project "
                    "deliverables selected for publication.",
                ),
            ],
        )

        _text_page(
            pdf,
            6,
            "Reproducibility and next steps",
            [
                (
                    "Reproduce the summary package",
                    "Install requirements.txt, then run scripts/validate_metrics.py, "
                    "scripts/generate_figures.py, scripts/generate_report.py, and "
                    "python -m unittest discover -s tests -v. These steps validate and visualize "
                    "transcribed aggregate values; they do not re-run the original read analysis.",
                ),
                (
                    "Run the documented filter",
                    "Provide the original FASTQ and run scripts/run_documented_cutadapt.sh. Save the "
                    "Cutadapt version, JSON report, full log, and sample manifest so that the reported "
                    "counts can be reconciled.",
                ),
                (
                    "Complete chimera validation",
                    "Export numeric adapter-match data and coordinates, predefine read-level criteria, "
                    "and apply an amplicon-appropriate chimera classifier or split-read alignment. Then "
                    "compare mapping or assembly metrics before and after filtering.",
                ),
                (
                    "Inputs still needed",
                    "Raw FASTQ/POD5 reads, full Cutadapt log or JSON, the numeric distribution data, "
                    "a reference/amplicon description, and sample IDs that connect wet-lab QC to "
                    "sequencing records.",
                ),
            ],
        )

    print(f"Wrote {REPORT}")
    return REPORT


if __name__ == "__main__":
    generate_report()
