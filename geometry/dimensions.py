class DimensionDetector:

    COMMON_TABLES = [
        (4, 4),
        (6, 6),
        (8, 8),
        (8, 10),
        (8, 16),
        (10, 10),
        (10, 12),
        (10, 16),
        (12, 16),
        (16, 16),
        (20, 20),
    ]

    def detect(self, region):

        size = region.length

        best = None
        best_error = float("inf")

        for rows, cols in self.COMMON_TABLES:

            cells = rows * cols

            error = abs(size - cells)

            if error < best_error:
                best_error = error
                best = (rows, cols)

        return best
