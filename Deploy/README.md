# ⚖️ Libra Attribution Engine

**Reference implementation of the Libra Attribution Standard (v0.3) — Module A: Corpus Apportionment.**
Methodology: **Aswin Krishna**

A recognized-contribution formula for AI training-data compensation: given a known training corpus
(works list) and a compensation pool, Libra produces a per-claim allocation schedule with disclosed
weights and rationale, rightsholder consolidation, redundancy discounting, mechanical market-exposure
scoring, mandatory sensitivity analysis, and a court/regulator-ready dossier (USD / EUR / GBP).

*To copyright settlements what recognized-loss plans are to securities settlements.*

## Live demo

**Try it:** https://YOUR-APP-URL.streamlit.app

## Why

In *Bartz v. Anthropic* (~$1.5B, the largest copyright recovery in U.S. history), allocation was a
flat ~$3,000 per work across ~500,000 works, and class members formally objected to its fairness.
Flat per-work was a defensible choice — administrable, claim-parity — but objectors and the court
had no principled *alternative* to weigh against it. In class settlements, Libra is the objectors'
instrument: the concrete alternative that makes fairness review meaningful. In licensing pools and
collective management — its primary home — it is the distribution policy itself.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## CSV schema (upload your own corpus)

`work_id, title, author, rightsholder_id, text, in_print, retail_available, pub_year`

## Validation status (Standard §5)

**The measurable layer is validated** against Benchmark v1 (real public-domain texts, engineered
ground truth): calibration mean absolute error 0.0005 across copy-fractions 0.1–0.9; false-positive
baseline ≤ 0.0001 on independent texts; consolidation and cross-platform reproducibility PASS.
Full results: `Libra_Validation_Report.md` and `benchmark_results.json` in this repository.
**The normative layer** (weights, floor) is not "validated" — it is disclosed and contestable in
every report, by design. The benchmark is **fully reproducible end-to-end** (see below);
independent replication and scale testing remain invited and pending.

## Honest limits (Standard §2)

Libra operates only on a **known corpus** (contract, disclosure, discovery, settlement works list,
CMO repertoire). It does **not** infer what a black-box model was trained on; similarity evidences
presence and weight, never causation. The cross-claimant redundancy discount is symmetric in v1
(a provenance-priority factor is scheduled for v2).

## Repository contents

- `libra_engine.py` — Module A engine (v0.2), spec-conformant and test-covered
- `app.py` — Streamlit interface
- `test_libra.py` — automated test suite (42 tests; the benchmark re-run test auto-skips until you
  fetch the corpus per "Reproduce the benchmark" below, and a companion test verifies the published
  `benchmark_results.json` against its stated thresholds on any clean clone)
- `benchmark.py` — benchmark construction and evaluation harness (published; the validation is
  reproducible end-to-end, ground truth included)
- `Libra_Validation_Report.md` — published error characteristics (Benchmark v1)
- `benchmark_results.json` — full benchmark outputs and manifest
- `Libra_RedTeam_Memo.md` — the design record: the objections opposing counsel would raise,
  anticipated and addressed before release
- `sample_works.csv`, `sample_dirty.csv`, `sample_bad.csv` — example inputs
- `requirements.txt` — dependencies

The Libra Attribution Standard specification itself is published with the forthcoming paper.

## Verify the tests yourself

```bash
pip install pytest
python -m pytest test_libra.py -v
```
A clean clone passes 41 tests and skips 1 (the full benchmark re-run, which needs the corpus below).

## Reproduce the benchmark (end-to-end, ground truth included)

1. Download the public-domain corpus: https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/gutenberg.zip
2. Extract it so a `gutenberg/` folder (containing the .txt books) sits beside `benchmark.py`.
3. Run `python benchmark.py` — it rebuilds the engineered ground truth, re-evaluates all five
   metric families, and writes `benchmark_results.json`. Compare against the committed file;
   the run is seeded and deterministic. Then `python -m pytest test_libra.py -v` passes all 42.
