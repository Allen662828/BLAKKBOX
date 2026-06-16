from validation.rom_security import RomSecurityValidator


def test_rom_security_rejects_same_file(tmp_path):
    file_path = tmp_path / "same.bin"
    file_path.write_bytes(b"abc")

    try:
        RomSecurityValidator().validate(file_path, file_path)
    except ValueError as exc:
        assert "same file" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("Expected ValueError")


def test_rom_security_accepts_two_files(tmp_path):
    original = tmp_path / "original.bin"
    modified = tmp_path / "modified.bin"
    original.write_bytes(b"abc")
    modified.write_bytes(b"abd")

    summary = RomSecurityValidator().validate(original, modified)
    assert summary.original_size == 3
    assert summary.modified_size == 3
