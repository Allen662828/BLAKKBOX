from export.manifest import ManifestExporter, sha256_file


def test_manifest_records_hashes(tmp_path):
    original = tmp_path / "original.bin"
    modified = tmp_path / "modified.bin"
    output = tmp_path / "enhanced.bin"
    original.write_bytes(b"abc")
    modified.write_bytes(b"abd")
    output.write_bytes(b"abe")

    manifest = ManifestExporter().build(
        original_file=original,
        modified_file=modified,
        output_bin=output,
        report_file=tmp_path / "analysis.json",
        status="PASS",
    )

    assert manifest["inputs"]["original"]["sha256"] == sha256_file(original)
    assert manifest["outputs"]["enhanced_sha256"] == sha256_file(output)
