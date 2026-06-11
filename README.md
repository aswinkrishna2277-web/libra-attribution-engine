# ⚖️ Libra Attribution Engine

**Reference implementation of the Libra Attribution Standard (v0.3) — Module A: Corpus Apportionment.**
Methodology: **Aswin Krishna**

A recognized-contribution formula for AI training-data compensation: given a known training corpus
(works list) and a compensation pool, Libra produces a per-claim allocation schedule with disclosed
weights and rationale, rightsholder consolidation, redundancy discounting, mechanical market-exposure
scoring, mandatory sensitivity analysis, and a court/regulator-ready dossier.

*To copyright settlements what recognized-loss plans are to securities settlements.*

## Live demo

**Try it:** libra-attribution-engine.streamlit.app

## Why

In *Bartz v. Anthropic* (~$1.5B, the largest copyright recovery in U.S. history), allocation was a
flat ~$3,000 per work across ~500,000 works — and class members formally objected to its fairness,
with no principled alternative methodology to invoke. Libra is designed to be that methodology.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## CSV schema (upload your own corpus)

`work_id, title, author, rightsholder_id, text, in_print, retail_available, pub_year`

## Validation status (Standard §5)

**Validated against Libra Benchmark v1 (measurable layer):** calibration mean absolute error 0.0005
across engineered copy-fractions 0.1-0.9; false-positive baseline <= 0.0001 on independent real texts;
rightsholder consolidation and cross-process reproducibility PASS. Independent replication and
scale testing pending.

## Honest limits (Standard §2)

Libra operates only on a **known corpus** (contract, disclosure, discovery, settlement works list).
It does **not** infer what a black-box model was trained on; similarity evidences presence and weight,
never causation. The cross-claimant redundancy discount is symmetric in v1 (a provenance-priority
factor is scheduled for v2).

## Repository contents

- `libra_engine.py` - Module A engine (v0.2), spec-conformant and test-covered
- `app.py` - Streamlit interface
- `test_libra.py` - automated test suite (41 tests: unit, invariants, edge cases, end-to-end)
- `sample_works.csv`, `sample_dirty.csv`, `sample_bad.csv` - example inputs for the demo
- `requirements.txt` - dependencies

The Libra Attribution Standard specification, validation report, and supporting scholarship are
maintained separately and released on their own timeline.

## Verify the tests yourself

```bash
pip install pytest
python -m pytest test_libra.py -v
```
