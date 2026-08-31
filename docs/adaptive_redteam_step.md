# Adaptive explanation-channel red team

Run from `D:\CO-ACT-CPS` after extracting the adaptive-red-team update.

```powershell
pytest -q

python scripts/evaluate_adaptive_explanation_attacks.py `
  --checkpoint artifacts/hai_process_graph_recalibrated/detector.pt `
  --adjacency artifacts/hai_process_graph/adjacency.npy `
  --windows data/processed/hai/test.npz `
  --output artifacts/hai_process_graph_recalibrated/adaptive_integrity_metrics.json `
  --max-windows 100 `
  --batch-size 16 `
  --mc-samples 4
```

The evaluator first selects detector-alarmed windows without reading test labels. It then searches
six truth-preserving manipulations per explanation and reports best-of-six attack success against
the legacy structural verifier and the hardened decision-semantic verifier.

This is a stronger development red team, not the final publication claim. The paper still requires
an external generative-model red team, held-out prompt families, SWaT confirmation, and the planned
operator study.
