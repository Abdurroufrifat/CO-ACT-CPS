# CO-ACT-CPS anonymous EAAI manuscript (V9.2 final evidence integration)

This is the anonymous review package for *Engineering Applications of Artificial Intelligence* (EAAI). It uses Elsevier's official `elsarticle` class in single-column double-blind review format, an abstract below 250 words, four separate highlights, line numbering, author-year citations, and no author-identifying metadata. The official class and Harvard bibliography style are included so the archive compiles without relying on a particular local TeX installation.

## Compile in Overleaf

1. Upload this project ZIP to Overleaf as a new project.
2. Select `main.tex` as the main document.
3. Use pdfLaTeX. Overleaf will run BibTeX automatically; a local equivalent is `latexmk -pdf main.tex`.
4. Upload `highlights.txt` separately as the journal's Highlights item when submitting.

The compiled anonymous manuscript is `main.pdf`.

## Package contents

- `main.tex` and `sections/`: complete manuscript source.
- `references.bib`: verified bibliography with recent 2025--2026 work and foundational sources.
- `figures/`: eight vector PDF figures generated from frozen machine-readable evidence.
- `tables/`: ten reusable LaTeX tables, including a scope-aligned 2025--2026 comparison.
- `data/`: the result, protocol, prediction, topology, and checksum files required to regenerate manuscript visuals.
- `scripts/generate_figures.py`: deterministic figure-generation script.
- `highlights.txt`: four EAAI highlights.
- `main.pdf`: compiled and visually inspected anonymous manuscript.
- `SUBMISSION_CHECKLIST.md`: author-side items that cannot be inferred from the technical evidence.

## Evidence and claim boundaries

The primary held-out claim is limited to protocol `cps-truthframe-external-v1.1`, Qwen3-1.7B, 80 tasks, 320 submissions, and 318 eligible candidates. Zero observed hardened ASR is not universal robustness. The post-freeze four-model analysis reuses development tasks and is reported separately. The completed blinded review characterizes 104 deterministically stratified texts; it does not measure operator behavior or estimate population rates. The prepared HAI test array is intentionally excluded; its SHA-256 value remains in the manifest.

## Regenerate figures locally

With Python 3, NumPy, and Matplotlib installed:

```bash
python scripts/generate_figures.py
```

## Checks before journal submission

The technical manuscript and evidence integration are complete. Before submitting, the human authors must insert the applicable institutional ethics approval/exemption/determination statement, verify the competing-interest and generative-AI declarations, prepare the separate identifying title page, restore funding and CRediT details on that title page, and upload only the public publication-evidence archive as supplementary material. The private audit archive must not be published.
