class MonotonicAnalyzer:

    def analyze(self, values):

        if len(values) < 2:
            return False

        increasing = True
        decreasing = True

        for a, b in zip(values, values[1:]):

            if b < a:
                increasing = False

            if b > a:
                decreasing = False

        return increasing or decreasing
