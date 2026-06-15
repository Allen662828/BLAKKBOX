class DeltaReport:

    def print(self, stats):

        print()
        print("=" * 60)
        print("DELTA ANALYSIS")
        print("=" * 60)

        print(f"Modified Regions : {stats['regions']}")
        print(f"Changed Bytes    : {stats['changed_bytes']:,}")
        print(f"Largest Region   : {stats['largest']:,} bytes")

        print("=" * 60)