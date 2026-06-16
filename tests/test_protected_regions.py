from protection.protected_regions import ProtectedRange, ProtectedRegionGuard


def test_protected_guard_accepts_clean_delta():
    guard = ProtectedRegionGuard([ProtectedRange(0x10, 0x20, "boot")])
    assert guard.validate({0x30: 99}) == []


def test_protected_guard_rejects_protected_delta():
    guard = ProtectedRegionGuard([ProtectedRange(0x10, 0x20, "boot")])
    try:
        guard.validate({0x18: 99})
    except RuntimeError as exc:
        assert "protected" in str(exc).lower()
        assert "boot" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("Expected RuntimeError")
