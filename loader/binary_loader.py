from pathlib import Path


class BinaryLoader:

    def load(self, filename: str) -> bytes:

        path = Path(filename)

        if not path.exists():
            raise FileNotFoundError(f"ROM file not found: {filename}")

        return path.read_bytes()
