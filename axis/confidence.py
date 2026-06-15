class AxisConfidence:

    def score(self, monotonic, continuity):

        score = 0

        if monotonic:
            score += 50

        if continuity:
            score += 50

        return score
