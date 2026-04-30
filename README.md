# 🧬 Detection and Removal of Chimeric Reads in Oxford Nanopore Sequencing Data

## 📌 Overview
This project focuses on identifying and removing chimeric reads and internal adapter sequences in Oxford Nanopore sequencing data. Long-read sequencing technologies such as Nanopore are prone to artifacts including adapter contamination, concatenated reads, and PCR chimeras, which can negatively impact downstream analyses.

This study uses adapter trimming statistics and sequence analysis to detect such artifacts and improve sequencing data quality.

---

## 🎯 Objectives
- Detect internal adapter sequences in Nanopore reads  
- Identify chimeric and concatenated reads  
- Remove contaminated reads to improve data quality  
- Analyze adapter match length distributions  
- Interpret sequencing artifacts using statistical patterns  

---

## ❗ Problem Statement
Nanopore reads may contain:
- Internal adapters  
- Barcode contamination  
- Primer sequences  
- Chimeric reads  

These artifacts can lead to:
- Incorrect genome assembly  
- False variant detection  
- Reduced mapping accuracy  

---

## 🔬 Methodology

### Workflow
FASTQ Reads
↓
Adapter Detection
↓
Adapter Trimming (Cutadapt)
↓
Length Distribution Analysis
↓
Internal Adapter Detection
↓
Chimeric Read Identification
↓
Filtered Clean Reads


---

## 🛠 Tools Used
- Cutadapt  
- Python  
- Excel / plotting tools  
- Oxford Nanopore MinKNOW (basecalling)

---

## ⚙️ Key Step: Adapter Trimming

```bash
cutadapt \
-g TTTTTTTTCCTGTACTTCGTTCAGTTACGTATTGCT \
-g ACAGACGACTACAAACGGAATCGA \
-g AGAGTTTGATCMTGGCTCAG \
-a TACGGYTACCTTGTTACGACTT \
-a TCGATTCCGTTTGTAGTCGTCTGT \
-a ACGTAACTGAACGAAGTACAGG \
--discard-trimmed --rc \
-o clean_reads.fastq \
trimmed_reads.fastq
