from loader.binary_loader import BinaryLoader


class OriginalLoader:

    def __init__(self):
        self.loader = BinaryLoader()

    def load(self, filename):

        print("Loading ORIGINAL ROM...")

        data = self.loader.load(filename)

        print(f"ORIGINAL Size : {len(data):,} bytes")

        return data