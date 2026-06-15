class MemoryLayoutDetector:

    KNOWN_SIZES = {
        327680: "320 KB",
        376832: "368 KB",
        524288: "512 KB",
        733184: "716 KB",
        917504: "896 KB",
        1015808: "1,015,808 bytes",
        1048576: "1 MB",
        1572864: "1.5 MB",
        2097152: "2 MB",
        2621440: "2.5 MB",
        3145728: "3 MB",
        4194304: "4 MB",
    }

    def detect(self, rom: bytes) -> str:
        return self.KNOWN_SIZES.get(len(rom), f"{len(rom):,} bytes")