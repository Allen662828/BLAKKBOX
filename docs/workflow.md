# BLAKKBOX ROM enhancement workflow v2

## Formula

```text
ENHANCED_BIN = ORIGINAL_BIN + FILTERED_DELTA
```

## Pipeline

1. Preflight ORIGINAL and MOD paths.
2. Validate equal ROM size.
3. Fingerprint ORIGINAL.
4. Extract byte-level delta from ORIGINAL vs MOD.
5. Cluster and classify modified regions.
6. Detect axis and geometry candidates.
7. Apply filtered-delta rules only inside existing modified regions.
8. Skip every MOD value equal to `0x00`.
9. Reject filtered deltas that touch configured protected ranges.
10. Merge filtered values onto ORIGINAL.
11. Validate that FINAL created no new modified offsets.
12. Validate that every untouched byte still matches ORIGINAL.
13. Export `enhanced.bin`, `analysis.json`, `analysis.md`, and `manifest.json`.

## Filter rules

Default rules are stored in `configs/pipeline.yaml`.

| Delta magnitude | Action |
|---:|---|
| 0-5 | Keep MOD value |
| 5-8 | Apply 80% of delta |
| >8 | Apply 55% of delta |

## Protected policy

The pipeline must not modify executable code, interrupt vectors, EGR maps,
EGR system calibrations, DTC/diagnostic tables, switch masks, access-control
logic, or any security bypass logic.

Optional protected address ranges can be configured privately in:

```text
configs/protected_regions.yaml
```

## Batch mode

Use batch mode for repeatable customer/job folders:

```bash
python main.py --job-dir private_jobs --out output/batch_001
```

Each job should contain `original.bin` and either `modified.bin` or `mod.bin`.
