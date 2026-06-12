# ⚖️ Libra Attribution Engine

**Reference implementation of the Libra Attribution Standard (v0.3) — Module A: Corpus Apportionment.**
Methodology: **Aswin Krishna**

A recognized-contribution formula for AI training-data compensation: given a known training corpus
(works list) and a compensation pool, Libra produces a per-claim allocation schedule with disclosed
weights and rationale, rightsholder consolidation, redundancy discounting, mechanical market-exposure
scoring, mandatory sensitivity analysis, and a court/regulator-ready dossier (USD / EUR / GBP).

*To copyright settlements what recognized-loss plans are to securities settlements.*

## Live demo

**Try it:** https://libra-attribution-engine.streamlit.app/

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
Full results: `Libra_Validation_Report.md` in this repository. **The normative layer** (weights,
floor) is not "validated" — it is disclosed and contestable in every report, by design.
Independent replication and scale testing pending; replication access available on request.

## Honest limits (Standard §2)

Libra operates only on a **known corpus** (contract, disclosure, discovery, settlement works list,
CMO repertoire). It does **not** infer what a black-box model was trained on; similarity evidences
presence and weight, never causation. The cross-claimant redundancy discount is symmetric in v1
(a provenance-priority factor is scheduled for v2).

## Repository contents

- `libra_engine.py` — Module A engine (v0.2), spec-conformant and test-covered
- `app.py` — Streamlit interface
- `test_libra.py` — automated test suite (42 tests; one auto-skips in this
  public distribution, since the benchmark *construction* module is proprietary — its published
  results are in the Validation Report, and replication access is available on request)
- `Libra_Validation_Report.md` — published error characteristics (Benchmark v1)
- `benchmark_results.json` — full benchmark outputs and manifest (results published; construction module proprietary)
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
