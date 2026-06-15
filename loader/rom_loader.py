from loader.original_loader import OriginalLoader
from loader.mod_loader import ModLoader


class RomLoader:

    def __init__(self):
        self.original = OriginalLoader()
        self.mod = ModLoader()

    def load(self, original_file, mod_file):

        original = self.original.load(original_file)
        mod = self.mod.load(mod_file)

        return original, mod