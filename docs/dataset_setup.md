# Dataset setup and leakage checklist

## HAI 23.05

Official source: <https://github.com/icsdataset/hai>

The official repository describes HAI as a hardware-in-the-loop ICS dataset joining
boiler, turbine, water-treatment, and simulated processes. Version 23.05 contains four
normal training files, two attack test files, separate detailed label files, and graph
resources. Recent versions require Git LFS.

### Download in PowerShell

```powershell
git lfs install
git clone https://github.com/icsdataset/hai.git data/raw/hai_repo
Push-Location data/raw/hai_repo
git lfs pull
Pop-Location
```

Check that the downloaded CSV files contain real comma-separated rows and are not tiny
Git LFS pointer files:

```powershell
Get-Item data/raw/hai_repo/hai-23.05/*.csv | Select-Object Name,Length
```

### Inspect and prepare

```powershell
python scripts/inspect_dataset.py data/raw/hai_repo/hai-23.05/hai-train1.csv
Copy-Item configs/hai_template.yaml configs/hai.yaml
python scripts/prepare_dataset.py --config configs/hai.yaml
```

Check `data/processed/hai/metadata.json` and pin `features` in `configs/hai.yaml` before
final runs. Exclude timestamps, free text, global labels, process labels, and any field
derived from the attack annotation.

The generic adapter uses the `attack` column for binary labels. Detailed causal/root
labels are not guessed. Build a separate reviewed mapping from the official
`label-test*.csv` and summary files if root-cause evaluation is required.

### Required HAI checks

- Preserve file and time order.
- Treat overlapping windows from one attack episode as one statistical group.
- Fit scaling on training-normal rows only.
- Calibrate thresholds on validation-normal rows only.
- Keep every test file and attack episode out of model selection.
- Use the official HAI eTaPR evaluation in final reporting.
- Record the repository commit hash and exact dataset version.
- Review the supplied graph resources and technical manual; do not publish the
  fully-connected fallback as the proposed topology.

## SWaT

Official pages:

- Characteristics: <https://www.sutd.edu.sg/itrust/itrust-labs/datasets/dataset-characteristics/swat/>
- Request: <https://www.sutd.edu.sg/itrust/request-for-datasets/>
- Terms: <https://www.sutd.edu.sg/itrust/itrust-labs/datasets/terms-of-usage/>

Request the dataset using your institution's details and follow the supplied terms.
Requests may take several working days. This repository does not contain or
redistribute SWaT.

Place authorized CSVs as follows:

```text
data/raw/swat/
├── normal/
│   └── your_normal_file.csv
└── attack/
    └── your_attack_file.csv
```

Then run:

```powershell
python scripts/inspect_dataset.py data/raw/swat/normal/your_normal_file.csv
python scripts/inspect_dataset.py data/raw/swat/attack/your_attack_file.csv
Copy-Item configs/swat_template.yaml configs/swat.yaml
code configs/swat.yaml
python scripts/prepare_dataset.py --config configs/swat.yaml
```

SWaT releases differ in file names, whitespace, timestamp formatting, and label values.
The template assumes a `Normal/Attack` column and `Normal` as the normal value; change
these only after inspection.

## Topology construction

The final graph should use separate edge types:

- `physical`: upstream/downstream flow and material/energy coupling;
- `control`: sensor-to-controller and controller-to-actuator dependencies;
- `communication`: only when supported by network/control documentation;
- `same_stage`: optional, declared engineering relation within one process stage.

The order of `topology.nodes` must exactly match the configured feature list. Example:

```yaml
dataset:
  features: [LIT101, MV101, FIT101, P101]

topology:
  nodes: [LIT101, MV101, FIT101, P101]
  relations:
    control:
      - [LIT101, MV101]
      - [LIT101, P101]
    physical:
      - [MV101, FIT101]
      - [FIT101, LIT101]
```

Document every edge source. Use the fully-connected graph only as a baseline.

## Physics and operational invariants

The current code supports a simple mass-balance residual:

```yaml
physics_invariants:
  - kind: mass_balance
    state_node: LIT101
    inflow_node: FIT101
    outflow_node: FIT201
    coefficient: 0.0018
```

The coefficient depends on sampling rate, scaling, and tank geometry. Estimate it on
training-normal data or derive it from process documentation; never copy the synthetic
coefficient into HAI/SWaT. Store units and estimation procedure.

## Data validation report to create

For each dataset, save a versioned report containing:

- cryptographic hashes of source files;
- row counts, time range, sampling interval, gaps, duplicates, and missingness;
- feature names/types/ranges and excluded columns;
- normal and attack episode counts/durations;
- split boundaries and episode IDs;
- scaler statistics fit source;
- topology edge counts/types and invariant definitions;
- label corrections, with rationale and reviewer initials;
- license/terms and citation.

## Common leakage failures

- Randomly splitting overlapping windows.
- Scaling before splitting.
- Choosing a threshold from test attack labels.
- Concatenating files and letting a window cross a file boundary.
- Treating an attack annotation or target description as an input feature.
- Generating root-cause labels from the model's own prediction.
- Tuning verifier rules on the same explanation attacks used for final testing.

The adapter windows each source file independently and stores a source-file group for
every window. Detailed attack episode IDs still need to be derived from the official
labels for episode-grouped evaluation and resampling.
