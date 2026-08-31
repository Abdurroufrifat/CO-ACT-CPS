# Full chronological HAI evaluation

The medium subset is useful for training and pipeline debugging, but its test
windows were stratified and subsampled. Therefore, episode recall, detection
delay, false-alarm episode count, and eTaPR from that subset are not valid
chronological results.

Install the bundled official eTaPR wheel without accessing the network:

```powershell
python -m pip install --no-deps vendor/eTaPR-22.6.1-py3-none-any.whl
```

Evaluate the existing medium checkpoint on the complete chronological test
windows:

```powershell
python scripts/evaluate_full_hai.py `
  --checkpoint artifacts/hai_medium/detector.pt `
  --adjacency artifacts/hai_medium/adjacency.npy `
  --windows data/processed/hai/test.npz `
  --metadata data/processed/hai/metadata.json `
  --catalog data/reference/hai23_attack_catalog.csv `
  --output artifacts/hai_medium/full_test_metrics.json `
  --episodes-output artifacts/hai_medium/full_test_episodes.csv `
  --predictions-output artifacts/hai_medium/full_test_predictions.npz `
  --batch-size 8
```

The script rejects irregular/subsampled windows, validates the expected 14 +
38 episode structure, reports the official eTaP/eTaR/eTaPR-F1, and calculates
target localization only where a target is observable among the 86 telemetry
features.

These remain development results if the prepared stride is 64 rows. A final
paper must state the evaluation resolution and use the publication stride for
comparisons with raw-second HAI results.
