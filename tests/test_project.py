import csv
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_metrics import load_metrics, validate_metrics


class ReportedMetricsTests(unittest.TestCase):
    def test_read_counts_balance(self):
        metrics = load_metrics()
        self.assertEqual(metrics["reads_removed"] + metrics["reads_retained"], metrics["reads_processed"])

    def test_rounded_retention_percentages_match(self):
        metrics = load_metrics()
        derived = validate_metrics(metrics)
        self.assertAlmostEqual(derived["reads_retained_percent"], 28.58, places=1)
        self.assertAlmostEqual(derived["bases_retained_percent"], 27.39, places=1)

    def test_adapter_counts_are_reported_or_explicitly_missing(self):
        path = ROOT / "data" / "adapter_event_counts.csv"
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 6)
        self.assertEqual(rows[1]["trimmed_occurrences"], "NA")
        self.assertTrue(all(row["source_plot"].startswith("figures/") for row in rows))


if __name__ == "__main__":
    unittest.main()
