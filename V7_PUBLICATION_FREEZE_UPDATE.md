# V7.2 publication reproducibility freeze

This update adds a standard-library-only freeze tool. It validates the final development
and held-out protocol, checks the frozen verifier and task hashes, verifies the expected
record counts and primary results, and hashes every publication-critical artifact.

The generated evidence archive includes the checkpoint, topology, metrics, task files,
external-model responses, and frozen implementation. By default it records the processed
test-array hash without copying the dataset bytes into the archive. Use
`--include-processed-test` only when redistribution is permitted.

## Install and test

```powershell
Expand-Archive `
  -Path "$env:USERPROFILE\Downloads\CO-ACT-CPS-publication-freeze-v7.2.zip" `
  -DestinationPath "D:\CO-ACT-CPS" `
  -Force

cd D:\CO-ACT-CPS
pytest -q
```

## Create the final freeze

```powershell
python scripts/freeze_publication_results.py `
  --root D:\CO-ACT-CPS `
  --output-dir artifacts/publication_freeze
```

Successful execution creates:

- `artifacts/publication_freeze/final_reproducibility_manifest.json`
- `artifacts/publication_freeze/final_results_summary.json`
- `artifacts/publication_freeze/SHA256SUMS.txt`
- `artifacts/publication_freeze/CO-ACT-CPS-publication-evidence.zip`

Do not modify frozen experiment files after this step. New human-review, SWaT, or
stronger-attacker studies must be stored as separately labeled extensions.
