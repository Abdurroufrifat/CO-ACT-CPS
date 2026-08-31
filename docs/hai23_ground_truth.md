# HAI 23.05 attack ground truth

Use `label-test1.csv` and `label-test2.csv` as the finalized binary detection
ground truth. Their contiguous positive regions contain 14 and 38 episodes,
respectively, matching the 52 scenarios documented in the official technical
manual.

Do not use the `Attacks: 40 times` line in `summary_label2.txt` as the final
episode count. That summary describes an earlier/raw collection split, while
the released `label-test2.csv` contains 38 finalized positive regions. Keep
this distinction in the experiment log because silently reporting 14 + 40
would conflict with both the released labels and the official 52-scenario
table.

Build and validate the scenario-to-target catalog with:

```powershell
python scripts/build_hai23_attack_catalog.py `
  --labels data/raw/hai_repo/hai-23.05 `
  --metadata data/processed/hai/metadata.json `
  --output data/reference/hai23_attack_catalog.csv
```

Expected output:

```text
Validated 52 finalized HAI 23.05 attack episodes
  label-test1.csv: 14 episodes
  label-test2.csv: 38 episodes
  exact target evaluable from the 86 telemetry features: 37/52
```

The exact-target denominator must be 37, not 52, when using only the 86 HAI
telemetry features. Fifteen scenarios target setpoints or internal DCS points
that are not present as named telemetry nodes. Report those separately as
hidden-target scenarios; do not count them as root-localization failures.

Source: *HAI Dataset Technical Details*, v4.0, May 31, 2023, pp. 31-32.
