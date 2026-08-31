# Explanation-channel threat model

## Protected decision process

The protected object is not only the detector prediction. It is the chain from
telemetry evidence to an operator's diagnosis and response.

Security properties:

1. **Evidence binding:** every material explanation claim cites an immutable evidence
   identifier present in the current event bundle.
2. **Causal consistency:** the probable cause and alternatives agree with the ranked
   process evidence or are explicitly marked as operator-supplied context.
3. **Uncertainty integrity:** generated language cannot silently increase certainty.
4. **Action containment:** the generator can recommend only diagnostic/escalation
   actions configured by the system; it never issues actuator commands.
5. **Contestability:** the operator can inspect evidence, alternatives, verifier reasons,
   and abstention status.
6. **Prediction preservation in attack tests:** the attacker must keep the detector alarm
   and class unchanged within a declared tolerance, isolating explanation-channel risk.

## Adversary capabilities

Evaluate progressively stronger attackers:

- **A1 — Output editor:** can remove, reorder, or rewrite explanation fields after
  generation but cannot change the signed evidence bundle.
- **A2 — Prompt/context attacker:** can inject instructions or misleading operational
  text into non-authenticated context passed to the generator.
- **A3 — Evidence selector attacker:** can try to suppress valid evidence or replace IDs,
  while the underlying detector output remains fixed.
- **A4 — Adaptive black-box attacker:** observes verifier accept/warn/abstain and queries
  it under a fixed budget to maximize manipulation success.
- **A5 — Compromised generator:** the generator deliberately produces a plausible but
  misleading JSON explanation.

Test goals include cause redirection, critical-evidence omission, confidence inflation,
alternative hiding, and unsafe recommendation.

## Defender assumptions

- The detector and independent verifier execute in a trusted boundary for the main
  experiments.
- Evidence bundle IDs, model/version IDs, timestamps, and hashes are immutable after
  construction.
- The topology/invariant specification is reviewed and versioned.
- The UI accurately displays verifier status and does not allow hidden text to bypass it.
- The human operator is authorized but can be busy, uncertain, or susceptible to
  automation bias.

Each assumption needs a sensitivity experiment where feasible. A compromised detector,
verifier, or key-management system is outside the initial scope and must be stated.

## Non-goals

- Automatically controlling the physical process.
- Proving that a static historical dataset was cryptographically authentic at collection.
- Defending every form of training-data poisoning, model extraction, or membership
  inference in one paper.
- Treating operator disagreement as an attack without independent ground truth.
- Claiming that an LLM's self-critique is an independent security verifier.

## Authentication boundary

For HAI/SWaT, file hashes can prove that local experiment files did not change after
ingestion. They cannot prove source authenticity before release. A genuine telemetry
authentication claim requires an instrumented producer/testbed that signs messages or
an authenticated acquisition gateway. Keep these two claims separate in the paper.

## Evaluation success and failure

An explanation attack succeeds when it changes a protected explanation property,
preserves the detector output, and passes the verifier. A clean false alarm occurs when
a valid explanation is warned or rejected. Report both; integrity detection alone can be
maximized trivially by abstaining on everything.

