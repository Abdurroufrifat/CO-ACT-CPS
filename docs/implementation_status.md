# Implementation status

Status date: 29 August 2026.

## Ready to run

- Python package and VS Code configuration.
- Synthetic CPS generator and end-to-end smoke test.
- Generic HAI/SWaT CSV inspection, train-only scaling, file-safe windowing, and source
  groups.
- Typed graph-temporal detector with supervised and normal-only modes.
- Validation-normal threshold calibration and detector/episode/calibration metrics.
- Evidence bundle, deterministic closed-evidence generator, optional Hugging Face mode.
- Four controlled explanation attacks and independent structural verifier.
- Post-ingestion evidence digest/HMAC verification, topology support, configured
  invariant evidence, and model counterfactual support fields.
- Explanation-integrity evaluation script.
- Operator-state Transformer and training entry point.
- Safety-constrained offline collaboration policy baseline and training entry point.
- Development-only Streamlit study interface and pseudonymous trial schema.
- Optional Qwen evidence-corpus export and QLoRA script.
- Unit/smoke tests.

## Not yet scientific results

- No HAI/SWaT data are bundled and no real-dataset results have been produced.
- The HAI/SWaT feature list, topology, invariant coefficients, and episode groups must be
  reviewed and frozen.
- Current root-cause evaluation needs official attack-target mapping.
- The four controlled explanation attacks are not an adaptive adversary.
- HMAC currently authenticates only a configured acquisition boundary; original-source
  authenticity, explicit multi-hop topology-path certificates, learned invariant
  thresholds, and stronger counterfactual causal tests remain to be implemented and
  ablated.
- The operator model and learned policy have no approved human data.
- The Streamlit scenario is synthetic and is not a validated study instrument.
- Qwen has not been downloaded, tuned, or evaluated.
- Required detector/XAI/security baselines and statistical analysis are not complete.
- No manuscript claim should be written as a result yet.

## Minimum next milestone

1. Run the test suite and synthetic demo.
2. Download HAI 23.05 and generate a data validation report.
3. Derive and validate attack episode IDs from the official detailed labels.
4. Reconstruct an explicit typed graph from the HAI graph resources/manual.
5. Implement persistence, Isolation Forest, LSTM/TCN, and topology-free Transformer
   baselines under identical splits.
6. Produce the first HAI detector table with five seeds and official eTaPR.
7. Only then implement adaptive explanation attacks and expand the verifier.

## Definition of “project complete”

The project is complete only after code, frozen configurations, data manifests,
real-dataset evaluations, baseline comparisons, ablations, attack evaluation,
statistical tests, reproducible figures/tables, and—if human claims remain—approved
human-study data and analysis all pass review. A runnable repository is the beginning,
not the publication result.
