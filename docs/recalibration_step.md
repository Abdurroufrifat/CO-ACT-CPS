# Validation-only node residual recalibration

The original detector aggregates raw residuals, allowing naturally difficult
channels to dominate alarms and root rankings. This step divides each node's
residual by its 99th-percentile error on the complete normal validation set,
then aggregates the five largest normalized node scores. No test labels are
read during recalibration.

```powershell
python scripts/recalibrate_detector.py `
  --checkpoint artifacts/hai_medium/detector.pt `
  --adjacency artifacts/hai_medium/adjacency.npy `
  --validation data/processed/hai/val.npz `
  --output artifacts/hai_recalibrated/detector.pt `
  --batch-size 16 `
  --score-top-k 5 `
  --calibration-quantile 0.99 `
  --node-scale-quantile 0.99 `
  --lower-reference-probability 0.05
```

Evaluate the recalibrated checkpoint on the complete chronological test set:

```powershell
python scripts/evaluate_full_hai.py `
  --checkpoint artifacts/hai_recalibrated/detector.pt `
  --adjacency artifacts/hai_medium/adjacency.npy `
  --windows data/processed/hai/test.npz `
  --metadata data/processed/hai/metadata.json `
  --catalog data/reference/hai23_attack_catalog.csv `
  --output artifacts/hai_recalibrated/full_test_metrics.json `
  --episodes-output artifacts/hai_recalibrated/full_test_episodes.csv `
  --predictions-output artifacts/hai_recalibrated/full_test_predictions.npz `
  --batch-size 16
```

This is a development improvement, not the final publication experiment.
Independent SWaT evaluation and a frozen HAI publication protocol remain
necessary to avoid reporting a design selected after examining HAI test data.
