from __future__ import annotations

import argparse
import csv
import json
import zipfile
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

DETECTOR_FILES = {
    "Base detector": "artifacts/hai_medium/full_test_metrics.json",
    "Score recalibrated": "artifacts/hai_recalibrated/full_test_metrics.json",
    "Process graph": "artifacts/hai_process_graph/full_test_metrics.json",
    "Process graph + recal.": (
        "artifacts/hai_process_graph_recalibrated/full_test_metrics.json"
    ),
}


def read_json(archive: zipfile.ZipFile, path: str) -> dict[str, Any]:
    value = json.loads(archive.read(path))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value


def pct(value: float) -> str:
    return f"{100.0 * value:.2f}"


def number(value: float, digits: int = 3) -> str:
    return f"{value:.{digits}f}"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows supplied for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def detector_rows(metrics: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    fields = (
        "balanced_accuracy",
        "f1",
        "roc_auc",
        "average_precision",
        "attack_episode_recall",
        "mean_detection_delay_windows",
        "false_alarm_window_rate",
        "target_hit_at_3_all_evaluable",
        "etapr_f1",
        "ece",
    )
    return [
        {"variant": variant, **{field: values[field] for field in fields}}
        for variant, values in metrics.items()
    ]


def write_detector_tex(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Detector performance on the complete chronological HAI test split. "
        r"Delay is measured in prepared windows and FAWR denotes false-alarm window rate.}",
        r"\label{tab:detector_variants}",
        r"\small",
        r"\setlength{\tabcolsep}{3.5pt}",
        r"\begin{tabular}{lrrrrrrrrrr}",
        r"\toprule",
        r"Variant & Bal. Acc. & F1 & ROC-AUC & AP & Ep. Recall & Delay & FAWR & "
        r"Hit@3 & eTaPR-F1 & ECE \\",
        r"\midrule",
    ]
    for row in rows:
        lines.append(
            "{} & {} & {} & {} & {} & {} & {} & {} & {} & {} & {} \\\\".format(
                row["variant"],
                number(row["balanced_accuracy"]),
                number(row["f1"]),
                number(row["roc_auc"]),
                number(row["average_precision"]),
                number(row["attack_episode_recall"]),
                number(row["mean_detection_delay_windows"]),
                number(row["false_alarm_window_rate"], 4),
                number(row["target_hit_at_3_all_evaluable"]),
                number(row["etapr_f1"]),
                number(row["ece"]),
            )
        )
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{table*}", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def write_integrity_tables(
    csv_path: Path,
    tex_path: Path,
    controlled: dict[str, Any],
    adaptive: dict[str, Any],
) -> None:
    rows: list[dict[str, Any]] = []
    for attack, values in controlled["by_attack"].items():
        rows.append(
            {
                "evaluation": "Controlled",
                "attack": attack,
                "cases": controlled["windows"],
                "legacy_asr": "",
                "hardened_asr": values["manipulation_attack_success_rate"],
                "integrity_detection_rate": values["integrity_detection_rate"],
                "clean_rejection_rate": controlled["clean_explanation_false_alarm_rate"],
            }
        )
    legacy = adaptive["verifiers"]["legacy_structural"]
    hardened = adaptive["verifiers"]["hardened_decision_semantic"]
    for attack in adaptive["strategies"]:
        rows.append(
            {
                "evaluation": "Adaptive",
                "attack": attack,
                "cases": adaptive["evaluated_alarmed_windows"],
                "legacy_asr": legacy["by_strategy"][attack]["attack_success_rate"],
                "hardened_asr": hardened["by_strategy"][attack]["attack_success_rate"],
                "integrity_detection_rate": 1.0
                - hardened["by_strategy"][attack]["attack_success_rate"],
                "clean_rejection_rate": hardened["clean_explanation_rejection_rate"],
            }
        )
    write_csv(csv_path, rows)

    lines = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Explanation-integrity evaluation under controlled and adaptive "
        r"truth-preserving transformations. A dash indicates that the controlled "
        r"experiment evaluated only the configured hardened verifier.}",
        r"\label{tab:integrity_attacks}",
        r"\small",
        r"\begin{tabular}{llrrrr}",
        r"\toprule",
        r"Evaluation & Attack strategy & Cases & Legacy ASR (\%) & Hardened ASR (\%) & "
        r"Clean rejection (\%) \\",
        r"\midrule",
    ]
    for row in rows:
        legacy_text = "--" if row["legacy_asr"] == "" else pct(float(row["legacy_asr"]))
        lines.append(
            "{} & {} & {} & {} & {} & {} \\\\".format(
                row["evaluation"],
                str(row["attack"]).replace("_", r"\_"),
                row["cases"],
                legacy_text,
                pct(float(row["hardened_asr"])),
                pct(float(row["clean_rejection_rate"])),
            )
        )
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{table*}", ""])
    tex_path.write_text("\n".join(lines), encoding="utf-8")


def redteam_rows(
    pre: dict[str, Any], development: dict[str, Any], heldout: dict[str, Any]
) -> list[dict[str, Any]]:
    pre_split = pre["by_split"]["development"]
    dev_split = development["by_split"]["development"]
    test_split = heldout["by_split"]["held_out"]
    result = []
    for phase, split, verifier_name in (
        ("Development pre-hardening", pre_split, "hardened_decision_semantic"),
        ("Development post-hardening", dev_split, "hardened_decision_semantic"),
        ("Held-out frozen", test_split, "hardened_decision_semantic"),
    ):
        legacy = split["verifiers"]["legacy_structural"]
        hardened = split["verifiers"][verifier_name]
        result.append(
            {
                "phase": phase,
                "tasks": split["tasks"],
                "submitted_candidates": split["submitted_candidates"],
                "eligible_candidates": split["valid_truth_preserving_candidates"],
                "legacy_candidate_asr": legacy["candidate_attack_success_rate"],
                "hardened_candidate_asr": hardened["candidate_attack_success_rate"],
                "legacy_best_of_n_asr": legacy["best_of_n_attack_success_rate"],
                "hardened_best_of_n_asr": hardened["best_of_n_attack_success_rate"],
                "clean_rejection_rate": hardened["clean_explanation_rejection_rate"],
                "mcnemar_p": split["paired_defense_test"]["exact_mcnemar_p_value"],
            }
        )
    return result


def write_redteam_tex(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{External Qwen3-1.7B truth-preserving explanation red-team results. "
        r"The frozen held-out split is the primary evaluation. ASR is automatically "
        r"computed over eligible surface-changing candidates.}",
        r"\label{tab:external_redteam}",
        r"\scriptsize",
        r"\setlength{\tabcolsep}{3pt}",
        r"\begin{tabular}{lrrrrrrrr}",
        r"\toprule",
        r"Phase & Tasks & Eligible & Legacy cand. & Hardened cand. & Legacy best-$n$ & "
        r"Hardened best-$n$ & Clean reject. & $p$ \\",
        r"\midrule",
    ]
    for row in rows:
        p_value = row["mcnemar_p"]
        p_text = f"{p_value:.2e}" if p_value < 0.001 else f"{p_value:.3f}"
        lines.append(
            "{} & {} & {} & {} & {} & {} & {} & {} & {} \\\\".format(
                row["phase"],
                row["tasks"],
                row["eligible_candidates"],
                pct(row["legacy_candidate_asr"]),
                pct(row["hardened_candidate_asr"]),
                pct(row["legacy_best_of_n_asr"]),
                pct(row["hardened_best_of_n_asr"]),
                pct(row["clean_rejection_rate"]),
                p_text,
            )
        )
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{table*}", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def configure_matplotlib() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.labelsize": 9,
            "axes.titlesize": 10,
            "legend.fontsize": 8,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.linewidth": 0.8,
            "savefig.bbox": "tight",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def save_figure(fig: plt.Figure, base: Path) -> None:
    base.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(base.with_suffix(".pdf"))
    fig.savefig(base.with_suffix(".svg"))
    fig.savefig(base.with_suffix(".png"), dpi=600)
    plt.close(fig)


def plot_detector(metrics: dict[str, dict[str, Any]], base: Path) -> None:
    metric_keys = (
        "roc_auc",
        "average_precision",
        "attack_episode_recall",
        "target_hit_at_3_all_evaluable",
        "etapr_f1",
    )
    labels = ("ROC-AUC", "Average\nprecision", "Episode\nrecall", "Target\nhit@3", "eTaPR-F1")
    variants = list(metrics)
    colors = ("#4C78A8", "#F58518", "#54A24B", "#B279A2")
    x = np.arange(len(metric_keys))
    width = 0.19
    fig, ax = plt.subplots(figsize=(7.2, 3.8), constrained_layout=True)
    for index, variant in enumerate(variants):
        values = [metrics[variant][key] for key in metric_keys]
        offset = (index - (len(variants) - 1) / 2.0) * width
        ax.bar(x + offset, values, width, label=variant, color=colors[index])
    ax.set_ylabel("Score")
    ax.set_xticks(x, labels)
    ax.set_ylim(0.0, 0.85)
    ax.grid(axis="y", color="#D9D9D9", linewidth=0.6, alpha=0.8)
    ax.set_axisbelow(True)
    ax.legend(ncol=2, frameon=False, loc="upper left")
    save_figure(fig, base)


def plot_redteam(heldout: dict[str, Any], base: Path) -> None:
    split = heldout["by_split"]["held_out"]
    legacy = split["verifiers"]["legacy_structural"]
    hardened = split["verifiers"]["hardened_decision_semantic"]
    categories = ("Candidate-level", "Best-of-4 task")
    values = np.array(
        [
            [legacy["candidate_attack_success_rate"], legacy["best_of_n_attack_success_rate"]],
            [
                hardened["candidate_attack_success_rate"],
                hardened["best_of_n_attack_success_rate"],
            ],
        ]
    )
    intervals = (
        (
            legacy["candidate_attack_success_95pct_wilson"],
            legacy["best_of_n_attack_success_95pct_wilson"],
        ),
        (
            hardened["candidate_attack_success_95pct_wilson"],
            hardened["best_of_n_attack_success_95pct_wilson"],
        ),
    )
    colors = ("#4C78A8", "#F58518")
    labels = ("Legacy structural", "Canonical hardened")
    x = np.arange(len(categories))
    width = 0.34
    fig, ax = plt.subplots(figsize=(6.4, 3.8), constrained_layout=True)
    for verifier_index in range(2):
        positions = x + (verifier_index - 0.5) * width
        lower = []
        upper = []
        for category_index in range(2):
            center = values[verifier_index, category_index]
            interval = intervals[verifier_index][category_index]
            lower.append(center - interval[0])
            upper.append(interval[1] - center)
        bars = ax.bar(
            positions,
            100.0 * values[verifier_index],
            width,
            yerr=100.0 * np.array([lower, upper]),
            capsize=4,
            label=labels[verifier_index],
            color=colors[verifier_index],
            error_kw={"elinewidth": 1.0, "capthick": 1.0},
        )
        for bar, value, upper_error in zip(bars, values[verifier_index], upper, strict=True):
            label_y = 100.0 * (value + upper_error) + 2.0
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                label_y,
                f"{100.0 * value:.1f}%",
                ha="center",
                va="bottom",
                fontsize=8,
            )
    ax.set_ylabel("Attack success rate (%)")
    ax.set_xticks(x, categories)
    ax.set_ylim(0.0, 100.0)
    ax.grid(axis="y", color="#D9D9D9", linewidth=0.6, alpha=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="upper right")
    ax.text(
        0.01,
        0.96,
        r"Exact McNemar $p=2.17\times10^{-19}$; clean rejection = 0%",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=8,
    )
    save_figure(fig, base)


def write_results_text(
    markdown_path: Path,
    latex_path: Path,
    detector: dict[str, dict[str, Any]],
    heldout: dict[str, Any],
    manifest: dict[str, Any],
) -> None:
    base = detector["Base detector"]
    final = detector["Process graph + recal."]
    split = heldout["by_split"]["held_out"]
    legacy = split["verifiers"]["legacy_structural"]
    hardened = split["verifiers"]["hardened_decision_semantic"]
    p_value = split["paired_defense_test"]["exact_mcnemar_p_value"]
    freeze_id = manifest["freeze_id"]
    markdown = f"""# Frozen publication results

Freeze identifier: `{freeze_id}`

## Detector results

On the complete 4,443-window chronological HAI test split, the final process-graph model
achieved ROC-AUC {final['roc_auc']:.3f}, average precision {final['average_precision']:.3f},
attack-episode recall {final['attack_episode_recall']:.3f}, and eTaPR-F1
{final['etapr_f1']:.3f}. Relative to the base detector, ROC-AUC increased from
{base['roc_auc']:.3f} to {final['roc_auc']:.3f} and episode recall increased from
{base['attack_episode_recall']:.3f} to {final['attack_episode_recall']:.3f}. This gain
coincided with a higher false-alarm window rate ({base['false_alarm_window_rate']:.4f} to
{final['false_alarm_window_rate']:.4f}) and worse ECE ({base['ece']:.3f} to
{final['ece']:.3f}), which must be reported as a detection-calibration trade-off.

## Primary external red-team result

The frozen held-out evaluation contained {split['tasks']} tasks and
{split['submitted_candidates']} Qwen3-1.7B candidates. After excluding one fact-changing
candidate and one no-op, {split['valid_truth_preserving_candidates']} candidates were
eligible. The legacy verifier accepted {legacy['candidate_statuses']['VERIFIED']} candidates
({100*legacy['candidate_attack_success_rate']:.2f}%) and had a best-of-four task ASR of
{100*legacy['best_of_n_attack_success_rate']:.2f}%. The canonical hardened verifier accepted
none, with 95% Wilson upper bounds of
{100*hardened['candidate_attack_success_95pct_wilson'][1]:.2f}% at candidate level and
{100*hardened['best_of_n_attack_success_95pct_wilson'][1]:.2f}% at task level. Clean
rejection remained 0%, and the paired exact McNemar test gave p = {p_value:.3e}.

## Required interpretation limits

- The zero observed hardened ASR applies to this frozen HAI/Qwen3-1.7B protocol; it is not
  evidence of universal robustness.
- The canonical surface is a secure-by-construction policy that intentionally constrains
  free-form operator wording. The zero ASR should be interpreted together with this utility
  trade-off, not as a learned semantic detector outperforming every possible attacker.
- Automatic eligibility establishes committed-fact preservation and a material surface
  change, not harmful decision influence. Blinded human/domain-expert review remains needed.
- The external evaluation uses one relatively small open model. Stronger-model and
  cross-dataset analyses should be reported as separately frozen sensitivity studies.
- eTaPR values were computed at the prepared window resolution and should not be compared
  directly with raw-second studies without a matched-stride evaluation.
"""
    markdown_path.write_text(markdown, encoding="utf-8")

    latex = rf"""\subsection{{Frozen Evaluation Results}}
On the complete chronological HAI test split (4,443 prepared windows), the final
process-graph model achieved a ROC--AUC of {final['roc_auc']:.3f}, average precision of
{final['average_precision']:.3f}, attack-episode recall of
{final['attack_episode_recall']:.3f}, and eTaPR-F1 of {final['etapr_f1']:.3f}. Relative to
the base detector, ROC--AUC increased from {base['roc_auc']:.3f} to
{final['roc_auc']:.3f}, while attack-episode recall increased from
{base['attack_episode_recall']:.3f} to {final['attack_episode_recall']:.3f}. These gains
were accompanied by a higher false-alarm window rate
({base['false_alarm_window_rate']:.4f} versus {final['false_alarm_window_rate']:.4f}) and
worse expected calibration error ({base['ece']:.3f} versus {final['ece']:.3f}).

The primary frozen external red-team evaluation comprised {split['tasks']} held-out tasks
and {split['submitted_candidates']} Qwen3-1.7B candidates. After excluding one
fact-changing response and one no-op, {split['valid_truth_preserving_candidates']}
candidates were eligible. The legacy structural verifier accepted
{legacy['candidate_statuses']['VERIFIED']} candidates
({100*legacy['candidate_attack_success_rate']:.2f}\%) and exhibited a best-of-four task
attack-success rate of {100*legacy['best_of_n_attack_success_rate']:.2f}\%. The canonical
hardened verifier accepted no eligible candidate, with 95\% Wilson upper bounds of
{100*hardened['candidate_attack_success_95pct_wilson'][1]:.2f}\% at candidate level and
{100*hardened['best_of_n_attack_success_95pct_wilson'][1]:.2f}\% at task level. Clean
rejection remained zero. The paired exact McNemar test was significant
($p={p_value:.3e}$).

These results are bounded to the frozen HAI/Qwen3-1.7B protocol. Canonical rendering is a
secure-by-construction constraint on operator-facing wording rather than a universal
semantic detector. Moreover, automatic eligibility verifies committed facts and a
material surface change but does not establish harmful decision influence; blinded
human/domain-expert review remains necessary. eTaPR is reported at the prepared window
resolution and is not directly comparable with raw-second evaluations.
"""
    latex_path.write_text(latex, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build paper-ready frozen results artifacts")
    parser.add_argument("--evidence-zip", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    output = Path(args.output_dir)
    tables = output / "tables"
    figures = output / "figures"
    latex = output / "latex"
    for directory in (tables, figures, latex):
        directory.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(args.evidence_zip) as archive:
        manifest = read_json(archive, "final_reproducibility_manifest.json")
        detector = {name: read_json(archive, path) for name, path in DETECTOR_FILES.items()}
        controlled = read_json(
            archive, "artifacts/hai_process_graph_recalibrated/integrity_metrics.json"
        )
        adaptive = read_json(
            archive,
            "artifacts/hai_process_graph_recalibrated/adaptive_integrity_metrics.json",
        )
        pre = read_json(
            archive,
            "artifacts/hai_external_redteam/development_qwen17b_metrics_pre_hardening.json",
        )
        development = read_json(
            archive,
            "artifacts/hai_external_redteam/development_qwen17b_hardened_metrics.json",
        )
        heldout = read_json(
            archive, "artifacts/hai_external_redteam/heldout_qwen17b_hardened_metrics.json"
        )

    d_rows = detector_rows(detector)
    write_csv(tables / "detector_variants.csv", d_rows)
    write_detector_tex(latex / "table_detector_variants.tex", d_rows)
    write_integrity_tables(
        tables / "explanation_integrity.csv",
        latex / "table_explanation_integrity.tex",
        controlled,
        adaptive,
    )
    r_rows = redteam_rows(pre, development, heldout)
    write_csv(tables / "external_redteam.csv", r_rows)
    write_redteam_tex(latex / "table_external_redteam.tex", r_rows)

    configure_matplotlib()
    plot_detector(detector, figures / "figure_detector_tradeoffs")
    plot_redteam(heldout, figures / "figure_external_redteam_asr")
    write_results_text(
        output / "FROZEN_RESULTS_INTERPRETATION.md",
        latex / "results_section.tex",
        detector,
        heldout,
        manifest,
    )
    captions = r"""\paragraph{Figure captions.}
\textbf{Figure 1.} Detector-stage comparison on the complete chronological HAI test split.
All measures use the prepared window resolution. The process graph improves ranking and
episode sensitivity, while calibration and false alarms remain explicit trade-offs.

\textbf{Figure 2.} Frozen held-out truth-preserving explanation red team. Bars show observed
attack-success rates and error bars show 95\% Wilson intervals. The canonical hardened
operator surface admits no eligible candidate while rejecting no clean explanation.
"""
    (latex / "figure_captions.tex").write_text(captions, encoding="utf-8")
    print(f"Saved paper-ready results to {output.resolve()}")


if __name__ == "__main__":
    main()
