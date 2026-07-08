# Libra Attribution Engine — Allocation Report
**Standard v0.3 · Engine v0.2 (Module A) · Methodology: Aswin Krishna**

> **Validation status (Standard §5, mandatory):** VALIDATED against Libra Benchmark v1 (measurable layer): calibration MAE 0.0005 across engineered copy-fractions 0.1–0.9; false-positive baseline ≤ 0.0001 on independent real texts; consolidation and reproducibility PASS. Independent replication and scale testing pending. See Libra Validation Report v1.

> **Synthetic-metadata disclosure (audit M3):** market metadata in this demonstration corpus is an illustrative placeholder. Tier A status for A4 requires sourcing from verifiable bibliographic metadata in production.

**Claims:** 27 (after rightsholder consolidation) · **Pool:** $1,500,000 · **Flat baseline:** $55,556/claim · **Shingle k:** 8

## 1. Mandatory methodology disclosure
| Parameter | Value | Written rationale |
|---|---|---|
| w_volume | 0.7 | Deduplicated volume measures EXPOSURE — how much of the claim's content the training process consumed — the conduct being compensated. Weighted highest because fully reproducible by opposing experts (Tier A). |
| w_market | 0.3 | Mirrors market-harm logic in statutory-damages jurisprudence: commercially live works face greater substitution exposure. Scored mechanically from verifiable metadata via the published mapping table (Tier A). |
| base_floor | 0.15 | Per-se inclusion value: copyright and statutory damages attach per work; no included claim may be diluted to zero by volume metrics. A TRIBUNAL-SET policy parameter with this disclosed default. |

**A4 published mapping table (discretion lives here, contestable in advance):**

| Metadata condition | Score |
|---|---|
| In print AND retail-available | 1.0 |
| In print, not retail-available | 0.8 |
| Out of print, retail-available (live backlist) | 0.6 |
| Out of print, unavailable, published within 20 years | 0.35 |
| Out of print, unavailable, older than 20 years | 0.2 |

**Consolidation statement (Standard §4 A2):** works were consolidated to rightsholder-claim level
before any redundancy computation; within-claim duplication (editions) collapses by construction
and is never discounted against the claimant.

## 2. Engineered cases (ground-truth behaviour)
| Rightsholder | Works | Tokens | Distinct vol | Uniqueness | Market | Share | Libra USD | Flat USD | Δ |
|---|---|---|---|---|---|---|---|---|---|
| RH-005 | 2 | 14,268 | 11,165 | 1.00 | 1.00 | 5.40% | $80,970 | $55,556 | +25,414 |
| RH-ANTH | 1 | 8,855 | 8,848 | 0.28 | 0.80 | 2.42% | $36,355 | $55,556 | -19,201 |
| RH-DERIV | 1 | 2,540 | 2,533 | 0.40 | 0.35 | 1.35% | $20,185 | $55,556 | -35,371 |


## 3. Full allocation schedule (top of schedule)
| Rightsholder | Works | Tokens | Distinct vol | Uniqueness | Market | Share | Libra USD | Flat USD | Δ |
|---|---|---|---|---|---|---|---|---|---|
| RH-013 | 1 | 13,915 | 13,908 | 1.00 | 1.00 | 6.26% | $93,843 | $55,556 | +38,287 |
| RH-011 | 1 | 13,423 | 13,416 | 1.00 | 1.00 | 6.10% | $91,534 | $55,556 | +35,978 |
| RH-020 | 1 | 14,825 | 14,818 | 1.00 | 0.60 | 6.00% | $90,018 | $55,556 | +34,463 |
| RH-005 | 2 | 14,268 | 11,165 | 1.00 | 1.00 | 5.40% | $80,970 | $55,556 | +25,414 |
| RH-016 | 1 | 11,690 | 11,683 | 1.00 | 0.80 | 5.29% | $79,353 | $55,556 | +23,797 |
| RH-023 | 1 | 13,610 | 13,603 | 1.00 | 0.35 | 5.28% | $79,257 | $55,556 | +23,701 |
| RH-003 | 1 | 11,856 | 11,849 | 1.00 | 0.60 | 5.07% | $76,084 | $55,556 | +20,529 |
| RH-017 | 1 | 9,382 | 9,375 | 1.00 | 1.00 | 4.84% | $72,569 | $55,556 | +17,013 |
| RH-018 | 1 | 10,000 | 9,993 | 1.00 | 0.80 | 4.76% | $71,422 | $55,556 | +15,866 |
| RH-004 | 1 | 9,459 | 9,452 | 1.00 | 0.60 | 4.32% | $64,835 | $55,556 | +9,280 |
| RH-014 | 1 | 7,699 | 7,692 | 1.00 | 1.00 | 4.31% | $64,671 | $55,556 | +9,115 |
| RH-021 | 1 | 8,808 | 8,801 | 1.00 | 0.60 | 4.12% | $61,780 | $55,556 | +6,224 |


## 4. Sensitivity analysis — weights AND technical parameters (Standard §5)
| Parameter varied | Value | Spearman vs default | Max share swing (pct-pts) |
|---|---|---|---|
| w_volume | 0.56 | 0.9805 | 0.6308 |
| w_volume | 0.84 | 0.9866 | 0.6308 |
| shingle_k | 6 | 0.9982 | 0.2098 |
| shingle_k | 10 | 1.0 | 0.1735 |
| base_floor | 0.1 | 1.0 | 0.1501 |
| base_floor | 0.2 | 1.0 | 0.1501 |

**Minimum rank stability (Spearman): 0.9805** · max share swing 0.63 pct-pts. Disclosed, not hidden.

## 5. Statement of limits (Standard §2)
This allocation operates on a **known corpus**. It asserts relative contribution within that corpus;
it does not assert what any black-box model was trained on. Similarity evidences presence and weight,
never causation. All factors herein are Tier A (deterministic) subject to the synthetic-metadata disclosure above.
