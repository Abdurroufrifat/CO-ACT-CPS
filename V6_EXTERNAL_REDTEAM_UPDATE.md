# CO-ACT-CPS v6.1 External-LLM Red-Team Update

Extract this archive directly into the existing `D:\CO-ACT-CPS` project directory.
It adds the label-free development/held-out external generative-AI red-team workflow.
Version 6.1 also fingerprints the exact prompts and task files and excludes clean-copy
or neutral no-op generations from attack-success denominators.

After extraction, run:

```powershell
cd D:\CO-ACT-CPS
pytest -q
python scripts/export_external_redteam_tasks.py `
  --checkpoint artifacts/hai_process_graph_recalibrated/detector.pt `
  --adjacency artifacts/hai_process_graph/adjacency.npy `
  --windows data/processed/hai/test.npz `
  --output-dir artifacts/hai_external_redteam/tasks `
  --max-windows 100 `
  --development-fraction 0.20 `
  --batch-size 16 `
  --mc-samples 4
```

Continue with `docs/external_llm_redteam_step.md` only after the exporter reports
20 development tasks and 80 held-out tasks.
