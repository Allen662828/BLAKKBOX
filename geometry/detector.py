from geometry.dimensions import DimensionDetector
from geometry.rectangle import RectangleAnalyzer
from geometry.interpolation import InterpolationAnalyzer
from geometry.confidence import GeometryConfidence
from geometry.report import GeometryReport


class GeometryDetector:

    def __init__(self):

        self.dimension = DimensionDetector()
        self.rectangle = RectangleAnalyzer()
        self.interpolation = InterpolationAnalyzer()
        self.confidence = GeometryConfidence()
        self.report = GeometryReport()

    def analyze(self, candidates):

        tables = []

        for candidate in candidates:

            region = candidate["region"]

            shape = self.dimension.detect(region)

            rectangle = self.rectangle.analyze(shape)

            interpolation = self.interpolation.analyze(region)

            score = self.confidence.score(
                rectangle,
                interpolation
            )

            tables.append({
                "region": region,
                "shape": shape,
                "score": score,
                "valid": score >= 70
            })

        self.report.print(tables)

        return tables
