"""
fingerprint/fingerprint.py

ROM fingerprint engine.

Coordinates the individual fingerprint detectors and produces
a structured summary of the ROM characteristics.
"""

from __future__ import annotations

from fingerprint.manufacturer import ManufacturerDetector
from fingerprint.mcu import MCUDetector
from fingerprint.swid import SWIDDetector
from fingerprint.rom_family import ROMFamilyDetector
from fingerprint.memory_layout import MemoryLayoutDetector

from core.logger import section
from core.logger import kv


class FingerprintEngine:
    """
    Main fingerprint engine.
    """

    def __init__(self) -> None:

        self.manufacturer = ManufacturerDetector()
        self.mcu = MCUDetector()
        self.swid = SWIDDetector()
        self.family = ROMFamilyDetector()
        self.layout = MemoryLayoutDetector()

    def analyze(self, rom: bytes) -> dict:
        """
        Analyze a ROM and return a fingerprint dictionary.
        """

        fingerprint = {
            "manufacturer": self.manufacturer.detect(rom),
            "mcu": self.mcu.detect(rom),
            "swid": self.swid.detect(rom),
            "rom_family": self.family.detect(rom),
            "memory_layout": self.layout.detect(rom),
        }

        section("ROM FINGERPRINT")

        kv("Manufacturer", fingerprint["manufacturer"])
        kv("MCU", fingerprint["mcu"])
        kv("SW ID", fingerprint["swid"])
        kv("ROM Family", fingerprint["rom_family"])
        kv("ROM Layout", fingerprint["memory_layout"])

        return fingerprint
