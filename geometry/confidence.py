class GeometryConfidence:

    def score(self, rectangle, interpolation):

        score = 0

        if rectangle:
            score += 50

        if interpolation:
            score += 50

        return score
