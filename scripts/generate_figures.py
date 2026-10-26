#!/usr/bin/env python3
"""Generate transparent figures from the reported summary metrics.

The six adapter-length plots in figures/source_adapter_distributions are source
images and are intentionally not digitized because their numeric series were
not supplied.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIGURES = ROOT / "figures"
SOURCE_FIGURES = FIGURES / "source_adapter_distributions"

COLORS = {
    "navy": "#16324F",
    "blue": "#2A6F97",
    "teal": "#2A9D8F",
    "gold": "#E9C46A",
    "orange": "#F4A261",
    "red": "#C8553D",
    "ink": "#17212B",
    "muted": "#5C6770",
    "grid": "#DDE4EA",
    "paper": "#FFFFFF",
}


def _read_metrics() -> dict[str, float]:
    with (DATA / "reported_metrics.csv").open(newline="", encoding="utf-8") as handle:
        rows = csv.DictReader(handle)
        return {row["metric"]: float(row["value"]) for row in rows}


def _save(fig: plt.Figure, stem: str) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES / f"{stem}.png", dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(FIGURES / f"{stem}.pdf", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def _setup_axis(ax: plt.Axes) -> None:
    ax.set_facecolor("white")
    ax.grid(axis="x", color=COLORS["grid"], linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(COLORS["grid"])
    ax.spines["bottom"].set_color(COLORS["grid"])
    ax.tick_params(colors=COLORS["muted"], labelsize=9)


def _stacked_retention_figure(
    *,
    title: str,
    total: int,
    retained: int,
    retained_label: str,
    removed_label: str,
    stem: str,
) -> None:
    removed = total - retained
    retained_pct = retained / total * 100
    removed_pct = removed / total * 100

    fig, ax = plt.subplots(figsize=(9, 3.8))
    fig.subplots_adjust(left=0.12, right=0.97, top=0.76, bottom=0.27)
    fig.suptitle(title, x=0.12, y=0.94, ha="left", fontsize=16, fontweight="bold", color=COLORS["ink"])
    ax.barh(0, removed_pct, color=COLORS["navy"], height=0.48, label=removed_label)
    ax.barh(0, retained_pct, left=removed_pct, color=COLORS["teal"], height=0.48, label=retained_label)
    ax.text(
        removed_pct / 2,
        0,
        f"{removed_label}\n{removed:,}  ·  {removed_pct:.1f}%",
        ha="center",
        va="center",
        color="white",
        fontsize=10,
        fontweight="bold",
    )
    ax.text(
        removed_pct + retained_pct / 2,
        0,
        f"{retained_label}\n{retained:,}  ·  {retained_pct:.1f}%",
        ha="center",
        va="center",
        color="white",
        fontsize=9,
        fontweight="bold",
    )
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.7, 0.7)
    ax.set_yticks([])
    ax.set_xlabel("Share of total (%)", color=COLORS["muted"])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.0f}%"))
    _setup_axis(ax)
    ax.set_title(f"Reported total: {total:,}", loc="left", fontsize=10, color=COLORS["muted"], pad=12)
    fig.text(
        0.12,
        0.08,
        "Source-reported aggregate; not independently recalculated from raw reads.",
        fontsize=8,
        color=COLORS["muted"],
    )
    _save(fig, stem)


def _adapter_event_figure(metrics: dict[str, float]) -> None:
    labels: list[str] = []
    counts: list[int] = []
    with (DATA / "adapter_event_counts.csv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            value = row["trimmed_occurrences"]
            if value == "NA":
                continue
            labels.append(f'{row["adapter_id"]}  {row["label"]}')
            counts.append(int(value))

    fig, ax = plt.subplots(figsize=(9, 5.2))
    fig.subplots_adjust(left=0.32, right=0.96, top=0.83, bottom=0.20)
    fig.suptitle(
        "Per-adapter Cutadapt occurrences reported",
        x=0.08,
        y=0.96,
        ha="left",
        fontsize=15,
        fontweight="bold",
        color=COLORS["ink"],
    )
    positions = list(range(len(labels)))
    ax.barh(positions, counts, color=COLORS["blue"], height=0.62)
    ax.set_yticks(positions, labels, fontsize=9, color=COLORS["ink"])
    ax.invert_yaxis()
    ax.set_xlabel("Reported trim occurrences (not unique reads)", color=COLORS["muted"])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
    _setup_axis(ax)
    for y, value in enumerate(counts):
        ax.text(value + max(counts) * 0.012, y, f"{value:,}", va="center", fontsize=9, color=COLORS["ink"])
    fig.text(
        0.08,
        0.07,
        "A2 has no visible total in the supplied summary. Adapter events may overlap; do not sum these bars as unique reads.",
        fontsize=8,
        color=COLORS["muted"],
        wrap=True,
    )
    _save(fig, "figure_03_reported_adapter_occurrences")


def _source_distribution_panel() -> None:
    panel = [
        ("A1 · Native adapter", "adapter_01_native.png"),
        ("A2 · Barcode NB022", "adapter_02_barcode.png"),
        ("A3 · 27F primer", "adapter_03_27f_primer.png"),
        ("A4 · 1492R primer", "adapter_04_1492r_primer.png"),
        ("A5 · Reverse barcode", "adapter_05_barcode_reverse.png"),
        ("A6 · Reverse native adapter", "adapter_06_native_reverse.png"),
    ]
    fig, axes = plt.subplots(3, 2, figsize=(12, 12))
    fig.suptitle(
        "Adapter-match length distributions from the supplied presentation",
        x=0.07,
        y=0.985,
        ha="left",
        fontsize=15,
        fontweight="bold",
        color=COLORS["ink"],
    )
    for ax, (title, filename) in zip(axes.flat, panel):
        image_path = SOURCE_FIGURES / filename
        if not image_path.exists():
            raise FileNotFoundError(f"Missing source plot: {image_path}")
        ax.imshow(Image.open(image_path).convert("RGB"))
        ax.set_title(title, loc="left", fontsize=10, color=COLORS["ink"], pad=6)
        ax.axis("off")
    fig.text(
        0.07,
        0.025,
        "Source plots reproduced as supplied (slides 13–18); numeric point tables and read-level match coordinates were not provided.",
        fontsize=8,
        color=COLORS["muted"],
    )
    fig.subplots_adjust(left=0.04, right=0.98, top=0.93, bottom=0.06, hspace=0.16, wspace=0.08)
    _save(fig, "figure_04_source_adapter_distributions")


def generate_figures() -> None:
    metrics = _read_metrics()
    _stacked_retention_figure(
        title="Reported read filtering outcome",
        total=int(metrics["reads_processed"]),
        retained=int(metrics["reads_retained"]),
        retained_label="Passed",
        removed_label="Discarded as trimmed",
        stem="figure_01_read_filtering",
    )
    _stacked_retention_figure(
        title="Reported base-pair retention",
        total=int(metrics["bases_processed"]),
        retained=int(metrics["bases_retained"]),
        retained_label="Retained",
        removed_label="Not retained",
        stem="figure_02_base_pair_retention",
    )
    _adapter_event_figure(metrics)
    _source_distribution_panel()
    print(f"Generated summary figures in {FIGURES}")


if __name__ == "__main__":
    generate_figures()
