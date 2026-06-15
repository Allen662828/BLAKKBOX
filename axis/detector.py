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

    def analyze(self, regions):

        candidates = []

        for region in regions:

            if not getattr(region, "calibration", False):
                continue

            # Placeholder: replace with extracted axis values
            values = [0, 10, 20, 30, 40]

            mono = self.monotonic.analyze(values)
            cont = self.continuity.analyze(values)

            score = self.confidence.score(mono, cont)

            candidates.append({
                "region": region,
                "valid": score >= 70,
                "score": score
            })

        self.report.print(candidates)

        return candidates