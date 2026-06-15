"""
loader/rom_loader.py

Loads the ORIGINAL and MOD ROM files.

The RomLoader coordinates the individual loaders and returns
both ROM images to the pipeline.
"""

from __future__ import annotations

from loader.original_loader import OriginalLoader
from loader.mod_loader import ModLoader

from core.logger import info


class RomLoader:
    """
    Main ROM loader.
    """

    def __init__(self) -> None:

        self.original = OriginalLoader()
        self.mod = ModLoader()

    def load(
        self,
        original_file: str,
        mod_file: str,
    ) -> tuple[bytes, bytes]:
        """
        Load the ORIGINAL and MOD ROM images.

        Parameters
        ----------
        original_file : str
            Path to the original ROM.

        mod_file : str
            Path to the modified ROM.

        Returns
        -------
        tuple[bytes, bytes]
            (original_rom, modified_rom)
        """

        info("Loading ROM files...")

        original = self.original.load(original_file)
        modified = self.mod.load(mod_file)

        if original is None:
            raise RuntimeError("Failed to load ORIGINAL ROM.")

        if modified is None:
            raise RuntimeError("Failed to load MOD ROM.")

        info(
            f"Loaded ORIGINAL ({len(original):,} bytes) "
            f"and MOD ({len(modified):,} bytes)"
        )

        return original, modified
