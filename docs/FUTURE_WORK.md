# Future work

The submitted documents describe adapter filtering and interpret adapter-match plots, but do not include raw reads or a verified read-level chimera analysis. The next steps to complete the scientific pipeline are:

1. Add the original FASTQ input and full Cutadapt log/JSON output, plus sample metadata and the exact software version.
2. Re-run the documented filtering command and reconcile its output with the reported totals.
3. Export numeric match-length data and match coordinates for every adapter; regenerate the six distributions from those data.
4. Define the operational criteria for an internal adapter, concatenated read, and PCR chimera before classifying reads.
5. Apply an amplicon-appropriate chimera method and/or split-read alignment against a declared reference; retain per-read evidence and thresholds.
6. Compare read counts, length distributions, and mapping or assembly metrics before and after filtering.
7. Link wet-lab QC records to the sequencing sample IDs before drawing conclusions about library quality.

Until the missing inputs are available, the repository provides a reproducible summary of reported results and a runnable template for the documented Cutadapt filter, not a re-analysis of raw reads.
