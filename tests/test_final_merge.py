from delta.final_merge import FinalMerge
from validation.final_integrity import FinalIntegrityValidator


def test_final_merge_only_applies_filtered_offsets():
    original = bytes([1, 2, 3, 4])
    final = FinalMerge().merge(original, {2: 9})

    assert final == bytes([1, 2, 9, 4])


def test_final_integrity_accepts_original_plus_filtered_delta():
    original = bytes([1, 2, 3, 4])
    modified = bytes([1, 2, 9, 4])
    final = bytes([1, 2, 7, 4])

    summary = FinalIntegrityValidator().validate(
        original=original,
        modified=modified,
        final=final,
        existing_delta_offsets={2},
        allowed_offsets={2},
    )

    assert summary.file_size_preserved is True
    assert summary.no_new_modified_regions is True
    assert summary.untouched_bytes_preserved is True


def test_final_integrity_rejects_new_modified_offset():
    original = bytes([1, 2, 3, 4])
    modified = bytes([1, 2, 9, 4])
    final = bytes([1, 8, 7, 4])

    try:
        FinalIntegrityValidator().validate(
            original=original,
            modified=modified,
            final=final,
            existing_delta_offsets={2},
            allowed_offsets={2},
        )
    except RuntimeError as exc:
        assert "new modified offsets" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("Expected RuntimeError")


def test_final_integrity_rejects_mod_zero_application():
    original = bytes([10])
    modified = bytes([0])
    final = bytes([0])

    try:
        FinalIntegrityValidator().validate(
            original=original,
            modified=modified,
            final=final,
            existing_delta_offsets={0},
            allowed_offsets={0},
        )
    except RuntimeError as exc:
        assert "MOD zero-values" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("Expected RuntimeError")
