class AxisReport:

    def print(self, candidates):

        print()
        print("=" * 60)
        print("AXIS ANALYSIS")
        print("=" * 60)

        print(f"Candidates        : {len(candidates)}")

        valid = sum(1 for c in candidates if c["valid"])

        print(f"Valid Axis        : {valid}")
        print(f"Rejected          : {len(candidates) - valid}")

        print("=" * 60)