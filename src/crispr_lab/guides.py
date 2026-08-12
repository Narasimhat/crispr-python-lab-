"""Find simple SpCas9 guide candidates in DNA sequences."""

from dataclasses import dataclass

DNA_BASES = frozenset("ACGT")


@dataclass(frozen=True, slots=True)
class GuideCandidate:
    """A 20 nt protospacer adjacent to an SpCas9 NGG PAM."""

    sequence: str
    pam: str
    strand: str
    start: int
    end: int
    gc_percent: float


def normalize_dna(sequence: str) -> str:
    """Remove whitespace, uppercase, and validate an unambiguous DNA sequence."""
    normalized = "".join(sequence.split()).upper()
    invalid = set(normalized) - DNA_BASES
    if invalid:
        symbols = ", ".join(sorted(invalid))
        raise ValueError(f"DNA sequence contains unsupported symbols: {symbols}")
    return normalized


def reverse_complement(sequence: str) -> str:
    """Return the reverse complement of an unambiguous DNA sequence."""
    normalized = normalize_dna(sequence)
    return normalized.translate(str.maketrans("ACGT", "TGCA"))[::-1]


def _gc_percent(sequence: str) -> float:
    return round(100 * sum(base in "GC" for base in sequence) / len(sequence), 1)


def find_spcas9_guides(sequence: str) -> list[GuideCandidate]:
    """Return 20 nt candidates followed by NGG on either DNA strand.

    Coordinates are zero-based and half-open on the forward input sequence.
    """
    dna = normalize_dna(sequence)
    candidates: list[GuideCandidate] = []

    for strand, scanned in (("+", dna), ("-", reverse_complement(dna))):
        for start in range(len(scanned) - 22):
            guide = scanned[start : start + 20]
            pam = scanned[start + 20 : start + 23]
            if pam[1:] != "GG":
                continue

            if strand == "+":
                forward_start = start
                forward_end = start + 20
            else:
                forward_start = len(dna) - (start + 20)
                forward_end = len(dna) - start

            candidates.append(
                GuideCandidate(
                    sequence=guide,
                    pam=pam,
                    strand=strand,
                    start=forward_start,
                    end=forward_end,
                    gc_percent=_gc_percent(guide),
                )
            )

    return sorted(candidates, key=lambda item: (item.start, item.strand))
