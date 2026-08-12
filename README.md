# CRISPR Python Lab

A hands-on Python project for learning genomics through CRISPR guide-RNA analysis.

The first milestone scans a DNA sequence for candidate **SpCas9** guides next to an
`NGG` PAM. It reports the strand, genomic coordinates, guide sequence, PAM, and GC
content. This is an educational implementation—not a substitute for validated guide
design or off-target analysis in a research or clinical workflow.

## What you will learn

- Represent and validate DNA sequences in Python.
- Work with both DNA strands using reverse complements.
- Find PAM sites and extract 20-nucleotide protospacers.
- Store biological results in typed data structures.
- Test edge cases with Python's built-in `unittest`.

## Quick start

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
crispr-scan examples/example_sequence.fasta
python -m unittest discover -s tests
```

Example output is tab-separated and can be redirected to a file:

```text
strand  start  end  guide                 pam  gc_percent
+       0      20   GAGTCCGAGCAGAAGAAGAA  TGG  50.0
```

Coordinates use Python's zero-based, half-open convention: `start` is included and
`end` is excluded. For reverse-strand hits, the reported interval is still relative
to the forward input sequence.

## Learning roadmap

1. **Current:** identify SpCas9 `NGG` guide candidates.
2. Add simple quality filters and explain their biological limitations.
3. Read larger genomes and annotations with Biopython.
4. Compare candidate guides with potential off-target sequences.
5. Analyze amplicon-editing results with pandas and visualization tools.

## Responsible use

The scanner checks sequence patterns only. It does not evaluate chromatin
accessibility, efficiency, specificity, genetic variation, delivery, safety, or
experimental suitability. Always use validated tools and appropriate expert review
for real experimental decisions.
