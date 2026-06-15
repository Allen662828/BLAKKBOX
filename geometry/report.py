class GeometryReport:

    def print(self, tables):

        print()
        print("=" * 60)
        print("GEOMETRY ANALYSIS")
        print("=" * 60)

        if not tables:
            print("Candidates        : 0")
            print("Valid Tables      : 0")
            print("Rejected          : 0")
            print("=" * 60)
            return

        valid = sum(
            1 for table in tables
            if table.get("valid", False)
        )

        rejected = len(tables) - valid

        average_score = (
            sum(
                table.get("score", 0)
                for table in tables
            ) / len(tables)
        )

        print(f"Candidates        : {len(tables)}")
        print(f"Valid Tables      : {valid}")
        print(f"Rejected          : {rejected}")
        print(f"Average Score     : {average_score:.1f}")

        print()
        print("Detected Shapes")
        print("-" * 60)

        shape_count = {}

        for table in tables:

            rows, cols = table.get("shape", (0, 0))

            key = f"{rows} x {cols}"

            shape_count[key] = shape_count.get(key, 0) + 1

        for shape in sorted(shape_count.keys()):
            print(f"{shape:<12} : {shape_count[shape]}")

        print()
        print("Top Candidates")
        print("-" * 60)

        sorted_tables = sorted(
            tables,
            key=lambda item: item.get("score", 0),
            reverse=True
        )

        for index, table in enumerate(sorted_tables[:5], start=1):

            rows, cols = table.get("shape", (0, 0))

            print(
                f"[{index}] "
                f"{rows}x{cols:<4} "
                f"Score: {table.get('score', 0):>3}"
            )

        print("=" * 60)
