from axis.monotonic import MonotonicAnalyzer
from axis.continuity import ContinuityAnalyzer
from axis.confidence import AxisConfidence
from axis.report import AxisReport


class AxisDetector:

    def __init__(self):

        self.monotonic = MonotonicAnalyzer()
        self.continuity = ContinuityAnalyzer()
        self.confidence = AxisConfidence()
        self.report = AxisReport()

    def extract_values(self, rom: bytes, region):
        """
        Extract raw bytes from the candidate region.

        For now we treat every byte as an unsigned value.
        Later this can be upgraded to support:
            - 8-bit
            - 16-bit Big Endian
            - 16-bit Little Endian
            - Float
            - Signed values
        """

        start = region.start
        end = region.end + 1

        return list(rom[start:end])

    def analyze(self, rom: bytes, regions):

        candidates = []

        for region in regions:

            if not getattr(region, "calibration", False):
                continue

            values = self.extract_values(rom, region)

            if len(values) < 4:
                continue

            monotonic = self.monotonic.analyze(values)

            continuity = self.continuity.analyze(values)

            score = self.confidence.score(monotonic, continuity)

            candidates.append(
                {
                    "region": region,
                    "values": values,
                    "score": score,
                    "valid": score >= 70,
                }
            )

        self.report.print(candidates)

        return candidates
