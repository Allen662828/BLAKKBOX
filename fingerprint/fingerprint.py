from fingerprint.manufacturer import ManufacturerDetector
from fingerprint.mcu import MCUDetector
from fingerprint.swid import SWIDDetector
from fingerprint.rom_family import ROMFamilyDetector
from fingerprint.memory_layout import MemoryLayoutDetector


class FingerprintEngine:

    def __init__(self):
        self.manufacturer = ManufacturerDetector()
        self.mcu = MCUDetector()
        self.swid = SWIDDetector()
        self.family = ROMFamilyDetector()
        self.layout = MemoryLayoutDetector()

    def analyze(self, rom: bytes):

        print()
        print("=" * 60)
        print("ROM FINGERPRINT")
        print("=" * 60)

        print(f"Manufacturer : {self.manufacturer.detect(rom)}")
        print(f"MCU          : {self.mcu.detect(rom)}")
        print(f"SW ID        : {self.swid.detect(rom)}")
        print(f"ROM Family   : {self.family.detect(rom)}")
        print(f"ROM Layout   : {self.layout.detect(rom)}")

        print("=" * 60)