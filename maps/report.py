class StructureReport:

    def print(self, structures):

        print()
        print("=" * 60)
        print("STRUCTURE DETECTION")
        print("=" * 60)

        if not structures:
            print("No structures detected.")
            print("=" * 60)
            return

        for index, item in enumerate(structures, start=1):

            rows, cols = item["shape"]

            print(
                f"[{index:02}] "
                f"{item['structure']:<14} "
                f"{rows}x{cols:<4} "
                f"Confidence: {item['confidence']}"
            )

        print("=" * 60)
