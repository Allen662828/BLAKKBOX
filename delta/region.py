from dataclasses import dataclass


@dataclass
class DeltaRegion:

    start: int
    end: int

    region_type: str = "UNKNOWN"

    confidence: float = 0.0

    executable: bool = False
    calibration: bool = False
    checksum: bool = False
    protected: bool = False

    @property
    def length(self):
        return self.end - self.start + 1