class DeltaStatistics:

    def summarize(self, regions):

        if not regions:
            return {
                "regions": 0,
                "changed_bytes": 0,
                "largest": 0,
            }

        lengths = [r.length for r in regions]

        return {
            "regions": len(regions),
            "changed_bytes": sum(lengths),
            "largest": max(lengths),
        }