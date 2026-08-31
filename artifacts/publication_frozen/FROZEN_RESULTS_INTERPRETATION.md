# Frozen publication results

Freeze identifier: `60b263ab81ea46ad0e4057c0eaac93471d389a39983f2deed9b2ae1e1034bf22`

## Detector results

On the complete 4,443-window chronological HAI test split, the final process-graph model
achieved ROC-AUC 0.758, average precision 0.376,
attack-episode recall 0.538, and eTaPR-F1
0.457. Relative to the base detector, ROC-AUC increased from
0.688 to 0.758 and episode recall increased from
0.231 to 0.538. This gain
coincided with a higher false-alarm window rate (0.0047 to
0.0121) and worse ECE (0.167 to
0.246), which must be reported as a detection-calibration trade-off.

## Primary external red-team result

The frozen held-out evaluation contained 80 tasks and
320 Qwen3-1.7B candidates. After excluding one fact-changing
candidate and one no-op, 318 candidates were
eligible. The legacy verifier accepted 177 candidates
(55.66%) and had a best-of-four task ASR of
78.75%. The canonical hardened verifier accepted
none, with 95% Wilson upper bounds of
1.19% at candidate level and
4.58% at task level. Clean
rejection remained 0%, and the paired exact McNemar test gave p = 2.168e-19.

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
