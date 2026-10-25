# Detection and removal of adapter-contaminated reads in Oxford Nanopore data

## Executive summary

The supplied project documents report a Cutadapt filtering run on **215,176 Nanopore reads**. They state that **153,681 reads (71.4%)** were discarded as trimmed and **61,495 reads (28.6%)** passed the filter. Of 139,129,218 input bases, 38,097,607 (27.4%) were reported as retained. The presentation also reports 48,697 reads reverse-complemented by Cutadapt (22.6%).

The supplied presentation contains six adapter-match length plots. They are included in this repository as source figures because the numeric series used to draw them were not supplied. The plots are not digitized or recalculated here. The reported summary values are visualized in new figures generated from `data/reported_metrics.csv`.

This is a summary of reported adapter filtering and sequence-artifact screening. It is **not** a verified, read-level chimera-detection result: raw FASTQ/POD5 reads, complete Cutadapt logs, match coordinates, and downstream alignment results were not supplied.

## Objective

The project aims to screen Oxford Nanopore reads for adapter, barcode, and primer sequence matches that may reflect library-preparation artifacts, concatenated molecules, or PCR chimeras. The source report also proposes downstream mapping and assembly comparisons as future work.

## Methods as reported

The source report states that reads were basecalled with MinKNOW in high-accuracy mode, with adapter and barcode trimming disabled at basecalling. The combined FASTQ was then processed with Cutadapt using six 5-prime/3-prime adapter sequences, `--rc`, and `--discard-trimmed`.

The documented filter discards reads that Cutadapt trims against the configured adapters and writes reads that pass without such a match. This is a filtering strategy; it does not by itself split multi-fragment reads or confirm a chimeric structure. The exact command is provided in `scripts/run_documented_cutadapt.sh` for use when the FASTQ input is available.

## Reported results

| Measure | Reported value |
|---|---:|
| Reads processed | 215,176 |
| Reads discarded as trimmed / reported with adapter matches | 153,681 (71.4%) |
| Reads passing filters | 61,495 (28.6%) |
| Bases processed | 139,129,218 bp |
| Bases retained | 38,097,607 bp (27.4%) |
| Reads reverse-complemented by Cutadapt | 48,697 (22.6%) |

The retained read and base-pair fractions differ, indicating that the filtered and retained groups did not contribute equal numbers of bases per read. The raw reads are unavailable here, so read-length distributions and per-sample effects cannot be recalculated.

## Adapter-match distributions

The source presentation shows six distributions for the native adapter, barcode sequences, and 27F/1492R primers. It describes peaks at short overlaps and at longer match lengths, and interprets some longer patterns as internal adapter/primer matches, concatenated reads, or chimeras.

Those plots are included under `figures/source_adapter_distributions/` and combined in Figure 4. Their point-level data and match coordinates are absent. Therefore, the repository preserves the source plots rather than presenting approximate digitizations as exact data. The source interpretations should be treated as hypotheses pending read-level verification.

## Associated laboratory context

The separate workflow document records DNA extraction, gel electrophoresis, PCR, quantification, and Nanopore library-preparation steps. It reports an early gel run with a maximum voltage of 33 V and poor separation, an unexpected band in a no-template PCR control, uncertain Qubit calculations, and no visible bands on the final library gel. The linkage between this laboratory record and the FASTQ dataset is not established, so these observations are not used to explain the Nanopore read-filtering totals.

## Limitations

- The FASTQ/POD5 inputs and complete Cutadapt JSON/log are not included; the reported run could not be independently reproduced.
- Numeric data for the six adapter plots and per-read match coordinates are absent.
- Adapter length distributions alone do not prove internal location or classify a read as chimeric.
- The documented `--discard-trimmed` step removes reads with configured matches; it does not distinguish adapters from chimeras or split reads into constituent fragments.
- No reference-based alignment, assembly, variant calling, or before/after downstream comparison is included.
- The wet-lab record cannot be linked to the read dataset from the supplied files.

## Reproducibility

From the repository root:

```bash
python -m pip install -r requirements.txt
python scripts/validate_metrics.py
python scripts/generate_figures.py
python scripts/generate_report.py
python -m unittest discover -s tests -v
```

To run the documented Cutadapt filter once the input is supplied:

```bash
bash scripts/run_documented_cutadapt.sh path/to/trimmed_reads.fastq
```

See `docs/DATA_PROVENANCE_AND_LIMITATIONS.md` and `docs/FUTURE_WORK.md` before interpreting the results as a validated chimera analysis.

## Source note

Aggregate metrics are transcribed from the supplied NGS project report (page 7) and final presentation (slide 12). Adapter plots and per-adapter log counts are taken from final presentation slides 13–18. The source PDFs themselves are not included in this public repository; they remain the original evidence supplied in the conversation.
