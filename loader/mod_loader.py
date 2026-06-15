from loader.binary_loader import BinaryLoader


class ModLoader:

    def __init__(self):
        self.loader = BinaryLoader()

    def load(self, filename):

        print("Loading MOD ROM...")

        data = self.loader.load(filename)

        print(f"MOD Size : {len(data):,} bytes")

        return data