# CO-ACT-CPS frozen publication results

This package contains paper-ready outputs generated from freeze
`60b263ab81ea46ad0e4057c0eaac93471d389a39983f2deed9b2ae1e1034bf22`.

## Contents

- `figures/`: PDF, SVG, and 600-dpi PNG versions of two verified figures.
- `tables/`: source CSV tables containing the exact frozen numeric values.
- `latex/`: three `booktabs` tables, figure captions, and a results-section draft.
- `FROZEN_RESULTS_INTERPRETATION.md`: evidence-bounded interpretation and limitations.
- `FREEZE_VERIFICATION.md`: manifest, archive, and checksum validation.
- `reproducibility/build_frozen_publication_results.py`: generation script.
- `reproducibility/final_reproducibility_manifest.json`: source freeze identity.

The LaTeX tables require `\usepackage{booktabs}`. The supplied tables were compiled in a
two-column article during quality assurance with no overfull boxes. Both figure PDFs were
rendered to PNG and visually checked for clipping, overlap, and legibility.
