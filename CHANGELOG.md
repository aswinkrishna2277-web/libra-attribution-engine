# Changelog

All notable changes to the Libra Attribution Engine are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/) and the
project adheres to semantic versioning.

## [Unreleased]

### Added
- **Length-normalised exposure measure** (`--measure per-work`). The default
  `per-word` basis weights a claim's distinctive text by volume; the new
  `per-work` basis counts each constituent work by its distinctiveness
  independent of length, so a short highly-distinctive work is not diluted by
  page count. A disclosed, contestable policy choice, substitutable under the
  same protocol; the active basis is recorded in every report (markdown + JSON).


### Added
- Command-line interface (`libra`): `score`, `sensitivity`, and `demo`
  subcommands with `--k`, `--w-volume`, `--floor`, `--pool`, `--currency`,
  and `md`/`csv`/`json` output formats.
- Corpus loading from CSV, JSON, and JSONL, with inline `text` or per-work
  `text_path` file references and strict validation of required columns.
- Packaging via `pyproject.toml`: `pip install .` provides the `libra`
  console command; optional extras `[app]` (Streamlit UI) and `[dev]`
  (pytest, ruff).
- Continuous integration (GitHub Actions): lint + test matrix on Python
  3.10–3.12, with and without the UI dependency, plus a CLI smoke test.
- Test-suite hardening: UI-dependent tests are skipped automatically when
  Streamlit is not installed, so the core engine suite always runs.

## [0.2.0] — 2026-06-12

### Added
- Rightsholder-claim consolidation before the redundancy discount.
- Market-exposure as a mechanical mapping from verifiable metadata.
- Sensitivity analysis over weights and technical parameters (k, floor).
- Validation-status disclosure in every report.
- Cryptographic stable shingle hashing for cross-platform reproducibility.
- Synthetic-metadata disclosure when demonstration data is used.

## [0.1.0] — 2026 (initial public release)

- Deterministic two-stage apportionment engine, Streamlit demo,
  benchmark, and test suite.
