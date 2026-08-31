# Human-study protocol draft

This document is a planning template, not ethics approval. Submit the final protocol,
consent/debriefing materials, recruitment plan, compensation, data management plan,
and interface to the responsible ethics/IRB body before involving participants.

## Objective

Test whether verified and co-adaptive AI support improves CPS incident diagnosis and
safe response, especially when an explanation is manipulated or uncertain.

## Conditions

1. No AI.
2. Alarm probability only.
3. Generic feature-attribution/XAI summary.
4. Unverified generative explanation.
5. Verified static evidence-grounded explanation.
6. Full verified, operator-aware adaptive collaboration.

The current Streamlit prototype implements five development conditions and omits the
unverified-LLM condition. Add it only if the study is powered to compare it.

## Participants

Define the target population before recruitment. Prefer industrial-control/security
practitioners; if students are used, treat expertise as a measured moderator and avoid
generalizing directly to plant operators. Conduct a simulation-based a priori power
analysis after a small approved pilot.

## Tasks and scenarios

- Use validated HAI/SWaT-derived scenarios with the same underlying alarm across
  explanation conditions.
- Include normal, clear attack, ambiguous attack, and manipulated-explanation trials.
- Counterbalance scenario order and randomize condition assignment as permitted by the
  design.
- Prevent learning leakage by creating parallel scenarios rather than repeating the
  same obvious answer.
- No scenario may control a live physical process.

## Primary outcomes

- Correct causal diagnosis (binary or multinomial).
- Unsafe response decision (binary, defined by experts before data collection).

## Secondary outcomes

- Response time.
- Confidence and confidence calibration.
- Appropriate reliance: accepting correct support and rejecting incorrect support.
- Workload using an approved validated instrument.
- Trust using a selected validated automation/AI trust instrument.
- Evidence inspection, alternative inspection, warning response, and abstention use.

Do not invent a new trust scale unless scale development is itself part of the study.

## Logging and privacy

- Use random `P-` codes; never place names, emails, IP addresses, or free-form personal
  details in the trial CSV.
- Store the identity-to-code link separately only if the approved protocol requires it.
- Record approval reference, consent version, interface version, scenario version,
  condition propensity, and timestamps under the approved retention plan.
- Encrypt approved research data at rest and restrict access.
- Development rows marked `DEVELOPMENT_ONLY` must be deleted or isolated before the
  approved study and never analyzed as participant data.

## Analysis

- Preregister the primary model, contrasts, exclusion criteria, stopping rule, and
  multiplicity correction.
- Fit mixed-effects logistic models for diagnosis correctness and unsafe decisions,
  with participant and scenario random effects.
- Model response time with a distribution appropriate to the observed skew or a survival
  model if censoring exists.
- Report effect sizes and confidence intervals.
- Test expertise and attack presence as planned moderators rather than fishing across
  many subgroups.
- Hold out participants when evaluating the operator-state model and policy.

## Safety and deception

If participants are not told which explanations are manipulated, the protocol must
justify the deception, minimize risk, and include approved debriefing and withdrawal
procedures. Warnings should not imply that a real facility is under attack. Provide a
clear exit and researcher contact route.

## Pilot checklist

- Expert validates every ground-truth diagnosis and safe/unsafe response label.
- Median completion time fits the consented session duration.
- UI records no direct identifiers.
- Randomization and counterbalancing are reproducible.
- Manipulations are perceptible enough to affect decisions but not trivially obvious.
- Attention/comprehension checks do not reveal the hypothesis.
- Data export matches `StudyTrial` schema.
- Emergency stop and data-withdrawal procedures work.

