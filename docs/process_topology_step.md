# HAI process-topology experiment (Windows PowerShell)

Run these commands from `D:\CO-ACT-CPS` after extracting the update ZIP there.

## 1. Build the topology from normal training windows

```powershell
python scripts/build_hai23_topology.py `
  --metadata data/processed/hai_medium/metadata.json `
  --train-windows data/processed/hai_medium/train.npz `
  --output data/reference/hai23_process_topology.json
```

Expected: 86 connected nodes, zero isolated nodes, and six typed relations. The official thermal
relation is intentionally omitted because projecting the published device graph onto observed
HAI-23.05 channels produces no direct observed-to-observed thermal edge.

## 2. Create the run configuration

```powershell
Copy-Item configs/hai_process_graph_template.yaml configs/hai_process_graph.yaml -Force
```

## 3. Train the fair process-graph ablation

```powershell
python scripts/train_detector.py --config configs/hai_process_graph.yaml
```

This is intentionally the same CPU-scale training budget as the earlier medium model. It tests the
topology change fairly. Do not compare a larger model against the old model and attribute all gains
to process grounding.

## 4. Run the full chronological HAI test

```powershell
python scripts/evaluate_full_hai.py `
  --checkpoint artifacts/hai_process_graph/detector.pt `
  --adjacency artifacts/hai_process_graph/adjacency.npy `
  --windows data/processed/hai_medium/test.npz `
  --metadata data/processed/hai/metadata.json `
  --catalog data/reference/hai23_attack_catalog.csv `
  --output artifacts/hai_process_graph/full_test_metrics.json `
  --episodes-output artifacts/hai_process_graph/full_test_episodes.csv `
  --predictions-output artifacts/hai_process_graph/full_test_predictions.npz `
  --batch-size 16
```

Send the topology summary and final metrics. We will compare episode recall, false-alarm episodes,
eTaPR-F1, target hit@3, Brier score, ECE, and inference time against the frozen statistical baseline.
