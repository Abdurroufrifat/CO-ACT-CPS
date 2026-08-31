# Special-Issue alignment

The attached two-page PDF is a **call for papers**, not an empirical research paper.
It announces the Engineering Applications of Artificial Intelligence Special Issue
“Human-Centered and Trustworthy AI for Cybersecurity in Cyber-Physical Systems,” with
submissions stated as 1 October 2026–31 January 2027.

The call emphasizes two connected risk levels:

- model-level adversarial threats, including adversarial examples, poisoning,
  backdoors, extraction, and membership inference;
- socio-technical threats that exploit human behavior, trust, cognitive bias,
  information manipulation, and human-in-the-loop systems.

It requests reproducible, validated engineering work rather than a conceptual use of
AI terminology.

## Direct mapping

| Call theme | CO-ACT-CPS element | Required evidence |
|---|---|---|
| Generative AI for defensive cybersecurity | Closed-evidence Qwen/template explanation layer | Grounding, attack, and ablation experiments |
| Graph learning for threat ecosystems | Typed sensor-actuator/control graph-temporal detector | Explicit topology and graph-free ablation |
| Human-AI interaction and overreliance | Operator-state model and collaboration actions | Approved controlled study |
| Trust calibration and decision support | Alternatives, uncertainty, warnings, questions, abstention | Calibration and appropriate-reliance outcomes |
| Dynamic risk assessment and explainability | Alarm/root/uncertainty evidence bundle plus verifier | Integrity ASR and clean false-alarm trade-off |
| Adversarial AI | Prediction-preserving explanation attacks | Adaptive attacker under fixed alarm |
| Critical infrastructure engineering case study | HAI and SWaT | Episode-safe, reproducible multi-dataset evaluation |
| Hybrid intelligence | Human retains the final diagnosis/response | UI workflow and no direct actuation |

## Themes not to overclaim

The supplied call does not make federated learning, differential privacy, or algorithmic
fairness mandatory. Privacy is relevant to approved human data, and expertise-group
performance should be audited, but adding federated learning or privacy noise without a
clear threat model would dilute the paper. Likewise, the project should not claim to
solve poisoning, extraction, and membership inference; its central adversary targets
the explanation channel.

## Fit condition

The project strongly fits only if the paper demonstrates all three layers together:

1. a real CPS security problem under adversarial conditions;
2. a trustworthy mechanism whose failures and abstention are measurable;
3. a genuine human decision workflow, or a transparently narrower technical paper that
   postpones human-effect claims.

An ordinary IDS plus an LLM-written description would not satisfy this standard.

