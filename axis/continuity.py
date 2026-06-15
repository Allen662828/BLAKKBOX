class ContinuityAnalyzer:

    def analyze(self, values):

        if len(values) < 3:
            return False

        jumps = 0

        for a, b in zip(values, values[1:]):
            if abs(b - a) > 32:
                jumps += 1

        return jumps < len(values) * 0.1