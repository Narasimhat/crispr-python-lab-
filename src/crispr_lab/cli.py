"""Command-line interface for the educational guide scanner."""

import argparse
from pathlib import Path

from .guides import find_spcas9_guides


def read_fasta(path: Path) -> str:
    """Read sequence lines from a single-record FASTA file."""
    lines = path.read_text(encoding="utf-8").splitlines()
    sequence_lines = [line.strip() for line in lines if line and not line.startswith(">")]
    if not sequence_lines:
        raise ValueError(f"No DNA sequence found in {path}")
    return "".join(sequence_lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Find SpCas9 NGG guide candidates")
    parser.add_argument("fasta", type=Path, help="single-record FASTA file")
    args = parser.parse_args()

    candidates = find_spcas9_guides(read_fasta(args.fasta))
    print("strand\tstart\tend\tguide\tpam\tgc_percent")
    for item in candidates:
        print(
            f"{item.strand}\t{item.start}\t{item.end}\t{item.sequence}\t"
            f"{item.pam}\t{item.gc_percent:.1f}"
        )


if __name__ == "__main__":
    main()
