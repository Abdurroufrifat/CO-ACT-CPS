# CO-ACT-CPS V9.2 GitHub publication update

This package is designed to be extracted directly into the root of the existing `CO-ACT-CPS` repository. It contains only public, publication-safe files.

## Included

- `manuscript/eaai_v92/`: complete anonymous Elsevier/EAAI LaTeX project, figures, tables, machine-readable manuscript data, highlights, submission checklist, and compiled PDF.
- `artifacts/publication_v92/`: final public publication-evidence archive.
- `docs/PUBLICATION_STATUS_V92.md`: concise project status and claim boundaries.
- `docs/GITIGNORE_PRIVATE_AUDIT_SNIPPET.txt`: recommended protection against accidentally committing private audit material.

## Explicitly excluded

The private audit archive, private item key, identifying reviewer/adjudicator evidence, and original private workbooks are not included. Never copy those files into a public GitHub repository.

## Commit from VS Code

Open the repository folder in VS Code, open its PowerShell terminal, and run:

```powershell
git status --short
git add manuscript/eaai_v92 artifacts/publication_v92 docs/PUBLICATION_STATUS_V92.md docs/GITIGNORE_PRIVATE_AUDIT_SNIPPET.txt README_GITHUB_UPDATE.md
git diff --cached --stat
git commit -m "Add V9.2 manuscript and public publication evidence"
git push origin main
```

Before committing, confirm that no filename containing `Private-Audit`, `PRIVATE_item_key`, or identifying independence evidence appears in `git status --short`.
