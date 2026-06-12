"""
Libra Benchmark v1 — construction + evaluation harness
Validates the MEASURABLE layer of the Libra Attribution Standard (v0.3, §7)
against real public-domain texts with engineered ground truth.

Validated claims (empirical):
  M1 Calibration  — engineered copied-fraction f vs measured overlap (1 - uniqueness)
  M2 False-positive baseline — uniqueness of genuinely independent texts (expect ~1.0)
  M3 Consolidation correctness — same-rightsholder editions are not punished
  M4 Anthology recovery — measured own-fraction vs engineered
  M5 Reproducibility — byte-identical metrics across independent runs

NOT validated here (normative, disclosed policy per Standard §5): weights, floor.
"""

from __future__ import annotations
import json
import random
from pathlib import Path

from libra_engine import Work, CorpusApportionmentEngine

GUT = Path("gutenberg")
CAP_CONTROL = 40_000   # words per control/edition text
SLICE = 10_000         # words per calibration donor/copier
FRACS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

CONTROLS = ["chesterton-ball", "chesterton-brown", "chesterton-thursday",
            "austen-persuasion", "austen-sense",
            "shakespeare-caesar", "shakespeare-hamlet", "shakespeare-macbeth"]
ANTH_DONORS = ["burgess-busterbrown", "carroll-alice", "blake-poems", "bryant-stories"]
EDITION_BASE = "austen-emma"
CALIB_DONOR = "melville-moby_dick"
FILLER_POOL = ["milton-paradise", "whitman-leaves", "edgeworth-parents"]


def words(name: str) -> list[str]:
    return (GUT / f"{name}.txt").read_text(encoding="utf-8", errors="ignore").split()


def build_benchmark(seed: int = 7):
    rng = random.Random(seed)
    works, manifest = [], {"cases": [], "texts": {}}

    # filler pool: disjoint consumption
    filler = words(FILLER_POOL[0]) + words(FILLER_POOL[1]) + words(FILLER_POOL[2])
    f_idx = 0
    def take_filler(n):
        nonlocal f_idx
        out = filler[f_idx:f_idx + n]
        f_idx += n
        assert len(out) == n, "filler pool exhausted"
        return out

    # F4 — pure controls (independent real texts)
    for name in CONTROLS:
        t = words(name)[:CAP_CONTROL]
        works.append(Work(name, name, name.split("-")[0].title(), f"RH-{name}",
                          " ".join(t)))
        manifest["texts"][name] = len(t)
        manifest["cases"].append({"family": "F4-control", "claim": f"RH-{name}",
                                  "expected": "uniqueness ~ 1.0"})

    # F1 — same-rightsholder editions (consolidation test)
    base = words(EDITION_BASE)[:CAP_CONTROL]
    noise_vocab = take_filler(2000)
    edition = [w if rng.random() > 0.05 else rng.choice(noise_vocab) for w in base]
    works.append(Work("emma-1ed", "Emma (1st ed.)", "Austen", "RH-AUSTEN-EMMA", " ".join(base)))
    works.append(Work("emma-2ed", "Emma (2nd ed.)", "Austen", "RH-AUSTEN-EMMA", " ".join(edition),
                      notes="engineered: ~95% same text, SAME rightsholder"))
    manifest["cases"].append({"family": "F1-editions", "claim": "RH-AUSTEN-EMMA",
                              "expected": "consolidated; uniqueness comparable to controls"})

    # F2 — calibration pairs: copier copies fraction f of its own disjoint donor slice
    moby = words(CALIB_DONOR)
    for i, f in enumerate(FRACS):
        donor = moby[i * SLICE:(i + 1) * SLICE]
        n_copy = int(f * SLICE)
        copier = donor[:n_copy] + take_filler(SLICE - n_copy)
        works.append(Work(f"don-{f}", f"Donor f={f}", "Melville", f"RH-DON-{int(f*100):02d}",
                          " ".join(donor)))
        works.append(Work(f"cop-{f}", f"Copier f={f}", "CopierCo", f"RH-COP-{int(f*100):02d}",
                          " ".join(copier), notes=f"engineered: fraction {f} copied from donor"))
        manifest["cases"].append({"family": "F2-calibration", "claim": f"RH-COP-{int(f*100):02d}",
                                  "engineered_f": f, "expected": f"measured overlap ~ {f}"})

    # F3 — anthology: 3k-word chunks from four donors + 6k own filler (own fraction = 1/3)
    chunks, total = [], 0
    for name in ANTH_DONORS:
        t = words(name)[:20_000]
        works.append(Work(name, name, name.split("-")[0].title(), f"RH-{name}", " ".join(t)))
        manifest["texts"][name] = len(t)
        chunk = t[:3000]
        chunks += chunk
        total += len(chunk)
    own = take_filler(total // 2)            # 6000 own words -> own fraction = 6000/18000
    anth_text = chunks + own
    engineered_own = len(own) / len(anth_text)
    works.append(Work("anthology", "The Anthology", "AnthCo", "RH-ANTH",
                      " ".join(anth_text), notes="engineered anthology"))
    manifest["cases"].append({"family": "F3-anthology", "claim": "RH-ANTH",
                              "engineered_own_fraction": round(engineered_own, 4),
                              "expected": f"uniqueness ~ {engineered_own:.3f}"})
    return works, manifest, engineered_own


def evaluate(seed: int = 7) -> dict:
    works, manifest, engineered_own = build_benchmark(seed)
    engine = CorpusApportionmentEngine()
    claims = {c.rightsholder_id: c for c in engine.analyze(works)}

    # M1 calibration
    calib = []
    for f in FRACS:
        measured = 1 - claims[f"RH-COP-{int(f*100):02d}"].uniqueness
        donor_m = 1 - claims[f"RH-DON-{int(f*100):02d}"].uniqueness
        calib.append({"engineered_f": f, "measured_overlap": round(measured, 4),
                      "abs_error": round(abs(measured - f), 4),
                      "donor_measured_overlap_symmetric": round(donor_m, 4)})
    mae = sum(c["abs_error"] for c in calib) / len(calib)
    maxe = max(c["abs_error"] for c in calib)

    # M2 false-positive baseline
    ctrl_u = [claims[f"RH-{n}"].uniqueness for n in CONTROLS]
    fp = {"mean_uniqueness": round(sum(ctrl_u) / len(ctrl_u), 4),
          "min_uniqueness": round(min(ctrl_u), 4),
          "max_false_overlap": round(1 - min(ctrl_u), 4)}

    # M3 consolidation
    emma_u = claims["RH-AUSTEN-EMMA"].uniqueness
    consolidation = {"editions_claim_uniqueness": round(emma_u, 4),
                     "controls_mean_uniqueness": fp["mean_uniqueness"],
                     "pass": bool(emma_u >= fp["mean_uniqueness"] - 0.05)}

    # M4 anthology
    anth_u = claims["RH-ANTH"].uniqueness
    anthology = {"engineered_own_fraction": round(engineered_own, 4),
                 "measured_uniqueness": round(anth_u, 4),
                 "abs_error": round(abs(anth_u - engineered_own), 4)}

    return {"benchmark_version": "1.0", "seed": seed,
            "corpus": "18 public-domain texts (NLTK Gutenberg selection), engineered cases",
            "n_works": len(works), "n_claims": len(claims),
            "M1_calibration": {"per_case": calib, "MAE": round(mae, 4), "max_error": round(maxe, 4)},
            "M2_false_positive_baseline": fp,
            "M3_consolidation": consolidation,
            "M4_anthology": anthology,
            "manifest": manifest}


if __name__ == "__main__":
    import hashlib
    r1 = evaluate()
    r2 = evaluate()  # M5 reproducibility: independent rebuild + rerun
    s1 = json.dumps({k: v for k, v in r1.items() if k != "manifest"}, sort_keys=True)
    s2 = json.dumps({k: v for k, v in r2.items() if k != "manifest"}, sort_keys=True)
    r1["M5_reproducibility"] = {"identical": s1 == s2,
                                "sha256": hashlib.sha256(s1.encode()).hexdigest()}
    Path("benchmark_results.json").write_text(json.dumps(r1, indent=2), encoding="utf-8")
    print(f"claims: {r1['n_claims']} | M1 MAE: {r1['M1_calibration']['MAE']} "
          f"(max {r1['M1_calibration']['max_error']})")
    print(f"M2 false-overlap baseline: {r1['M2_false_positive_baseline']['max_false_overlap']} "
          f"(mean uniqueness {r1['M2_false_positive_baseline']['mean_uniqueness']})")
    print(f"M3 consolidation pass: {r1['M3_consolidation']['pass']} "
          f"(editions uniq {r1['M3_consolidation']['editions_claim_uniqueness']})")
    print(f"M4 anthology: engineered {r1['M4_anthology']['engineered_own_fraction']} "
          f"vs measured {r1['M4_anthology']['measured_uniqueness']}")
    print(f"M5 reproducible: {r1['M5_reproducibility']['identical']}")
    for c in r1["M1_calibration"]["per_case"]:
        print(f"   f={c['engineered_f']}: measured {c['measured_overlap']} (err {c['abs_error']})")
