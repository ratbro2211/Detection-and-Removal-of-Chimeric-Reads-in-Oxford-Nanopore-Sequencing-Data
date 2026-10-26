#!/usr/bin/env python3
"""Check arithmetic consistency of the aggregate values transcribed from source."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METRICS_FILE = ROOT / "data" / "reported_metrics.csv"


def load_metrics() -> dict[str, float]:
    with METRICS_FILE.open(newline="", encoding="utf-8") as handle:
        return {row["metric"]: float(row["value"]) for row in csv.DictReader(handle)}


def validate_metrics(metrics: dict[str, float]) -> dict[str, float]:
    reads_total = metrics["reads_processed"]
    reads_removed = metrics["reads_removed"]
    reads_retained = metrics["reads_retained"]
    bases_total = metrics["bases_processed"]
    bases_retained = metrics["bases_retained"]

    if reads_removed + reads_retained != reads_total:
        raise ValueError("Reported read counts do not balance.")
    if not 0 <= bases_retained <= bases_total:
        raise ValueError("Retained base pairs must be between zero and total base pairs.")
    if metrics["reverse_complemented_reads"] > reads_total:
        raise ValueError("Reverse-complemented count cannot exceed total reads.")

    read_pct = reads_retained / reads_total * 100
    bp_pct = bases_retained / bases_total * 100
    if abs(read_pct - metrics["read_retention_percent"]) > 0.15:
        raise ValueError("Reported read-retention percentage does not match the counts.")
    if abs(bp_pct - metrics["bases_retention_percent"]) > 0.15:
        raise ValueError("Reported base-retention percentage does not match the counts.")

    return {
        "reads_removed_percent": reads_removed / reads_total * 100,
        "reads_retained_percent": read_pct,
        "bases_removed": bases_total - bases_retained,
        "bases_retained_percent": bp_pct,
    }


if __name__ == "__main__":
    derived = validate_metrics(load_metrics())
    print("PASS: reported counts balance and rounded percentages are consistent.")
    print(f"  read retention: {derived['reads_retained_percent']:.2f}%")
    print(f"  base retention: {derived['bases_retained_percent']:.2f}%")
    print(f"  bases not retained: {derived['bases_removed']:,.0f} bp")
