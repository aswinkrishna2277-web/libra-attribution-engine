# ⚖️ Libra Attribution Engine

**Reference implementation of the Libra Attribution Standard (v0.3) — Module A: Corpus Apportionment.**
Methodology: **Aswin Krishna**

A recognized-contribution formula for AI training-data compensation: given a known training corpus
(works list) and a compensation pool, Libra produces a per-claim allocation schedule with disclosed
weights and rationale, rightsholder consolidation, redundancy discounting, mechanical market-exposure
scoring, mandatory sensitivity analysis, and a court/regulator-ready dossier.

*To copyright settlements what recognized-loss plans are to securities settlements.*

## Why
In *Bartz v. Anthropic* (~$1.5B, the largest copyright recovery in U.S. history), allocation was a
flat ~$3,000 per work across ~500,000 works — and class members formally objected to its fairness,
with no principled alternative methodology to invoke. Libra is designed to be that methodology.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy free (public URL in ~5 minutes)
1. Push this folder to a public GitHub repo.
2. Go to share.streamlit.io → New app → select the repo, branch `main`, file `app.py` → Deploy.
3. Your app is live at `https://<your-app>.streamlit.app` — link it on your CV/LinkedIn.

## CSV schema (upload your own corpus)
`work_id, title, author, rightsholder_id, text, in_print, retail_available, pub_year`

## Honest limits (Standard §2)
Libra operates only on a **known corpus** (contract, disclosure, discovery, settlement works list).
It does not infer what a black-box model was trained on; similarity evidences presence and weight,
never causation. Current status: pre-validation prototype (Standard §7 benchmark pending).

## Files
- `libra_engine.py` — Module A engine (v0.2), fully spec-conformant
- `app.py` — Streamlit interface
- Standard, red-team memo, audit report and authorities file accompany the engine.
