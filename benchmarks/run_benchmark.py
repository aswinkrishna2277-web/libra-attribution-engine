"""
Copyright 2026 Aswin Krishna. Licensed under the Apache License, Version 2.0 (see LICENSE).
Libra Scale-and-Noise Benchmark.

Measures whether the engine's uniqueness measure still separates copied works from
originals as realistic corpus noise increases (OCR corruption, non-contiguous copying,
edition variants, paraphrase), and how far allocation shares drift under that noise.

Corpus is generated deterministically from a seed, or supplied as a folder of .txt files
(one work per file) via --texts DIR. All parameters are disclosed and reproducible.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))          # local: corpus.py
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # repo root: libra_engine.py

from corpus import NOISE_FUNCS, _vocab, make_work_text  # noqa: E402
from libra_engine import CorpusApportionmentEngine, Work  # noqa: E402


def _auc(scores_pos: list[float], scores_neg: list[float]) -> float:
    """AUC via the Mann-Whitney U statistic (no sklearn dependency).
    Probability a random copy scores higher-'copyness' than a random original."""
    if not scores_pos or not scores_neg:
        return float("nan")
    wins = ties = 0
    for p in scores_pos:
        for n in scores_neg:
            if p > n:
                wins += 1
            elif p == n:
                ties += 1
    return (wins + 0.5 * ties) / (len(scores_pos) * len(scores_neg))


def _load_texts(folder: Path) -> list[str]:
    files = sorted(folder.glob("*.txt"))
    if not files:
        raise SystemExit(f"no .txt files found in {folder}")
    return [f.read_text(encoding="utf-8", errors="ignore") for f in files]


def build_corpus(n_originals: int, copy_frac_of_corpus: float, seed: int,
                 base_texts: list[str] | None):
    """Return (works_meta, is_shared).

    Negatives: distinctive standalone originals.
    Positives: members of shared-text GROUPS (>=2 works sharing a distinctive core).
    The uniqueness measure is corpus-relative and symmetric, so every member of a
    sharing group is a true positive -- that is exactly what the method detects.
    Copies are built clean here; noise is applied per-condition later.
    """
    rng = random.Random(seed)
    if base_texts:
        pool = list(base_texts)
    else:
        vocab = _vocab(rng)
        pool = [make_work_text(rng, vocab, rng.randint(300, 900))
                for _ in range(n_originals + 2 * max(1, int(n_originals * copy_frac_of_corpus)))]

    works, is_shared = [], []
    idx = 0

    # negatives: standalone originals
    for _ in range(n_originals):
        works.append((f"O{idx:04d}", pool[idx]))
        is_shared.append(False)
        idx += 1

    # positives: shared-text groups of two, sharing a distinctive core passage
    n_groups = max(1, int(n_originals * copy_frac_of_corpus))
    vfill = _vocab(random.Random(seed + 7))
    for g in range(n_groups):
        core = pool[idx]
        idx += 1
        cf = rng.uniform(0.3, 0.7)
        core_toks = core.split()
        take = max(1, int(len(core_toks) * cf))
        start = rng.randint(0, max(0, len(core_toks) - take))
        shared_core = core_toks[start:start + take]
        for m in range(2):  # two members per group
            filler = make_work_text(rng, vfill, rng.randint(150, 400)).split() \
                if not base_texts else pool[(idx + m) % len(pool)].split()[:400]
            contiguous = (m == 0)  # one member contiguous, one scattered
            if contiguous:
                body = filler[:len(filler)//2] + shared_core + filler[len(filler)//2:]
            else:
                body = filler[:]
                chunk = max(1, len(shared_core)//4)
                for c0 in range(0, len(shared_core), chunk):
                    ins = rng.randint(0, len(body))
                    body[ins:ins] = shared_core[c0:c0+chunk]
            works.append((f"S{g:04d}_{m}", " ".join(body)))
            is_shared.append(True)
    return works, is_shared


def score_condition(works_meta, noise_name: str, rate: float, seed: int,
                    engine: CorpusApportionmentEngine):
    """Apply one noise type at one rate to every work, run the engine, return per-work uniqueness + shares."""
    tag = f"{noise_name}:{round(rate, 6)}".encode()
    derived = seed ^ int.from_bytes(hashlib.blake2b(tag, digest_size=4).digest(), "big")
    rng = random.Random(derived)
    works = []
    for wid, text in works_meta:
        t = text
        if rate > 0 and noise_name in NOISE_FUNCS:
            t = NOISE_FUNCS[noise_name](t, rate, rng)
        # each work is its own rightsholder so claim==work: isolates per-work uniqueness
        works.append(Work(wid, wid, "a", wid, t, True, True, 2000, "", 0))
    claims = engine.analyze(works)
    uniq = {c.rightsholder_id: c.uniqueness for c in claims}
    share = {c.rightsholder_id: c.share for c in claims}
    return uniq, share


def main(argv=None):
    ap = argparse.ArgumentParser(description="Libra scale-and-noise benchmark")
    ap.add_argument("--n", type=int, default=200, help="number of original works (default 200)")
    ap.add_argument("--copy-frac", type=float, default=0.4, help="copies as fraction of originals")
    ap.add_argument("--seed", type=int, default=20260708)
    ap.add_argument("--texts", type=str, default=None, help="folder of .txt files (one work each); overrides --n")
    ap.add_argument("--levels", type=float, nargs="+", default=[0.0, 0.01, 0.02, 0.05, 0.10, 0.20],
                    help="noise rates to sweep")
    ap.add_argument("--out", type=str, default="benchmark_scale_results.json")
    ap.add_argument("--quick", action="store_true", help="tiny fast run for CI (n=40)")
    ap.add_argument("--fuzzy", action="store_true",
                    help="use OCR-tolerant character-shingle matching")
    args = ap.parse_args(argv)

    if args.quick:
        args.n, args.levels = 40, [0.0, 0.05, 0.20]

    base_texts = _load_texts(Path(args.texts)) if args.texts else None
    n_desc = f"{len(base_texts)} real texts" if base_texts else f"{args.n} synthetic works"
    works_meta, is_shared = build_corpus(args.n, args.copy_frac, args.seed, base_texts)
    from libra_engine import WeightConfig
    _cfg = WeightConfig()
    _cfg.fuzzy = args.fuzzy
    engine = CorpusApportionmentEngine(config=_cfg)

    # clean baseline shares (for drift measurement)
    base_uniq, base_share = score_condition(works_meta, "none", 0.0, args.seed, engine)
    ids = [wid for wid, _ in works_meta]
    shared_ids = [wid for wid, c in zip(ids, is_shared, strict=False) if c]
    orig_ids = [wid for wid, c in zip(ids, is_shared, strict=False) if not c]

    t0 = time.time()
    results = {"config": {"corpus": n_desc, "n_originals": args.n if not base_texts else len(base_texts),
                          "n_shared_works": len(shared_ids), "copy_frac": args.copy_frac, "seed": args.seed,
                          "levels": args.levels, "shingle_k": engine.shingle_k,
                          "w_volume": engine.config.w_volume, "base_floor": engine.config.base_floor,
                          "fuzzy": args.fuzzy},
               "conditions": []}

    for noise in ["ocr", "edition", "paraphrase"]:
        for rate in args.levels:
            uniq, share = score_condition(works_meta, noise, rate, args.seed, engine)
            copyness_shared = [1.0 - uniq[i] for i in shared_ids]  # shared works should score high
            copyness_orig = [1.0 - uniq[i] for i in orig_ids]
            auc = _auc(copyness_shared, copyness_orig)
            mean_uniq_shared = sum(uniq[i] for i in shared_ids) / len(shared_ids)
            mean_uniq_orig = sum(uniq[i] for i in orig_ids) / len(orig_ids)
            drift = sum(abs(share[i] - base_share[i]) for i in ids)  # L1 share drift vs clean
            results["conditions"].append({
                "noise": noise, "rate": rate, "auc": round(auc, 4),
                "mean_uniqueness_shared": round(mean_uniq_shared, 4),
                "mean_uniqueness_originals": round(mean_uniq_orig, 4),
                "separation_gap": round(mean_uniq_orig - mean_uniq_shared, 4),
                "share_L1_drift_vs_clean": round(drift, 6),
            })
    results["elapsed_sec"] = round(time.time() - t0, 2)

    Path(args.out).write_text(json.dumps(results, indent=2), encoding="utf-8")
    _print_table(results)
    return 0


def _print_table(results):
    c = results["config"]
    print(f"\nLibra Scale-and-Noise Benchmark  ({c['corpus']}; "
          f"{c['n_shared_works']} shared works; k={c['shingle_k']}; seed={c['seed']})")
    print(f"{'noise':<12}{'rate':>6}{'AUC':>8}{'uniq(orig)':>12}{'uniq(shared)':>13}{'gap':>8}{'drift':>10}")
    print("-" * 68)
    for r in results["conditions"]:
        print(f"{r['noise']:<12}{r['rate']:>6}{r['auc']:>8}{r['mean_uniqueness_originals']:>12}"
              f"{r['mean_uniqueness_shared']:>12}{r['separation_gap']:>8}{r['share_L1_drift_vs_clean']:>10}")
    print("\nAUC = P(a copy looks more-copied than an original); 1.00 = perfect detection, 0.50 = chance.")
    print(f"elapsed: {results['elapsed_sec']}s")


if __name__ == "__main__":
    raise SystemExit(main())
