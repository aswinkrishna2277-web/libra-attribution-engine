# Phase 1 hardening — what this adds and how to apply it

New files to commit at the ROOT of the repository:
- `cli.py` — the `libra` command-line interface
- `pyproject.toml` — packaging; `pip install .` gives you the `libra` command
- `CHANGELOG.md`
- `.github/workflows/ci.yml` — CI: lint + tests on Python 3.10/3.11/3.12 + CLI smoke test

Modified file (replace your existing one):
- `test_libra.py` — UI tests now skip automatically when Streamlit is absent

Apply:
1. Copy all files into your local clone, preserving the `.github/workflows/` path.
2. `git add -A && git commit -m "Add CLI, packaging, CI; harden test suite" && git push`
3. On GitHub → Actions tab: the CI run should appear and go green.

Local use after install (`pip install -e ".[dev,app]"`):
    libra demo                          # run the built-in demonstration corpus
    libra score corpus.csv --pool 1500000 --format md -o report.md
    libra score corpus.jsonl --w-volume 0.6 --floor 0.10 --format json
    libra sensitivity corpus.csv

Corpus input format (CSV/JSON/JSONL), columns:
    work_id, title, author, rightsholder_id, text (or text_path),
    in_print, retail_available, pub_year, notes
