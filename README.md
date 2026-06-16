# BLAKKBOX

OEM-preserving DENSO Diesel ECU calibration framework.

BLAKKBOX processes an ORIGINAL ROM and a MOD ROM, extracts only the existing
modified regions, filters those deltas, and exports an enhanced binary using
one rule:

```text
ENHANCED_BIN = ORIGINAL_BIN + FILTERED_DELTA
```

## Core rules

- ORIGINAL BIN is read-only.
- MOD BIN is the only editable source.
- Only existing modified regions are processed.
- Untouched OEM bytes are preserved byte-for-byte.
- No new modified regions are created.
- MOD values equal to `0x00` are not applied.
- File size, address layout, and binary alignment are preserved.
- Executable code, interrupt vectors, diagnostics, DTC, EGR, switch-mask, and
  security-related areas are protected by policy and must not be modified.

## v2 Features

- ROM input preflight guard
- ECU fingerprinting
- Byte-level delta extraction
- Calibration-region classification
- Axis and geometry detection
- Configurable BLAKKBOX filtered-delta processing
- Optional protected address-range policy
- Final OEM-preservation validation
- Enhanced BIN export
- JSON report generation
- Markdown report generation
- SHA-256 job manifest generation
- Batch job runner
- GitHub Actions safety scan to block ROMs, caches, and generated artifacts

## Supported targets

- Toyota DENSO
- Mitsubishi DENSO
- Nissan DENSO
- Mazda DENSO
- Hyundai DENSO

## Single job usage

```bash
python main.py --original path/to/ORIGINAL.bin --mod path/to/MOD.bin --out output/job_001
```

Dry run without writing the enhanced binary:

```bash
python main.py --original path/to/ORIGINAL.bin --mod path/to/MOD.bin --out output/job_001 --dry-run
```

Strict mode:

```bash
python main.py --original path/to/ORIGINAL.bin --mod path/to/MOD.bin --out output/job_001 --strict
```

## Batch usage

Expected layout:

```text
private_jobs/
├── toyota_1gd_job_001/
│   ├── original.bin
│   └── modified.bin
└── nissan_yd25_job_002/
    ├── original.bin
    └── mod.bin
```

Run all jobs:

```bash
python main.py --job-dir private_jobs --out output/batch_001
```

## Output

```text
output/job_001/
├── enhanced.bin
├── analysis.json
├── analysis.md
└── manifest.json
```

## Configuration

`configs/pipeline.yaml` controls filtered-delta thresholds and output names.

`configs/protected_regions.yaml` may define private protected address ranges.
Keep proprietary address maps private. Use `configs/protected_regions.example.yaml`
as a template.

## Repository safety

Do not commit customer ROM files or generated binaries. CI blocks committed
ROM-like extensions such as `.bin`, `.ori`, `.mod`, `.hex`, `.s19`, `.mot`,
`.frf`, `.sgm`, and `.dump`, plus Python caches and generated output folders.
