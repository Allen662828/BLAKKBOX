# BLAKKBOX Universal DENSO ROM Enhancement Workflow v3

This document is the active BLAKKBOX processing system for DENSO ROM enhancement tasks.

## Core formula

```text
ENHANCED_BIN = ORIGINAL_BIN + FILTERED_DELTA
FILTERED_DELTA = safe, classified, bounded changes extracted only from ORIGINAL vs MOD
```

## Non-negotiable file policy

1. `ORIGINAL_BIN` is read-only and must never be edited directly.
2. `MOD_BIN` is the only editable source for enhancement decisions.
3. `FINAL_BIN` is built by merging approved filtered values back onto `ORIGINAL_BIN`.
4. Untouched OEM bytes must remain byte-for-byte identical to `ORIGINAL_BIN`.
5. The workflow must never create new modified regions.
6. The workflow may only process regions that are already different in `MOD_BIN` compared with `ORIGINAL_BIN`.
7. Any `MOD_BIN` value equal to `0x00` must be skipped and preserved from `ORIGINAL_BIN`.

## Protected policy

The pipeline must not modify:

- Executable code
- Interrupt vectors
- Bootloader or checksum logic
- Access-control logic
- Security bypass logic
- EGR maps
- EGR system calibrations
- DTC or diagnostic tables
- Switch masks
- Emissions defeat logic
- Any configured protected address range

Optional protected ranges can be configured privately in:

```text
configs/protected_regions.yaml
```

## Aggressive tune policy

Aggressive enhancement is allowed only when it remains inside already-modified calibration regions and passes all validation rules.

Aggressive mode may:

- Smooth uneven calibration spikes inside existing modified regions.
- Reduce parallel-table mismatch when the tables are already modified.
- Clean noisy deltas caused by uneven manual edits.
- Apply bounded strengthening to existing MOD changes when the region is classified as calibration data.

Aggressive mode must not:

- Touch protected regions.
- Add new modified offsets.
- Expand a modified table beyond the existing changed region.
- Infer or invent missing maps outside the MOD delta.
- Change `0x00` MOD values.
- Modify executable code or diagnostic/emissions-disable areas.

## Delta filter rules

Default rules are stored in:

```text
configs/pipeline.yaml
```

Suggested baseline filter profile:

| Delta magnitude | Action |
|---:|---|
| 0-5 | Keep MOD value |
| 5-8 | Apply 80% of delta |
| >8 | Apply 55% of delta |

Aggressive calibration-only profile:

| Region classification | Action |
|---|---|
| Smooth calibration table | Keep or strengthen bounded MOD trend |
| Noisy table spike | Smooth toward local table trend |
| Parallel table mismatch | Align only inside matching existing MOD regions |
| Axis/geometry candidate | Preserve unless confidently classified |
| Protected or unknown region | Reject |

## Required pipeline

1. Preflight `ORIGINAL_BIN` and `MOD_BIN` paths.
2. Validate equal ROM size.
3. Fingerprint `ORIGINAL_BIN`.
4. Extract byte-level delta from `ORIGINAL_BIN` vs `MOD_BIN`.
5. Cluster modified offsets into existing modified regions.
6. Classify each region as calibration, axis, geometry, unknown, or protected.
7. Detect table shape and neighboring trend candidates.
8. Apply filtered-delta rules only inside existing modified regions.
9. Skip every `MOD_BIN` value equal to `0x00`.
10. Reject filtered deltas that touch protected ranges.
11. Merge approved filtered values onto `ORIGINAL_BIN`.
12. Validate that `FINAL_BIN` created no new modified offsets.
13. Validate that every untouched byte still matches `ORIGINAL_BIN`.
14. Export final binary and full audit artifacts.

## Validation gates

A final file is invalid if any of these checks fail:

- Final size differs from original size.
- Any untouched byte differs from `ORIGINAL_BIN`.
- Any new modified offset exists outside the original MOD delta.
- Any protected range was changed.
- Any `0x00` MOD value was copied into the final file.
- Any executable-code-like region was modified.
- Any EGR, DTC, diagnostic, switch-mask, or emissions-disable area was modified.

## Required outputs

Every completed job should export:

```text
enhanced.bin
analysis.json
analysis.md
manifest.json
```

The manifest should include:

- Original filename
- MOD filename
- Final filename
- File size
- Original hash
- MOD hash
- Final hash
- Total original MOD offsets
- Total final changed offsets
- Rejected protected offsets
- Skipped `0x00` offsets
- Validation status

## Batch mode

Use batch mode for repeatable customer/job folders:

```bash
python main.py --job-dir private_jobs --out output/batch_001
```

Each job should contain:

```text
original.bin
modified.bin
```

or:

```text
original.bin
mod.bin
```

## Operating rule

When a user requests sports, stage, max, or aggressive tuning, treat this workflow as the active system. Enhance only what the provided MOD file already changed, preserve the OEM baseline everywhere else, and always prioritize file integrity, auditability, and protected-region safety.