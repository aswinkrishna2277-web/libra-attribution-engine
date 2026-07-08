# Libra — Test & Verification Checklist v1
**Engine v0.2 · Standard v0.3 · Suite: `test_libra.py` · Result: 41/41 PASSED**

---

## A. Automated suite — what is now proven by tests

| # | Category | What it proves | Tests | Result |
|---|---|---|---|---|
| 1 | A4 mapping table | Every metadata combination maps to exactly the published score; scoring is mechanical, never discretionary | 6 | ✅ |
| 2 | Shingling | Deterministic across calls; shingle count obeys the n−k+1 formula; short/empty text handled; case-insensitive | 5 | ✅ |
| 3 | Hand-verifiable math | Engine reproduces a pen-and-paper computable case exactly (see §B) | 3 | ✅ |
| 4 | Formula invariants | Shares sum to 100% across 10 randomized corpora and configs; floor guarantee holds even for an empty-text claim; more unique volume ⇒ strictly larger share; allocation arithmetic exact; allocations sum to the pool | 4 | ✅ |
| 5 | Consolidation | Identical same-rightsholder editions merge into one claim with uniqueness 1.0 and no volume double-count; 100% cross-claimant copy drives uniqueness to 0.0 symmetrically (documented v1 behaviour) | 2 | ✅ |
| 6 | Edge cases | Single claim allocates 100%; empty corpus raises a friendly error; invalid weights rejected; sensitivity covers all 3 parameter families | 4 | ✅ |
| 7 | End-to-end | Demo corpus engineered cases behave as designed; generated report contains every mandatory disclosure; CSV/JSON exports parse cleanly | 3 | ✅ |
| 8 | CSV hardening | Dirty metadata ("FALSE", " yes ", "nonsense", NaN, blank, None) parses to sane values — the audit's crash bug stays dead | 13 | ✅ |
| 9 | Benchmark thresholds | Benchmark v1 re-run live: MAE < 0.01, false-positive < 0.01, consolidation PASS, anthology error < 0.05 | 1 | ✅ |

Re-run anytime with: `pip install pytest && python -m pytest test_libra.py -v`

## B. Verify the core math yourself (pen and paper, 5 minutes)

This is the heart of the engine, small enough to check by hand — and the cleanest way to *know* how it works:

Claim A's text: `a b c d` · Claim B's text: `c d e f` · shingle size k = 2.

1. A's 2-word shingles: `ab, bc, cd` (three). B's: `cd, de, ef` (three).
2. Shared between claims: only `cd`. So A has 2 unique shingles of 3 → **uniqueness = 2/3 ≈ 0.667**. Same for B.
3. Effective volume = distinct shingles × uniqueness = 3 × 2/3 = **2.0** each.
4. Equal volumes, equal market metadata → equal scores. With floor 0.15 and two claims: share = 0.15/2 + 0.85 × 0.5 = **0.5 each**.

The suite asserts the engine produces exactly these numbers (`TestHandVerifiable`). If you can follow those four steps, you understand Libra's measurable layer — everything else is this, at scale, with disclosed weights.

## C. Manual checklist — run after you deploy the app

| Step | Action | Expected |
|---|---|---|
| 1 | Open the app URL | Header shows Standard v0.3, your name, validation status banner (Benchmark v1 figures) |
| 2 | Load demonstration corpus | Metrics row: 28 works → 27 claims; engineered-cases table appears |
| 3 | Check RH-005 row | 2 works, uniqueness 1.00 — consolidation protecting the editions claimant |
| 4 | Check RH-DERIV / RH-ANTH | Uniqueness well below 1; negative delta vs flat |
| 5 | Move the volume-weight slider | Allocations update; weights always sum to 1 |
| 6 | Move the floor slider to 0 then 0.5 | Smallest claims shrink/grow accordingly; totals still sum to pool |
| 7 | Expand sensitivity section | Six scenarios (weights, shingle k, floor); Spearman near 1 |
| 8 | Download all three dossier formats | Report opens; contains disclosure table, mapping table, validation status, statement of limits |
| 9 | Upload a deliberately messy CSV (blank pub_year, "FALSE" strings) | No crash; sane allocation |
| 10 | Upload a CSV missing the `text` column | Friendly error naming the missing column |

## D. How Libra works — plain language (your walkthrough)

1. You give it a **works list** — who owns what, plus the text.
2. It **consolidates**: every rightsholder's works become one claim, so nobody is penalised for their own editions.
3. Each claim's text is cut into overlapping **8-word fingerprints** (shingles), hashed cryptographically so results are identical on any machine.
4. A fingerprint appearing in *another* claimant's text is **shared**; the fraction that's unshared is the claim's **uniqueness**.
5. **Effective volume** = how much distinct content × how unique it is — the measure of contribution-as-exposure.
6. **Market exposure** comes from a published lookup table over verifiable metadata — never anyone's opinion on the day.
7. Volume and market are combined by **disclosed weights**, each carrying a written legal rationale in the report itself.
8. A **floor** — a tribunal-set parameter — guarantees every included claim its per-se share before contribution metrics apply.
9. The engine **re-runs itself under perturbed parameters** and publishes how stable the ranking is, because a method that hides its sensitivity invites Daubert death.
10. Out comes the **dossier**: allocation schedule, every assumption disclosed, validation status attached, limits stated. That honesty is the product.

## E. Known limits (unchanged, restated for the record)

Symmetric cross-claimant discount until v2's provenance-priority factor · contiguous-copy calibration only (paraphrase = Module B) · genre-dependent false-positive baselines pending Benchmark v2 · scale testing pending · normative layer (weights/floor) is disclosed policy, not an empirical claim.
