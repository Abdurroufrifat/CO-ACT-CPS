#!/usr/bin/env python3
"""Regenerate the CO-ACT-CPS manuscript figures from frozen evidence files."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIG = ROOT / "figures"
FIG.mkdir(parents=True, exist_ok=True)

BLUE = "#0072B2"
SKY = "#56B4E9"
GREEN = "#009E73"
ORANGE = "#E69F00"
VERMILLION = "#D55E00"
PURPLE = "#CC79A7"
GRAY = "#6B7280"
LIGHT = "#F3F4F6"
DARK = "#172033"


def load_json(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def setup() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.titlesize": 10,
            "axes.labelsize": 9,
            "axes.edgecolor": "#9CA3AF",
            "axes.linewidth": 0.8,
            "axes.grid": True,
            "grid.color": "#D1D5DB",
            "grid.alpha": 0.55,
            "grid.linewidth": 0.6,
            "legend.frameon": False,
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(FIG / name, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


def add_box(ax, xy, width, height, title, lines, color, *, title_color="white"):
    x, y = xy
    box = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        facecolor="white",
        edgecolor=color,
        linewidth=1.5,
    )
    ax.add_patch(box)
    header = FancyBboxPatch(
        (x, y + height - 0.085),
        width,
        0.085,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        facecolor=color,
        edgecolor=color,
        linewidth=0,
    )
    ax.add_patch(header)
    ax.text(x + width / 2, y + height - 0.043, title, ha="center", va="center",
            fontsize=9.2, fontweight="bold", color=title_color)
    ax.text(x + width / 2, y + height - 0.122, "\n".join(lines), ha="center", va="top",
            fontsize=8.1, color=DARK, linespacing=1.35)


def add_arrow(ax, start, end, color=GRAY, style="-|>", width=1.5, rad=0.0):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle=style,
            mutation_scale=11,
            linewidth=width,
            color=color,
            connectionstyle=f"arc3,rad={rad}",
        )
    )


def architecture() -> None:
    fig, ax = plt.subplots(figsize=(11.8, 5.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_box(ax, (0.03, 0.59), 0.25, 0.29, "HAI-23.05 telemetry",
            ["86 process variables", "64-row chronological windows", "No labels on operator surface"], BLUE)
    add_box(ax, (0.37, 0.59), 0.25, 0.29, "Relational temporal detector",
            ["Six-relation process graph", "Temporal self-attention", "Alarm and root-cause support"], GREEN)
    add_box(ax, (0.71, 0.59), 0.25, 0.29, "Closed evidence bundle",
            ["Alarm, causes, uncertainty", "Ranked evidence and alternatives", "Permitted diagnostic actions"], PURPLE)

    add_box(ax, (0.12, 0.12), 0.28, 0.29, "Canonical operator renderer",
            ["Deterministic summary", "Critical evidence first", "Question and action locked"], SKY, title_color=DARK)
    add_box(ax, (0.47, 0.12), 0.28, 0.29, "Independent integrity gate",
            ["Fact and set preservation", "Exact surface commitment", "VERIFIED / WARNING / ABSTAIN"], ORANGE, title_color=DARK)
    add_box(ax, (0.82, 0.12), 0.15, 0.29, "Operator",
            ["Evidence", "status", "human decision"], GREEN)

    add_arrow(ax, (0.28, 0.735), (0.37, 0.735))
    add_arrow(ax, (0.62, 0.735), (0.71, 0.735))
    add_arrow(ax, (0.84, 0.59), (0.34, 0.41), color=PURPLE, rad=-0.22)
    add_arrow(ax, (0.40, 0.265), (0.47, 0.265))
    add_arrow(ax, (0.75, 0.265), (0.82, 0.265))

    attack = FancyBboxPatch(
        (0.49, 0.435), 0.25, 0.095,
        boxstyle="round,pad=0.01,rounding_size=0.015",
        facecolor="#FFF2ED", edgecolor=VERMILLION, linewidth=1.3,
    )
    ax.add_patch(attack)
    ax.text(0.615, 0.482, "Truth-preserving rewrite attempt",
            ha="center", va="center", color=VERMILLION, fontweight="bold", fontsize=8.5)
    add_arrow(ax, (0.72, 0.48), (0.64, 0.41), color=VERMILLION, rad=0.10)
    ax.text(0.62, 0.075,
            "The generative model is treated as untrusted: integrity-critical language is accepted only when it equals the evidence-derived surface.",
            ha="center", va="center", fontsize=8.2, color=GRAY)
    save(fig, "figure_architecture.pdf")


def detector_tradeoffs() -> None:
    files = [
        "detector_temporal_initial.json",
        "detector_graph_initial.json",
        "detector_graph_recalibrated.json",
        "detector_temporal_recalibrated.json",
    ]
    labels = ["Temporal\ninitial", "Graph\ninitial", "Graph + recal.\n(primary)", "Temporal + recal."]
    metrics = [load_json(name) for name in files]
    colors = [GRAY, SKY, BLUE, GREEN]

    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.4), gridspec_kw={"wspace": 0.23})
    ax = axes[0]
    keys = ["balanced_accuracy", "f1", "attack_episode_recall", "etapr_f1"]
    names = ["Balanced\naccuracy", "Window\nF1", "Episode\nrecall", "eTaPR\nF1"]
    x = np.arange(len(keys))
    width = 0.19
    for j, (lab, color, row) in enumerate(zip(labels, colors, metrics)):
        vals = [row[k] for k in keys]
        ax.bar(x + (j - 1.5) * width, vals, width, label=lab.replace("\n", " "), color=color)
    ax.set_xticks(x, names)
    ax.set_ylim(0, 0.82)
    ax.set_ylabel("Score")
    ax.set_title("(a) Detection and episode metrics")
    ax.legend(ncol=2, loc="upper center", bbox_to_anchor=(0.5, 1.00), fontsize=7.5)

    ax = axes[1]
    x = np.arange(len(labels))
    episode = [m["attack_episode_recall"] for m in metrics]
    loc3 = [m["target_hit_at_3_detected_evaluable"] for m in metrics]
    far = [m["false_alarm_window_rate"] for m in metrics]
    ax.bar(x - 0.24, episode, 0.24, label="Episode recall", color=BLUE)
    ax.bar(x, loc3, 0.24, label="Target hit@3 (detected)", color=GREEN)
    ax.bar(x + 0.24, far, 0.24, label="False-alarm window rate", color=ORANGE)
    ax.set_xticks(x, ["Temp.\ninitial", "Graph\ninitial", "Graph\nrecal.", "Temp.\nrecal."])
    ax.set_ylim(0, 0.75)
    ax.set_ylabel("Rate")
    ax.set_title("(b) Operational trade-offs")
    ax.legend(loc="upper left", fontsize=7.5)
    for a in axes:
        a.spines[["top", "right"]].set_visible(False)
        a.set_axisbelow(True)
    fig.suptitle("Detector variants from the frozen evaluation artifacts", y=1.02,
                 fontsize=11, fontweight="bold", color=DARK)
    save(fig, "figure_detector_tradeoffs.pdf")


def calibration() -> None:
    metrics = load_json("detector_graph_recalibrated.json")
    arrays = np.load(DATA / "full_test_predictions.npz", allow_pickle=False)
    y = arrays["y"].astype(int)
    p = arrays["probabilities"].astype(float)
    edges = np.linspace(0.0, 1.0, 11)
    centers, observed, counts = [], [], []
    for i in range(10):
        if i == 9:
            mask = (p >= edges[i]) & (p <= edges[i + 1])
        else:
            mask = (p >= edges[i]) & (p < edges[i + 1])
        if mask.any():
            centers.append(float(p[mask].mean()))
            observed.append(float(y[mask].mean()))
            counts.append(int(mask.sum()))

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.15), gridspec_kw={"width_ratios": [1, 1.08], "wspace": 0.26})
    ax = axes[0]
    ax.plot([0, 1], [0, 1], "--", color=GRAY, linewidth=1.1, label="Ideal")
    ax.plot(centers, observed, "o-", color=BLUE, linewidth=1.8, markersize=5, label="Primary detector")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Mean predicted alarm probability")
    ax.set_ylabel("Observed attack fraction")
    ax.set_title("(a) Reliability by probability bin")
    ax.legend(loc="upper left")

    ax = axes[1]
    hist, bins = np.histogram(p, bins=edges)
    ax.bar((bins[:-1] + bins[1:]) / 2, hist, width=0.085, color=SKY, edgecolor=BLUE, linewidth=0.5)
    ax.set_yscale("log")
    ax.set_xlabel("Predicted alarm probability")
    ax.set_ylabel("Windows (log scale)")
    ax.set_title("(b) Prediction distribution")
    note = (f"Brier = {metrics['brier']:.3f}\n"
            f"ECE = {metrics['ece']:.3f}\n"
            f"n = {int(metrics['chronological_windows']):,}")
    ax.text(0.04, 0.96, note, transform=ax.transAxes, ha="left", va="top",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="#D1D5DB"),
            fontsize=8.2)
    for a in axes:
        a.spines[["top", "right"]].set_visible(False)
        a.set_axisbelow(True)
    fig.suptitle("Alarm probabilities remain imperfectly calibrated", y=1.02,
                 fontsize=11, fontweight="bold", color=DARK)
    save(fig, "figure_calibration.pdf")


def integrity_stages() -> None:
    controlled = load_json("integrity_controlled.json")
    adaptive = load_json("integrity_adaptive.json")

    fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.2), gridspec_kw={"wspace": 0.33})
    ax = axes[0]
    attacks = list(controlled["by_attack"])
    short = ["Omit\nevidence", "Inflate\nconfidence", "Hide\nalternatives", "Redirect\ncause"]
    values = [controlled["by_attack"][a]["integrity_detection_rate"] for a in attacks]
    ax.bar(np.arange(4), values, color=[BLUE, SKY, PURPLE, GREEN])
    ax.set_xticks(np.arange(4), short)
    ax.set_ylim(0, 1.12)
    ax.set_ylabel("Detection rate")
    ax.set_title("(a) Controlled transforms\n200 windows per attack")
    for i, v in enumerate(values):
        ax.text(i, v + 0.025, f"{v:.0%}", ha="center", fontsize=8)

    ax = axes[1]
    legacy = adaptive["verifiers"]["legacy_structural"]
    hard = adaptive["verifiers"]["hardened_decision_semantic"]
    vals = [legacy["adaptive_best_of_n_attack_success_rate"], hard["adaptive_best_of_n_attack_success_rate"]]
    ax.bar([0, 1], vals, color=[VERMILLION, GREEN])
    ax.set_xticks([0, 1], ["Legacy\nstructural", "Hardened\ndecision-semantic"])
    ax.set_ylim(0, 1.12)
    ax.set_ylabel("Best-of-6 ASR")
    ax.set_title("(b) Adaptive templates\n100 alarmed windows")
    for i, v in enumerate(vals):
        ax.text(i, v + 0.025, f"{v:.0%}", ha="center", fontsize=8)

    ax = axes[2]
    means = [controlled["mean_verification_overhead_ms"], legacy["mean_verification_overhead_ms"], hard["mean_verification_overhead_ms"]]
    p95s = [controlled["p95_verification_overhead_ms"], legacy["p95_verification_overhead_ms"], hard["p95_verification_overhead_ms"]]
    x = np.arange(3)
    ax.bar(x - 0.18, means, 0.36, label="Mean", color=BLUE)
    ax.bar(x + 0.18, p95s, 0.36, label="p95", color=ORANGE)
    ax.set_xticks(x, ["Controlled", "Adaptive\nlegacy", "Adaptive\nhardened"])
    ax.set_ylabel("Verification time (ms)")
    ax.set_title("(c) CPU verification overhead")
    ax.legend(fontsize=7.5)
    for a in axes:
        a.spines[["top", "right"]].set_visible(False)
        a.set_axisbelow(True)
    fig.suptitle("Staged explanation-integrity evaluation", y=1.03,
                 fontsize=11, fontweight="bold", color=DARK)
    save(fig, "figure_integrity_stages.pdf")


def external_redteam() -> None:
    result = load_json("external_heldout.json")["by_split"]["held_out"]
    legacy = result["verifiers"]["legacy_structural"]
    hard = result["verifiers"]["hardened_decision_semantic"]

    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.45), gridspec_kw={"width_ratios": [1.05, 0.95], "wspace": 0.28})
    ax = axes[0]
    groups = ["Candidate ASR\n(n = 318)", "Best-of-4 task ASR\n(n = 80)"]
    lvals = [legacy["candidate_attack_success_rate"], legacy["best_of_n_attack_success_rate"]]
    hvals = [hard["candidate_attack_success_rate"], hard["best_of_n_attack_success_rate"]]
    lci = [legacy["candidate_attack_success_95pct_wilson"], legacy["best_of_n_attack_success_95pct_wilson"]]
    hci = [hard["candidate_attack_success_95pct_wilson"], hard["best_of_n_attack_success_95pct_wilson"]]
    x = np.arange(2)
    width = 0.34
    ly = np.array([[v - ci[0] for v, ci in zip(lvals, lci)], [ci[1] - v for v, ci in zip(lvals, lci)]])
    hy = np.array([[v - ci[0] for v, ci in zip(hvals, hci)], [ci[1] - v for v, ci in zip(hvals, hci)]])
    ax.bar(x - width / 2, lvals, width, yerr=ly, capsize=4, color=VERMILLION, label="Legacy structural")
    ax.bar(x + width / 2, hvals, width, yerr=hy, capsize=4, color=GREEN, label="Hardened decision-semantic")
    ax.set_xticks(x, groups)
    ax.set_ylim(0, 1.02)
    ax.set_ylabel("Attack success rate")
    ax.set_title("(a) Frozen held-out Qwen3-1.7B protocol")
    ax.legend(loc="upper right", fontsize=8)
    for xpos, val in zip(x - width / 2, lvals):
        ax.text(xpos, val + 0.035, f"{val:.1%}", ha="center", fontsize=8)
    for xpos, val, ci in zip(x + width / 2, hvals, hci):
        ax.text(xpos, ci[1] + 0.035, f"{val:.1%}", ha="center", fontsize=8)

    ax = axes[1]
    status_order = ["VERIFIED", "WARNING", "ABSTAIN"]
    status_colors = [VERMILLION, ORANGE, GREEN]
    rows = [legacy["candidate_statuses"], hard["candidate_statuses"]]
    left = np.zeros(2)
    for status, color in zip(status_order, status_colors):
        vals = np.array([row[status] for row in rows])
        ax.barh([0, 1], vals, left=left, color=color, label=status)
        for yidx, (start, val) in enumerate(zip(left, vals)):
            if val >= 18:
                ax.text(start + val / 2, yidx, str(int(val)), ha="center", va="center",
                        color="white" if status != "WARNING" else DARK, fontweight="bold", fontsize=8)
        left += vals
    ax.set_yticks([0, 1], ["Legacy", "Hardened"])
    ax.invert_yaxis()
    ax.set_xlabel("Eligible candidates")
    ax.set_title("(b) Gate outcomes")
    ax.legend(ncol=3, loc="lower center", bbox_to_anchor=(0.5, -0.27), fontsize=7.5)
    ax.text(0.02, -0.47,
            "320 submitted -> 319 fact-preserving -> 318 eligible\n"
            "63 legacy-only successful tasks; 0 hardened-only; exact McNemar p = 2.17e-19",
            transform=ax.transAxes, ha="left", va="top", fontsize=8.0, color=DARK,
            bbox=dict(boxstyle="round,pad=0.35", facecolor=LIGHT, edgecolor="#D1D5DB"))
    for a in axes:
        a.spines[["top", "right"]].set_visible(False)
        a.set_axisbelow(True)
    fig.suptitle("External truth-preserving explanation red team", y=1.03,
                 fontsize=11, fontweight="bold", color=DARK)
    save(fig, "figure_external_redteam.pdf")


def episode_results() -> None:
    metrics = load_json("detector_graph_recalibrated.json")
    values = [
        metrics["attack_episode_recall"],
        metrics["target_hit_at_1_all_evaluable"],
        metrics["target_hit_at_3_all_evaluable"],
        metrics["target_hit_at_1_detected_evaluable"],
        metrics["target_hit_at_3_detected_evaluable"],
    ]
    labels = [
        "Detected\nattack episodes\n28 / 52",
        "Hit@1, all\nevaluable\n7 / 37",
        "Hit@3, all\nevaluable\n16 / 37",
        "Hit@1, detected\nevaluable\n7 / 24",
        "Hit@3, detected\nevaluable\n14 / 24",
    ]
    colors = [BLUE, GRAY, SKY, PURPLE, GREEN]
    fig, ax = plt.subplots(figsize=(9.7, 4.0))
    x = np.arange(len(values))
    ax.bar(x, values, color=colors, width=0.68)
    ax.set_xticks(x, labels)
    ax.set_ylim(0, 0.72)
    ax.set_ylabel("Rate")
    ax.set_title("Episode detection and root-cause localization on the chronological test set",
                 fontweight="bold", color=DARK)
    for i, v in enumerate(values):
        ax.text(i, v + 0.022, f"{v:.1%}", ha="center", fontsize=8.5, fontweight="bold")
    ax.text(0.99, 0.96,
            f"Median detection delay: {metrics['median_detection_delay_windows']:.0f} window\n"
            f"Mean delay: {metrics['mean_detection_delay_windows']:.2f} windows\n"
            f"False-alarm window rate: {metrics['false_alarm_window_rate']:.2%}",
            transform=ax.transAxes, ha="right", va="top", fontsize=8.2,
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="#D1D5DB"))
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_axisbelow(True)
    save(fig, "figure_episode_results.pdf")


def multimodel_utility() -> None:
    metrics = load_json("development_multimodel_v92_metrics.json")
    model_entries = list(metrics["per_model"].items())
    labels = ["Qwen3\n1.7B", "Gemma 4\n12B", "Ministral 3\n14B", "Phi-4 mini\n3.8B"]

    legacy_vals, legacy_ci, reg_vals, reg_ci = [], [], [], []
    for _, row in model_entries:
        verifiers = row["clustered_inference"]["development"]["verifiers"]
        legacy = verifiers["legacy_structural_v1"]["task_level_best_of_n_primary"]
        registered = verifiers["registered_surface_v2"]["task_level_best_of_n_primary"]
        legacy_vals.append(legacy["attack_success_rate"])
        legacy_ci.append(legacy["wilson_95pct"])
        reg_vals.append(registered["attack_success_rate"])
        reg_ci.append(registered["wilson_95pct"])

    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.35), gridspec_kw={"wspace": 0.28})
    ax = axes[0]
    x = np.arange(len(labels))
    width = 0.34
    legacy_err = np.array(
        [[v - ci[0] for v, ci in zip(legacy_vals, legacy_ci)],
         [ci[1] - v for v, ci in zip(legacy_vals, legacy_ci)]]
    )
    reg_err = np.array(
        [[v - ci[0] for v, ci in zip(reg_vals, reg_ci)],
         [ci[1] - v for v, ci in zip(reg_vals, reg_ci)]]
    )
    ax.bar(x - width / 2, legacy_vals, width, yerr=legacy_err, capsize=3,
           color=VERMILLION, label="Legacy structural")
    ax.bar(x + width / 2, reg_vals, width, yerr=reg_err, capsize=3,
           color=GREEN, label="Registered finite surface")
    ax.set_xticks(x, labels)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Task-level best-of-n ASR")
    ax.set_title("(a) Response-model variation")
    ax.legend(loc="upper center", fontsize=7.5)
    for xpos, value in zip(x - width / 2, legacy_vals):
        ax.text(xpos, value + 0.035, f"{value:.0%}", ha="center", fontsize=8)

    ax = axes[1]
    pooled = metrics["pooled"]["evaluation"]["by_split"]["development"]["verifiers"]
    gate_keys = ["legacy_structural_v1", "canonical_surface_v1", "registered_surface_v2"]
    gate_labels = ["Legacy", "Exact\ncanonical", "Registered\nfinite surface"]
    cohort_keys = ["clean", "benign", "attack"]
    cohort_labels = ["Clean acceptance", "Benign acceptance", "Attack acceptance"]
    cohort_colors = [BLUE, SKY, VERMILLION]
    x = np.arange(len(gate_keys))
    width = 0.24
    for j, (cohort, label, color) in enumerate(zip(cohort_keys, cohort_labels, cohort_colors)):
        values = [pooled[g]["by_cohort"][cohort]["verified_acceptance_rate"] for g in gate_keys]
        ax.bar(x + (j - 1) * width, values, width, color=color, label=label)
    ax.set_xticks(x, gate_labels)
    ax.set_ylim(0, 1.12)
    ax.set_ylabel("Verified acceptance rate")
    ax.set_title("(b) Security--utility separation")
    ax.legend(loc="upper center", fontsize=7.5)

    for a in axes:
        a.spines[["top", "right"]].set_visible(False)
        a.set_axisbelow(True)
    fig.suptitle("Post-freeze multi-model development stress test", y=1.02,
                 fontsize=11, fontweight="bold", color=DARK)
    save(fig, "figure_multimodel_utility.pdf")


def human_validation() -> None:
    metrics = load_json("final_human_validation_metrics.json")
    agreement = metrics["agreement_before_adjudication"]
    keys = [
        "structured_fact_consistency_yes_no_uncertain",
        "unsupported_free_text_claim_yes_no_uncertain",
        "attack_goal_adherence_1_to_5",
        "likely_operator_influence_1_to_5",
        "unsafe_delay_or_misdirection_1_to_5",
        "plausibility_and_subtlety_1_to_5",
    ]
    labels = ["Fact\nconsistency", "Unsupported\nclaim", "Goal\nadherence",
              "Likely\ninfluence", "Delay /\nmisdirection", "Plausibility /\nsubtlety"]
    raw = [agreement[k]["raw_exact_agreement"] for k in keys]
    kappas = [agreement[k].get("cohen_kappa", agreement[k].get("quadratic_weighted_kappa")) for k in keys]

    fig, axes = plt.subplots(1, 2, figsize=(11.7, 4.4), gridspec_kw={"width_ratios": [1.45, 0.8], "wspace": 0.28})
    ax = axes[0]
    x = np.arange(len(keys))
    width = 0.36
    ax.bar(x - width / 2, raw, width, color=BLUE, label="Exact agreement")
    ax.bar(x + width / 2, kappas, width, color=GREEN, label=r"$\kappa$ / quadratic-weighted $\kappa$")
    ax.set_xticks(x, labels)
    ax.set_ylim(0.80, 1.025)
    ax.set_ylabel("Agreement statistic")
    ax.set_title("(a) Two-reviewer reliability before adjudication")
    ax.legend(loc="lower right", fontsize=7.5)
    for i, (rv, kv) in enumerate(zip(raw, kappas)):
        ax.text(i - width / 2, rv + 0.006, f"{rv:.3f}", ha="center", fontsize=6.8, rotation=90)
        ax.text(i + width / 2, kv + 0.006, f"{kv:.3f}", ha="center", fontsize=6.8, rotation=90)

    ax = axes[1]
    results = metrics["final_results"]
    rows = [results["attack_sample"], results["control_sample_diagnostic"]]
    labels = ["Attack sample\n12 / 80", "Diagnostic controls\n4 / 24"]
    values = [row["item_rate"] for row in rows]
    intervals = [row["wilson_95pct"] for row in rows]
    errors = np.array(
        [[v - ci[0] for v, ci in zip(values, intervals)],
         [ci[1] - v for v, ci in zip(values, intervals)]]
    )
    ax.bar([0, 1], values, yerr=errors, capsize=5, color=[VERMILLION, GRAY], width=0.58)
    ax.set_xticks([0, 1], labels)
    ax.set_ylim(0, 0.42)
    ax.set_ylabel("Meets frozen human-validity rule")
    ax.set_title("(b) Final adjudicated text ratings")
    for i, value in enumerate(values):
        ax.text(i, value + 0.02, f"{value:.1%}", ha="center", fontsize=8.5, fontweight="bold")
    ax.text(0.5, 0.39, "Descriptive Wilson intervals\n(deterministic stratified sample)",
            ha="center", va="top", fontsize=7.5, color=DARK)

    for a in axes:
        a.spines[["top", "right"]].set_visible(False)
        a.set_axisbelow(True)
    fig.suptitle("Blinded human semantic validation", y=1.02,
                 fontsize=11, fontweight="bold", color=DARK)
    save(fig, "figure_human_validation.pdf")


def main() -> None:
    setup()
    architecture()
    detector_tradeoffs()
    calibration()
    integrity_stages()
    external_redteam()
    episode_results()
    multimodel_utility()
    human_validation()


if __name__ == "__main__":
    main()
