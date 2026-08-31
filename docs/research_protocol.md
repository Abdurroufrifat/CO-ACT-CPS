# CO-ACT-CPS research protocol

## Recommended title

**CO-ACT-CPS: Contestable and Co-Adaptive Generative AI for Secure Human-AI
Incident Diagnosis in Cyber-Physical Systems**

Alternative titles:

1. **Securing the Explanation Channel: Process-Grounded Generative AI for
   Human-Centered CPS Incident Diagnosis**
2. **When the Alarm Is Right but the Explanation Is Wrong: Verified Generative
   Decision Support for Industrial CPS Security**
3. **Evidence Before Eloquence: Contestable Generative Explanations for Trustworthy
   Cyber-Physical-System Security**

## Problem and gap

Industrial anomaly detectors, post-hoc explainers, and LLM incident assistants are
usually evaluated as if the alarm and its explanation were one output. They are not.
An adversary—or an unfaithful generator—may leave the detector's alarm unchanged
while omitting decisive evidence, redirecting the causal diagnosis, hiding plausible
alternatives, inflating certainty, or recommending an inappropriate response. A
correct alarm can therefore produce an unsafe human decision.

Existing detector-robustness work primarily protects predictions. Existing XAI work
primarily measures fidelity or stability. Existing LLM grounding work rarely checks
sensor-actuator topology, physical process evidence, calibrated uncertainty, and the
operator's evolving reliance as one independently verified decision-support loop.
The research gap is a method and benchmark for **prediction-preserving explanation
attacks** in CPS, together with a verifier and collaboration policy that decide not only
what evidence is valid, but how the system should interact with a human when evidence
is incomplete or contested.

This is a novelty hypothesis, not a guaranteed priority claim. Before submission,
perform and document a systematic search through the submission date, including
forward/backward citation chasing and explicit inclusion criteria.

## Research questions

- **RQ1:** How successfully can an attacker manipulate an operator-facing CPS
  explanation while holding the detector alarm and predicted class within a fixed
  tolerance?
- **RQ2:** How much do typed process topology, masked next-state evidence, physical
  invariants, provenance, counterfactual tests, and calibrated uncertainty improve
  detection of explanation manipulation without rejecting valid explanations?
- **RQ3:** Does a verified, co-adaptive collaboration policy improve diagnosis accuracy,
  reduce unsafe actions, and calibrate reliance better than no AI, alarm-only, generic
  XAI, and verified-static explanation conditions?
- **RQ4:** Does the security/human benefit generalize across HAI and SWaT, attack
  families, operating shifts, generator models, and operator expertise levels at
  acceptable latency?

## Preregisterable hypotheses

- **H1:** Prediction-preserving attacks will materially increase causal-diagnosis error
  and inappropriate reliance when explanations are shown without an integrity gate.
- **H2:** The full verifier will reduce manipulation attack success rate relative to
  text-only and attribution-only gates, while keeping the clean-explanation false-alarm
  rate below a preregistered operational bound.
- **H3:** Verified co-adaptive support will reduce unsafe operator decisions relative to
  unverified generative explanations without increasing median response time beyond a
  preregistered non-inferiority margin.
- **H4:** Explicit uncertainty and alternatives will reduce overreliance when the top two
  causal hypotheses are close, relative to a single confident explanation.
- **H5:** Typed topology plus process constraints will improve attack-episode detection
  and root-cause Hit@K under distribution shift relative to a topology-free temporal
  Transformer.

Define effect sizes, operational bounds, non-inferiority margins, exclusions, and the
primary outcome before observing confirmatory human-study results.

## Technical contributions to test

1. A formal threat model and controlled benchmark for prediction-preserving attacks on
   the AI-to-operator explanation channel.
2. A normal-only typed graph-temporal detector that produces alarm evidence, ranked
   causal hypotheses, and epistemic uncertainty rather than only a class label.
3. An independent process-grounded integrity gate that checks evidence provenance,
   graph support, physical/operational consistency, counterfactual support, uncertainty,
   causal alternatives, and action constraints.
4. A closed-evidence generative layer whose text can be replaced or attacked without
   bypassing the verifier.
5. An operator-state model and safety-constrained offline collaboration policy that can
   explain, expose evidence, compare alternatives, ask for context, warn, or abstain.
6. A multi-level evaluation separating detector quality, explanation integrity,
   calibration, computational overhead, and human decision outcomes.

Only claim a contribution after its corresponding experiment succeeds.

## System stages

### Training stage

1. Fit preprocessing parameters on training-normal telemetry only.
2. Construct a typed graph from physical flow, control, and communication relations.
3. Train the graph-temporal detector by masking the final state and selected history
   values, then predicting the held-out state. Use supervised attack/root heads only as
   a separately declared ablation when episode-safe attack labels are available.
4. Calibrate the anomaly threshold and probability scale on validation-normal windows.
5. Construct expert-reviewed, closed evidence-to-JSON examples; optionally tune a text
   LLM with QLoRA.
6. After approved human data exists, train the operator-state model on prior interaction
   sequences with participant-held-out splits.
7. Train the collaboration policy offline, enforce hard verifier constraints, then freeze
   it before confirmatory evaluation.

### Inference and security-monitoring stage

1. Validate telemetry schema, feature order, timestamp continuity, and provenance.
2. Produce alarm probability, node residuals/root hypotheses, and uncertainty.
3. Build an immutable evidence bundle with stable evidence identifiers.
4. Generate an operator-facing JSON explanation using only the bundle.
5. Independently verify every cited claim and permitted action.
6. Select a collaboration action subject to safety constraints.
7. Display evidence and uncertainty; the operator makes and records the final decision.

## Mathematical method

Let a CPS window be \(X_{t-W+1:t}\in\mathbb{R}^{W\times N\times F}\), with
typed adjacency matrices \(A^{(r)}\in\{0,1\}^{N\times N}\). A relational message
layer is

\[
M_t = \sum_{r=1}^{R}\tilde A^{(r)}H_tW_r,\qquad
H'_t=\operatorname{LN}\left(H_t+g_t\odot M_t+(1-g_t)\odot H_t\right),
\]

where \(g_t=\sigma(W_g[H_t\Vert M_t])\). A temporal Transformer maps each
node's sequence to a contextual representation. For normal-only learning, the final
state is masked and reconstructed:

\[
\hat X_t=f_\theta(X_{t-W+1:t-1},\{A^{(r)}\}),\qquad
L_{pred}=\operatorname{SmoothL1}(X_t,\hat X_t).
\]

For a mass-balance invariant with state \(l\), inlet \(q^{in}\), and outlet \(q^{out}\),

\[
L_{phys}=\frac{1}{W-1}\sum_\tau
\left[(\hat l_{\tau}-\hat l_{\tau-1})
-\kappa(\hat q^{in}_{\tau}-\hat q^{out}_{\tau})\right]^2.
\]

The implemented training objective is

\[
L_{det}=L_{pred}+\lambda_{phys}L_{phys}
\]

for normal-only learning, and

\[
L_{det}=L_{BCE}+\lambda_rL_{root}+\lambda_xL_{recon}
+\lambda_{phys}L_{phys}
\]

for the supervised ablation.

Let node residual \(e_{t,i}=\|X_{t,i}-\hat X_{t,i}\|_1/F\). The anomaly score is
the mean of the top \(K=\max(1,\lceil0.1N\rceil)\) node residuals:

\[
s_t=\frac{1}{K}\sum_{i\in\operatorname{TopK}(e_t)}e_{t,i},\qquad
p_t=\sigma\left(\frac{s_t-\tau}{T}\right).
\]

\(\tau\) and \(T\) are estimated only from validation-normal scores. Monte Carlo
dropout gives epistemic uncertainty

\[
u_t=\operatorname{Std}_{m=1}^{M}\left[p_t^{(m)}\right].
\]

Let an explanation \(z\) cite evidence set \(C(z)\). The verifier contains bounded
checks \(c_j\in[0,1]\) for evidence identity/coverage, causal agreement, provenance,
topology/invariant support, counterfactual consistency, uncertainty preservation,
alternative disclosure, and permitted action. Its score is

\[
I(z,E)=\sum_j w_jc_j,\qquad \sum_jw_j=1.
\]

Hard failures—unknown evidence, missing mandatory evidence, invalid provenance, or an
unsafe action—override the average and force warning/abstention. Weights and thresholds
must be selected on validation attacks and frozen for test evaluation.

The collaboration state combines AI evidence \(a_t\) and estimated operator state
\(o_t=(\hat d_t,\hat c_t,\hat r_t,\hat w_t)\), representing diagnosis belief,
confidence, reliance, and workload. A policy chooses

\[
\pi_\phi(k\mid a_t,o_t),\quad k\in
\{\text{summary,evidence,alternatives,question,warning,abstain}\}.
\]

The offline objective is outcome-weighted policy learning plus conservative imitation,
entropy regularization, and verifier safety constraints:

\[
L_{policy}=-\mathbb{E}\left[\bar\rho_tR_t\log\pi_\phi(k_t\mid s_t)\right]
+\beta L_{imit}-\eta H(\pi_\phi)+\lambda_sC_{safe}.
\]

\(\bar\rho_t\) is clipped importance weight from logged behavior propensity. The
reward must be preregistered; one defensible form is diagnosis correctness minus a
larger unsafe-decision penalty, a small response-time penalty, and an overreliance
penalty. A learned policy must never override verifier abstention.

## Datasets and roles

| Dataset | CPS domain | Role | Strength | Limitation |
|---|---|---|---|---|
| HAI 23.05 | Coupled boiler, turbine, water treatment, HIL | Primary detector/integrity benchmark | Public, realistic typed processes, attack metadata and graph resources | No genuine operator interaction; source authenticity cannot be recovered retrospectively |
| SWaT | Six-stage water treatment | Independent replication | Widely used real testbed, sensor/actuator dependencies | Request-controlled; versions/labels differ; no human traces |
| CPS-CoLab | Controlled human interaction records created by this project | Human outcomes/operator model/policy | Directly measures diagnosis, safety, reliance, workload, time | Requires approval, power analysis, recruitment, and careful external-validity claims |

Do not merge datasets as if their tags share meaning. Train/evaluate each topology
separately, then test transfer only through aligned semantic node types or a declared
domain-adaptation method.

## Experimental matrix

### Detector evaluation

- Within-dataset, file/time/episode-safe train-validation-test evaluation.
- Cross-operating-period and cross-version shift where available.
- Zero-day evaluation by holding out attack mechanisms, not random windows.
- Sensor noise, missingness, delay, replay, bias, actuator-state mismatch, and topology
  corruption at declared severities.
- At least five seeds; keep all preprocessing and calibration inside each training fold.

### Explanation-security evaluation

- Hold detector alarm probability/class fixed within a preregistered tolerance.
- Manipulate evidence selection, causal claim, alternatives, uncertainty, and action.
- Compare rule/template attacks, gradient/search-based adaptive attacks, and independent
  LLM red-team attacks.
- Train/validate attacks and verifier thresholds on disjoint episodes/prompts.
- Report clean false alarms alongside manipulation detection; a verifier that rejects
  everything is not useful.

### Human evaluation

- Conditions: no AI, alarm only, generic XAI, unverified generative explanation,
  verified static explanation, and full co-adaptive verified support. The current UI
  contains five conditions and should add the unverified-LLM arm if sample size permits.
- Within- or mixed design with randomized/counterbalanced scenario order.
- Primary outcomes: diagnosis correctness and unsafe decision rate.
- Secondary outcomes: response time, confidence calibration, appropriate reliance,
  workload, trust, explanation comprehension, and intervention frequency.
- Include manipulated and clean explanations without deceiving participants beyond the
  approved protocol and debriefing plan.

## Baselines

### Detector baselines

1. Persistence/linear forecast residual: establishes whether deep learning is necessary.
2. Isolation Forest or One-Class SVM: traditional normal-only baseline.
3. LSTM/TCN autoencoder or forecaster: standard temporal deep baseline.
4. Temporal Transformer without graph: isolates typed topology value.
5. Graph-temporal network without physics loss: isolates process constraints.
6. Full CO-ACT detector.
7. Strong published HAI/SWaT implementation with official configuration when code and
   license permit.

### Explanation and interaction baselines

1. Alarm only.
2. Gradient/attention or SHAP-like attribution without causal verification.
3. Unverified LLM summary from the same evidence.
4. Static verified explanation.
5. Full operator-aware adaptive policy.
6. Oracle evidence/policy upper bound for diagnosis—not presented as deployable.

Use the same detector alarm across explanation conditions whenever testing the
explanation channel.

## Metrics

### Detector

- PR-AUC, ROC-AUC, MCC, F1, balanced accuracy, precision, recall, and false-positive
  rate.
- Attack-episode recall, official eTaPR for HAI, time-to-detect, and false-alarm episodes.
- Root-cause Hit@1/Hit@3 and mean reciprocal rank when verified root labels exist.
- Brier score, expected calibration error, and reliability diagrams.
- CPU/GPU latency, peak memory, parameter count, and throughput.

### Explanation integrity

- Manipulation attack success rate: fraction of manipulated explanations that pass.
- Integrity detection rate and class-specific detection.
- Clean-explanation false-alarm rate.
- Evidence precision/recall, mandatory-evidence coverage, causal consistency,
  uncertainty preservation error, and action-policy violation rate.
- Adaptive-attack query/compute cost and verifier latency.

### Human outcomes

- Diagnosis accuracy and unsafe-decision probability.
- Sensitivity/specificity to correct versus incorrect AI advice.
- Confidence calibration and reliance calibration.
- Response time and intervention count.
- NASA-TLX or approved workload measure; validated trust scale chosen before the study.
- Qualitative error themes using a preregistered coding scheme where applicable.

## Ablations

Remove or replace one component at a time:

1. Typed topology → fully connected/statistical graph.
2. Physics loss → zero weight.
3. Normal-only masked prediction → supervised classifier.
4. MC-dropout uncertainty → point confidence.
5. Provenance check → absent.
6. Invariant and topology checks → absent.
7. Counterfactual check → absent.
8. Alternative disclosure → top cause only.
9. Independent verifier → generator self-check.
10. Operator-state model → fixed population state.
11. Adaptive policy → static verified explanation.
12. Qwen generator → deterministic template and another text model.

Report both security gain and clean-case cost for each removal.

## Statistical analysis

- Predefine one primary detector, integrity, and human outcome to control multiplicity.
- Use episode-level bootstrap confidence intervals for telemetry outcomes.
- Use paired seed/fold tests for model comparisons and correct multiple comparisons.
- For repeated human trials, use mixed-effects logistic regression for correctness/unsafe
  action and an appropriate mixed model or survival model for response time, with
  participant and scenario random effects.
- Report effect sizes and confidence intervals, not only p-values.
- Run an a priori simulation-based power analysis after pilot variance estimates; do
  not choose a sample size by convenience.

## Planned paper figures

1. End-to-end architecture and security boundary.
2. Threat model showing alarm-preserving explanation manipulation.
3. Typed sensor-actuator graph for each dataset.
4. Detector precision-recall and calibration plots.
5. Integrity detection versus clean false-alarm trade-off.
6. Adaptive-attack success versus attacker budget.
7. Human diagnosis/safety effects with confidence intervals.
8. Reliance calibration and response-time distribution.
9. Ablation/security-performance Pareto plot.

## Planned paper tables

1. Closest-work capability comparison after the final systematic search.
2. Dataset, split, attack, and topology summary.
3. Model/baseline hyperparameters and computational budget.
4. Main detector results.
5. Explanation attack and verifier results.
6. Cross-dataset/shift/zero-day results.
7. Ablations.
8. Human-study outcomes and mixed-model estimates.
9. Runtime, memory, and verifier overhead.

## Decision gates

- **Gate 1:** Do not proceed to LLM tuning until HAI preprocessing and baseline splits
  are independently checked.
- **Gate 2:** Do not claim process grounding until explicit topology and invariants are
  configured and ablated.
- **Gate 3:** Do not claim human benefit without approval and confirmatory human data.
- **Gate 4:** Do not claim robustness from the four scripted attacks alone; implement an
  adaptive attacker.
- **Gate 5:** If the human study cannot finish in time, narrow the manuscript to a
  technical explanation-channel security paper and describe the UI only as a prototype.
