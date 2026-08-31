# External Generative-AI Red-Team Protocol

This stage evaluates whether the frozen decision-semantic verifier generalizes to
unseen language produced by a separate generative model. It must be run after the
template adaptive evaluation and before any verifier modification.

## Scientific controls

- Windows are selected only from detector alarms; test labels are never exported.
- Twenty percent of selected windows form the development split. The remaining
  eighty percent are held out and are the primary result.
- The task, checkpoint, data, topology, and verifier are fingerprinted with SHA-256.
- The exact prompts and complete development/held-out task files are fingerprinted.
- The attack model must preserve cause, evidence-ID set, alternatives, and uncertainty.
- Malformed and fact-changing outputs are reported and excluded from attack-success
  denominators rather than silently counted as blocked attacks.
- Exact clean copies and neutral no-op outputs are excluded from attack-success denominators.
- The model, prompt, decoding parameters, number of candidates, and verifier must be
  frozen before held-out generation.
- The held-out result reports Wilson 95% confidence intervals and an exact paired
  McNemar test comparing the legacy and hardened verifier.

Automatic checks cover the committed structured facts and require a material change to
operator-facing text. Two blinded reviewers should later inspect the free text for
unsupported claims and harmful decision influence before the final paper calls every
candidate a valid truth-preserving attack.

## 1. Export the frozen tasks

From `D:\CO-ACT-CPS` in PowerShell:

```powershell
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

This should produce 20 development tasks, 80 held-out tasks, and `manifest.json`.

## 2. Install the lightweight local attack model stack

```powershell
python -m pip install -r requirements-redteam.txt
```

The CPU-compatible starting model is `Qwen/Qwen3-0.6B`. Its role is only to attack
the explanation channel; it never changes the CPS detector. A larger second model
should be added later for the final multi-model result.

## 3. Smoke-test three development tasks

```powershell
python scripts/generate_external_redteam_hf.py `
  --tasks artifacts/hai_external_redteam/tasks/development_tasks.jsonl `
  --output artifacts/hai_external_redteam/development_smoke_responses.jsonl `
  --model-id Qwen/Qwen3-0.6B `
  --max-tasks 3 `
  --candidates-per-task 2
```

If this succeeds, generate all development candidates:

```powershell
python scripts/generate_external_redteam_hf.py `
  --tasks artifacts/hai_external_redteam/tasks/development_tasks.jsonl `
  --output artifacts/hai_external_redteam/development_responses.jsonl `
  --model-id Qwen/Qwen3-0.6B `
  --candidates-per-task 4
```

## 4. Evaluate development responses

```powershell
python scripts/evaluate_external_redteam_responses.py `
  --tasks artifacts/hai_external_redteam/tasks/development_tasks.jsonl `
  --responses artifacts/hai_external_redteam/development_responses.jsonl `
  --manifest artifacts/hai_external_redteam/tasks/manifest.json `
  --output artifacts/hai_external_redteam/development_metrics.json
```

Use development results only to verify that generation and parsing work. Do not modify
the verifier after this point.

## 5. Generate and evaluate the held-out split once

```powershell
python scripts/generate_external_redteam_hf.py `
  --tasks artifacts/hai_external_redteam/tasks/heldout_tasks.jsonl `
  --output artifacts/hai_external_redteam/heldout_responses.jsonl `
  --model-id Qwen/Qwen3-0.6B `
  --candidates-per-task 4

python scripts/evaluate_external_redteam_responses.py `
  --tasks artifacts/hai_external_redteam/tasks/heldout_tasks.jsonl `
  --responses artifacts/hai_external_redteam/heldout_responses.jsonl `
  --manifest artifacts/hai_external_redteam/tasks/manifest.json `
  --output artifacts/hai_external_redteam/heldout_metrics.json
```

The held-out run may take a long time on CPU. The response writer flushes every
candidate, so partial output is retained if the process is interrupted.

## Interpretation

A strong result requires high task coverage and committed-fact preservation, zero or
low clean rejection, a materially lower hardened attack-success rate than the legacy
rate, a narrow confidence interval, and a significant paired test. A nonzero hardened
attack-success rate is useful evidence: it identifies genuine residual weaknesses and
must not be hidden by post-hoc verifier tuning.
