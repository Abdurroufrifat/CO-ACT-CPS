# Software verification report

Verification date: 29 August 2026.

Environment used for this check: Python 3.12, PyTorch 2.7.1 CPU, Linux. The user-facing
instructions recommend Python 3.11 on Windows for broad dependency compatibility.

## Passed checks

- `ruff check .`: passed.
- `ruff format --check .`: passed.
- `python -m compileall -q src scripts apps tests`: passed.
- `python -m pytest -q`: **15 passed**.
- Normal-only synthetic CLI demo: completed with checkpoint, windows, adjacency,
  evidence bundle, process checks, explanation, verification, and collaboration action.
- Single-window analysis CLI: completed.
- Controlled integrity evaluation: completed on 12 synthetic windows. Clean explanations
  were accepted and all four scripted manipulations were warned in this software check.
- Simulated interaction-log generator: completed.
- Operator-state Transformer development training: completed.
- Safety-constrained collaboration-policy development training: completed.

## Not executed in this verification

- HAI or SWaT training, because datasets are not redistributed with the project.
- Hugging Face model download/inference or QLoRA, because they are optional GPU/network
  paths.
- Streamlit browser interaction, though the app passes compilation/lint checks.
- Ethics-approved human data collection.

## Interpretation

Passing these checks means the software interfaces work together. The controlled
synthetic integrity result is deliberately easy and must not be reported as evidence of
security, human benefit, or journal-level performance. The next scientific milestone is
the frozen HAI 23.05 split/topology plus baseline comparison.

