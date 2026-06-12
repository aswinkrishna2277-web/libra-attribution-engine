# Libra Attribution Standard — Validation Report v1
**Benchmark v1.0 · Engine v0.2 · Standard v0.3 · Methodology: Aswin Krishna**

This report publishes the error characteristics of the Libra Module A measurable layer against a ground-truth benchmark, per Standard §7. It answers the *Daubert* error-rate requirement (Red-Team Objection 6) with numbers rather than assurances.

---

## 1. What is validated — and what is not

Libra separates two layers. The **measurable layer** — redundancy detection, consolidation behaviour, overlap calibration — makes empirical claims and is validated here. The **normative layer** — weights, base floor — is disclosed policy under Standard §5 and makes no empirical claim to validate. Conflating the two is how methodologies get destroyed on cross-examination; Libra's validation is scoped to what it actually asserts.

## 2. Benchmark design

**Corpus:** 18 real public-domain texts (the classic NLTK Project Gutenberg selection: Austen, Melville, Shakespeare, Chesterton, Milton, Whitman, et al.), assembled into **32 rightsholder claims** with five engineered case families:

- **F1 Editions (consolidation):** *Emma* plus a ~95%-identical second edition under the **same rightsholder** — tests that consolidation protects a claimant from being discounted as her own duplicator.
- **F2 Calibration (9 cases):** copier texts engineered to copy exactly f ∈ {0.1 … 0.9} of a disjoint donor slice (Melville), padded with held-out filler — tests whether measured overlap (1 − uniqueness) recovers the engineered fraction.
- **F3 Anthology:** a work assembled from chunks of four donor claims plus one-third own content — tests compound-source recovery.
- **F4 Controls (8 claims):** genuinely independent texts — measures the false-positive baseline.
- **F5 Reproducibility:** the entire benchmark rebuilt and re-evaluated independently; results compared bit-for-bit.

Construction is seeded and fully deterministic; the manifest (texts, lengths, case parameters) is embedded in `benchmark_results.json`.

## 3. Published error characteristics

**M1 — Calibration: MAE 0.0005 (max error 0.0014) across nine engineered fractions.**

| Engineered f | Measured overlap | Abs. error |
|---|---|---|
| 0.1 | 0.0994 | 0.0006 |
| 0.2 | 0.1996 | 0.0004 |
| 0.3 | 0.2995 | 0.0005 |
| 0.4 | 0.3996 | 0.0004 |
| 0.5 | 0.4997 | 0.0003 |
| 0.6 | 0.5997 | 0.0003 |
| 0.7 | 0.7014 | 0.0014 |
| 0.8 | 0.7999 | 0.0001 |
| 0.9 | 0.8999 | 0.0001 |

Donor-side measurements mirror copier-side values, empirically confirming the documented symmetric-discount behaviour (v2 provenance-priority factor remains scheduled).

**M2 — False-positive baseline: maximum false overlap 0.0001** across eight independent real texts (mean uniqueness 1.0000, minimum 0.9999). Eight-word shingles on natural prose essentially never collide across genuinely independent works in this corpus.

**M3 — Consolidation: PASS.** The two-edition claim shows uniqueness 1.0000 — indistinguishable from fully original controls. The claimant with duplicate editions is not penalised; Red-Team Objection 2's fix is empirically confirmed.

**M4 — Anthology: engineered own-fraction 0.3333, measured 0.3380** (error 0.0047, attributable to novel shingles formed at chunk boundaries).

**M5 — Reproducibility: PASS.** Independent rebuild and re-evaluation produced bit-identical results (SHA-256 verified).

## 4. Honest limits of this validation

1. **Contiguous copying only.** Calibration cases copy contiguous blocks. Dispersed or paraphrased copying will degrade recovery — that is precisely the boundary between Tier A (deterministic overlap) and Tier B (Module B's paraphrase/semantic signals, v2). The near-zero error here characterises Tier A on its own terms, not all copying.
2. **Genre dependence of the false-positive baseline.** Formulaic genres (legal boilerplate, liturgical text) repeat long word sequences and will raise the baseline; the highly repetitive KJV was deliberately excluded from controls. Genre-stratified baselines are scheduled for Benchmark v2.
3. **Scale.** 32 claims validates correctness of behaviour, not performance at settlement scale (10⁵–10⁶ claims). Scale testing is an engineering exercise, scheduled.
4. **Measurable layer only**, per §1.

## 5. Effect on validation status

Engine disclosure updated from "pre-validation prototype" to: **validated against Benchmark v1 on the measurable layer (calibration MAE 0.0005; false-positive baseline ≤ 0.0001; consolidation and reproducibility PASS); independent replication and scale testing pending.** Every generated report now carries this status with a pointer to this document.

## 6. Reproducibility note (supersedes the earlier asset note)

Benchmark v1 is published in full: the construction and evaluation script (`benchmark.py`), the complete results and manifest (`benchmark_results.json`), and the corpus recipe (README, "Reproduce the benchmark") are all in the public repository under Apache-2.0. The validation is therefore reproducible end-to-end by any stranger — ground-truth construction included; runs are seeded and deterministic, and the results file carries a full SHA-256 digest for comparison. Authorship and priority rest on the published, timestamped record itself.
