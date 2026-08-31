from __future__ import annotations

import os
import random
import time

import streamlit as st

from coact_cps.study.records import CONDITIONS, StudyTrial, append_trial, new_participant_code

SCENARIO = {
    "scenario_id": "DEV-TANK-001",
    "alarm_probability": 0.87,
    "uncertainty": 0.31,
    "verification_score": 0.91,
    "verification_status": "VERIFIED",
    "cause": "LIT101 sensor bias",
    "alternatives": ["MV101 command anomaly", "P101 state mismatch"],
    "evidence": [
        "EV-001: LIT101 changed without the expected mass-balance response.",
        "EV-002: FIT101 and FIT201 do not support the reported level jump.",
    ],
}


def visible_panel(condition: str) -> None:
    if condition == "no_ai":
        st.info("No AI support is shown in this condition.")
        return
    st.metric("AI alarm probability", f"{SCENARIO['alarm_probability']:.0%}")
    if condition == "alarm_only":
        return
    if condition == "generic_xai":
        st.write("Most influential tag: LIT101. Review the tank-level subsystem.")
        return
    st.write(f"Probable cause: **{SCENARIO['cause']}**")
    for evidence in SCENARIO["evidence"]:
        st.write(evidence)
    st.caption(
        f"Explanation gate: {SCENARIO['verification_status']} "
        f"({SCENARIO['verification_score']:.0%}); uncertainty {SCENARIO['uncertainty']:.0%}."
    )
    if condition == "coadaptive_verified":
        st.warning("Uncertainty is material. Compare alternative causes before escalation.")
        st.write("Alternatives: " + ", ".join(SCENARIO["alternatives"]))
        st.write("Operator question: Was maintenance authorized on LIT101 in this period?")


st.set_page_config(page_title="CO-ACT-CPS study prototype", layout="centered")
st.title("CO-ACT-CPS operator study prototype")
st.error(
    "Development mode uses a synthetic scenario only. Do not recruit participants or collect "
    "human data until ethics/IRB approval, consent materials, and an approved data plan exist."
)

approval = os.getenv("COACT_ETHICS_APPROVAL", "DEVELOPMENT_ONLY")
if approval == "DEVELOPMENT_ONLY":
    st.caption("Current recording label: DEVELOPMENT_ONLY")
else:
    st.success(f"Configured approval reference: {approval}")

if "participant" not in st.session_state:
    st.session_state.participant = new_participant_code()
if "condition" not in st.session_state:
    st.session_state.condition = random.choice(CONDITIONS)
if "started" not in st.session_state:
    st.session_state.started = time.monotonic()
if "trial" not in st.session_state:
    st.session_state.trial = 1

st.write(f"Anonymous development code: `{st.session_state.participant}`")
visible_panel(st.session_state.condition)

with st.form("trial"):
    diagnosis = st.selectbox(
        "Your diagnosis",
        ("LIT101 sensor bias", "MV101 command anomaly", "P101 state mismatch", "Unknown"),
    )
    response = st.radio(
        "Your next response",
        (
            "Inspect authenticated telemetry",
            "Check maintenance and command history",
            "Escalate to the responsible operator",
            "Immediately change actuator state",
        ),
    )
    confidence = st.slider("Confidence in your diagnosis", 0, 100, 50) / 100
    reliance = st.slider("How much did you rely on the AI?", 0, 100, 50) / 100
    workload = st.slider("Current mental workload", 0, 100, 50) / 100
    consent = st.checkbox(
        "I confirm this is synthetic development testing, or the configured approval is active."
    )
    submitted = st.form_submit_button("Record trial")

if submitted:
    if not consent:
        st.error("Confirm the study status before recording.")
    else:
        elapsed = time.monotonic() - st.session_state.started
        correct = int(diagnosis == SCENARIO["cause"])
        unsafe = int(response == "Immediately change actuator state")
        reward = float(correct - 1.5 * unsafe - 0.002 * min(elapsed, 300.0))
        displayed_action = {
            "no_ai": "abstain",
            "alarm_only": "explain_summary",
            "generic_xai": "show_evidence",
            "verified_static": "show_evidence",
            "coadaptive_verified": "show_alternatives",
        }[st.session_state.condition]
        trial = StudyTrial(
            participant_id=st.session_state.participant,
            trial_index=st.session_state.trial,
            scenario_id=SCENARIO["scenario_id"],
            condition=st.session_state.condition,
            alarm_probability=SCENARIO["alarm_probability"],
            explanation_uncertainty=SCENARIO["uncertainty"],
            verification_score=SCENARIO["verification_score"],
            verification_status=SCENARIO["verification_status"],
            evidence_count=len(SCENARIO["evidence"]),
            alternative_count=len(SCENARIO["alternatives"]),
            collaboration_action=displayed_action,
            diagnosis_label=diagnosis,
            diagnosis_correct=correct,
            chosen_response=response,
            unsafe_decision=unsafe,
            response_time_s=elapsed,
            self_confidence=confidence,
            reliance=reliance,
            workload=workload,
            outcome_reward=reward,
            approval_reference=approval,
        )
        append_trial("data/study/development_trials.csv", trial)
        st.success("Trial recorded locally without name or email.")
        st.session_state.trial += 1
        st.session_state.started = time.monotonic()
