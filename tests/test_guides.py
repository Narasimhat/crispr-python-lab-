import unittest

from crispr_lab.guides import find_spcas9_guides, reverse_complement


class GuideTests(unittest.TestCase):
    def test_reverse_complement_normalizes_whitespace_and_case(self) -> None:
        self.assertEqual(reverse_complement("acgt\nGG"), "CCACGT")

    def test_finds_forward_spcas9_candidate(self) -> None:
        guide = "GAGTCCGAGCAGAAGAAGAA"
        candidates = find_spcas9_guides(guide + "TGG")

        self.assertEqual(len(candidates), 1)
        candidate = candidates[0]
        self.assertEqual(candidate.sequence, guide)
        self.assertEqual(candidate.pam, "TGG")
        self.assertEqual(candidate.strand, "+")
        self.assertEqual((candidate.start, candidate.end), (0, 20))
        self.assertEqual(candidate.gc_percent, 50.0)

    def test_finds_reverse_strand_candidate(self) -> None:
        reverse_oriented_target = "ACGTACGTACGTACGTACGTAGG"
        forward_sequence = reverse_complement(reverse_oriented_target)

        candidates = find_spcas9_guides(forward_sequence)

        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0].strand, "-")
        self.assertEqual(candidates[0].sequence, "ACGTACGTACGTACGTACGT")
        self.assertEqual((candidates[0].start, candidates[0].end), (3, 23))

    def test_rejects_ambiguous_bases(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported symbols: N"):
            find_spcas9_guides("ACGTN")


if __name__ == "__main__":
    unittest.main()
