"""Regression guards for the scale-and-noise benchmark."""
import run_benchmark as rb
from libra_engine import CorpusApportionmentEngine


def _clean_auc(seed=20260708, n=60):
    works, is_shared = rb.build_corpus(n, 0.4, seed, None)
    eng = CorpusApportionmentEngine()
    uniq, _ = rb.score_condition(works, "none", 0.0, seed, eng)
    ids = [w for w, _ in works]
    pos = [1 - uniq[i] for i, s in zip(ids, is_shared, strict=False) if s]
    neg = [1 - uniq[i] for i, s in zip(ids, is_shared, strict=False) if not s]
    return rb._auc(pos, neg)


def test_clean_baseline_perfect_detection():
    # on clean text the engine must separate shared works from originals perfectly
    assert _clean_auc() == 1.0


def test_reproducible():
    assert _clean_auc(seed=123) == _clean_auc(seed=123)


def test_auc_helper_bounds():
    assert rb._auc([1, 1, 1], [0, 0, 0]) == 1.0
    assert rb._auc([0, 0], [1, 1]) == 0.0
    assert rb._auc([1, 0], [1, 0]) == 0.5
