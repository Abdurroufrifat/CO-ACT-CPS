# Reproducibility freeze verification

- Freeze ID: `60b263ab81ea46ad0e4057c0eaac93471d389a39983f2deed9b2ae1e1034bf22`
- Evidence ZIP SHA-256: `8554561403ac258915933cf8fe8b0c317dfdcf05f1e29428089c7601126d943c`
- Manifest records: 31
- ZIP members: 33
- ZIP CRC test: passed
- Archived artifact hash mismatches: 0
- Standalone checksum records matching the manifest: 31/31
- Processed test array included in ZIP: no; its SHA-256 is preserved in the manifest

The uploaded standalone `SHA256SUMS.txt` and the copy inside the ZIP use different newline
conventions (Windows CRLF versus LF). After newline-independent parsing, both contain the
same 31 path-to-digest mappings and exactly match the reproducibility manifest. This is a
text portability difference, not an evidence-integrity failure.

All tables and figures in this package were generated exclusively from the frozen evidence
ZIP. No model, verifier, task, response, threshold, or evaluation result was changed.
