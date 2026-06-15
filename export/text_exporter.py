"""
test_export.py

Simple exporter test.
"""

from pathlib import Path

from export.metadata import MetadataBuilder
from export.json_exporter import JsonExporter


def main() -> None:

    print("=" * 60)
    print("BLAKKBOX EXPORT TEST")
    print("=" * 60)

    metadata = MetadataBuilder().build(
        original_file="ORIGINAL.bin",
        modified_file="MOD.bin",
        original_size=507904,
        modified_size=507904,
    )

    output = Path("output") / "analysis.json"

    JsonExporter().export(
        output_file=str(output),
        report=metadata,
    )

    print(f"Output file : {output.resolve()}")

    if output.exists():
        print("Export successful.")
    else:
        print("Export failed.")


if __name__ == "__main__":
    main()
