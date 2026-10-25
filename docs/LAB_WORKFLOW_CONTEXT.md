# Associated laboratory workflow context

This note summarizes the separate 40-page workflow document supplied with the project. It is context only: the source document does not establish that these laboratory observations came from the same sample/library as the Nanopore reads summarized in the NGS report.

## Workflow covered in the source document

The record describes environmental DNA extraction, agarose gel electrophoresis, touchdown PCR, AMPure bead cleanup, DNA quantification, Oxford Nanopore end-preparation, native barcode ligation, adapter ligation, and a final library gel check. Detailed procedures are intentionally not reproduced in this analysis summary.

## Reported quality-control observations

- The initial DNA extraction was described as low-yield; a modified lysis approach was recorded for biofilm material.
- An early gel run had slow/incomplete migration and poor separation. The document reports a maximum voltage of 33 V against a planned 120 V.
- PCR notes report a visible band for sample L1 and an unexpected band in the T1 no-template control. The source lists contamination, primer-dimer formation, or nonspecific amplification as possibilities; it does not resolve which occurred.
- The quantification section reports a standard-curve equation and estimated concentrations, but the displayed values are internally difficult to reconcile. Treat the reported concentrations as provisional until checked against the original plate-reader export and calculation sheet.
- The final library gel section reports no visible DNA bands and lists low concentration or losses during cleanup as possible explanations.

These observations are relevant to interpreting readiness for sequencing, but they are not evidence that the summarized FASTQ dataset failed or passed library QC. The sample linkage is unknown.
