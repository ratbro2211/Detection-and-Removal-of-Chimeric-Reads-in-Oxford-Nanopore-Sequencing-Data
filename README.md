# Nanopore chimeric-read and adapter screening

This repository organizes the supplied Oxford Nanopore project into a reproducible package with a report, summary figures, adapter definitions, and a runnable version of the documented Cutadapt filter.

## Reported outcome

The source documents report 215,176 reads processed, 153,681 reads discarded as trimmed (71.4%), and 61,495 reads passing filters (28.6%). They report 139,129,218 input bases and 38,097,607 retained bases (27.4%). These values are transcribed from the submitted report and presentation; this repository did not rerun the original FASTQ analysis because the FASTQ/POD5 files and complete Cutadapt log were not supplied.

## Scientific scope

The six adapter-match length plots are preserved under `figures/source_adapter_distributions/`. Their point-level numeric data are unavailable, so they are not digitized or presented as newly calculated curves. The source report interprets some longer match patterns as possible internal adapters, concatenated reads, and PCR chimeras; those interpretations require read-level evidence before they can be considered confirmed.

The associated laboratory workflow notes are summarized separately in `docs/LAB_WORKFLOW_CONTEXT.md`. The available files do not establish that those wet-lab observations correspond to the FASTQ dataset in the NGS report.

## Quick start

Requires Python 3.10+ and Matplotlib.

```bash
python -m pip install -r requirements.txt
python scripts/validate_metrics.py
python scripts/generate_figures.py
python scripts/generate_report.py
python -m unittest discover -s tests -v
```

The generated report is `reports/final_report.pdf`; the narrative source is `reports/final_report.md`.

## Run the documented filter

The source documents use Cutadapt with six configured sequences, reverse-complement handling, and `--discard-trimmed`. Once a FASTQ file is available:

```bash
bash scripts/run_documented_cutadapt.sh path/to/trimmed_reads.fastq
```

This writes reads that pass without a configured adapter match, plus a Cutadapt JSON report and log. It does not perform validated chimera classification or split reads into fragments. Raw sequencing files are intentionally excluded from Git.

## Repository map

- `data/` — reported aggregate metrics and adapter definitions/counts
- `figures/` — exact-summary plots and the six source adapter plots
- `reports/` — final Markdown and PDF report
- `scripts/` — figure/report generation, metric checks, and documented Cutadapt command
- `docs/` — provenance, limitations, laboratory context, and future-work plan

## Source and interpretation notes

See `docs/DATA_PROVENANCE_AND_LIMITATIONS.md`, `docs/LAB_WORKFLOW_CONTEXT.md`, and `docs/FUTURE_WORK.md`. The original PDFs and full text transcripts are not included in this public repository, as requested.
