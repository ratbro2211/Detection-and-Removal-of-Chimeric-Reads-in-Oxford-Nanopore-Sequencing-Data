#!/usr/bin/env bash
# Reproduce the filtering command documented in the supplied NGS report.
# This is not a read-level chimera classifier.
set -euo pipefail

if [[ $# -lt 1 || $# -gt 3 ]]; then
  echo "Usage: $0 INPUT_FASTQ [OUTPUT_FASTQ] [JSON_REPORT]" >&2
  exit 2
fi

input_fastq="$1"
output_fastq="${2:-results/reads_passing_filter.fastq}"
json_report="${3:-results/cutadapt_report.json}"
log_file="${output_fastq%.*}.cutadapt.log"

if [[ ! -f "$input_fastq" ]]; then
  echo "Input FASTQ not found: $input_fastq" >&2
  exit 1
fi
if ! command -v cutadapt >/dev/null 2>&1; then
  echo "Cutadapt is not installed. Install it before running this script." >&2
  exit 1
fi

mkdir -p "$(dirname "$output_fastq")" "$(dirname "$json_report")"

cutadapt \
  -g TTTTTTTTCCTGTACTTCGTTCAGTTACGTATTGCT \
  -g ACAGACGACTACAAACGGAATCGA \
  -g AGAGTTTGATCMTGGCTCAG \
  -a TACGGYTACCTTGTTACGACTT \
  -a TCGATTCCGTTTGTAGTCGTCTGT \
  -a ACGTAACTGAACGAAGTACAGG \
  --discard-trimmed \
  --rc \
  --json "$json_report" \
  -o "$output_fastq" \
  "$input_fastq" 2>&1 | tee "$log_file"

echo "Passing reads: $output_fastq"
echo "Cutadapt JSON: $json_report"
echo "Cutadapt log:  $log_file"
