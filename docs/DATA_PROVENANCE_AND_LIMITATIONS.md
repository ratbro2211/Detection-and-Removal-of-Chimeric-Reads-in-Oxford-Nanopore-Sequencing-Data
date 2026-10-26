# Data provenance and limitations

## Sources reviewed

The project summary is transcribed from the user-supplied `NGSproject` report (especially pages 7–18) and `Final_Presentation` (slides 12–19). The separate 40-page `Final_Document_for_NGS_Workflow` was reviewed for laboratory context. The source PDFs and full text transcripts are intentionally not included in this public repository.

The six adapter-match plots in `figures/source_adapter_distributions/` are extracted from the supplied presentation (slides 13–18). They are preserved as source figures, not regenerated from underlying numeric tables.

## Data that is not included

- Raw POD5 or FASTQ reads
- The complete Cutadapt log or JSON report
- The numeric arrays used to draw the six adapter-match distributions
- A reference genome or amplicon reference
- A sample manifest linking the laboratory workflow notes to the Nanopore read dataset

The project report points to a Google Drive result file, but that file was not available in the supplied attachments and was not retrieved for this repository update.

## Interpretation limits

The read totals and base-pair totals in `data/reported_metrics.csv` are reported values, not independently re-run results. The summary charts generated here reproduce only those exact aggregate values.

The adapter-match plots show length/count patterns, but the underlying data and match coordinates are absent. A match-length peak alone does not establish that a match was internal to a read or that the read is a PCR chimera. The source documents interpret some peaks as evidence of concatenation or chimeras; this repository labels those statements as hypotheses from the source report, not confirmed read-level classifications.

The documented Cutadapt command uses 5-prime and 3-prime adapter models with `--discard-trimmed`. That option discards reads that are trimmed and retains reads with no detected configured match; it does not split a chimeric read into valid fragments or independently verify a chimera. No alignment, assembly, or downstream impact analysis is reported in the supplied project documents.

The laboratory workflow attachment reports low/uncertain library quality and a final gel with no visible library bands. Its association with the FASTQ dataset summarized in the NGS report is not established, so the two evidence streams are described separately.
