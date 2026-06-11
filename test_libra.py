"""
Libra Attribution Engine — Test Suite v1
Run: pytest test_libra.py -v
Covers: unit correctness, hand-verifiable math, formula invariants,
edge cases, end-to-end behaviour, CSV-parsing hardening, benchmark thresholds.
"""

import io
import ast
import random
import pandas as pd
import pytest

from libra_engine import (
    Work, Claim, WeightConfig, CorpusApportionmentEngine,
    market_score, _shingles, build_demo_corpus, report_markdown,
    rows_to_csv, full_json, SPEC_VERSION,
)


# ---------------------------- 1. UNIT: A4 mapping table -------------------------

class TestMarketMapping:
    def test_in_print_and_retail(self):
        assert market_score(True, True, 1990) == 1.00

    def test_in_print_only(self):
        assert market_score(True, False, 1990) == 0.80

    def test_retail_only_backlist(self):
        assert market_score(False, True, 1950) == 0.60

    def test_unavailable_recent(self):
        assert market_score(False, False, 2015) == 0.35

    def test_unavailable_old(self):
        assert market_score(False, False, 1980) == 0.20

    def test_mapping_is_mechanical(self):
        """Same metadata -> same score, always (Standard §4 A4)."""
        for _ in range(50):
            assert market_score(True, False, 2000) == 0.80


# ---------------------------- 2. UNIT: shingling --------------------------------

class TestShingles:
    def test_deterministic_across_calls(self):
        assert _shingles("the quick brown fox jumps over the lazy dog", 4) == \
               _shingles("the quick brown fox jumps over the lazy dog", 4)

    def test_count_formula(self):
        # n tokens, window k -> n-k+1 distinct shingles (all-distinct text)
        text = " ".join(f"w{i}" for i in range(20))
        assert len(_shingles(text, 8)) == 20 - 8 + 1

    def test_short_text_single_shingle(self):
        assert len(_shingles("hello world", 8)) == 1

    def test_empty_text(self):
        assert _shingles("", 8) == set()

    def test_case_insensitive(self):
        assert _shingles("A B C D", 2) == _shingles("a b c d", 2)


# ------------------- 3. HAND-VERIFIABLE MATH (pen-and-paper case) ----------------

class TestHandVerifiable:
    """Two tiny works, k=2. Verify with pen and paper:
       Claim A: 'a b c d'  -> shingles {ab, bc, cd}
       Claim B: 'c d e f'  -> shingles {cd, de, ef}
       Shared: {cd}. So uniqueness A = 2/3, B = 2/3.
       Effective volume = 3 x 2/3 = 2 each. Equal market (same metadata).
       => identical scores => with floor 0.15: share = 0.075 + 0.85 x 0.5 = 0.5 each."""

    def setup_method(self):
        self.works = [
            Work("A", "A", "a", "RH-A", "a b c d", in_print=True, retail_available=True, pub_year=2020),
            Work("B", "B", "b", "RH-B", "c d e f", in_print=True, retail_available=True, pub_year=2020),
        ]
        self.engine = CorpusApportionmentEngine()

    def test_uniqueness_two_thirds(self):
        claims = {c.rightsholder_id: c for c in self.engine.analyze(self.works, k=2)}
        assert claims["RH-A"].uniqueness == pytest.approx(2 / 3)
        assert claims["RH-B"].uniqueness == pytest.approx(2 / 3)

    def test_effective_volume(self):
        claims = {c.rightsholder_id: c for c in self.engine.analyze(self.works, k=2)}
        assert claims["RH-A"].effective_volume == pytest.approx(2.0)

    def test_symmetric_shares_half_each(self):
        claims = self.engine.analyze(self.works, k=2)
        for c in claims:
            assert c.share == pytest.approx(0.5)


# ---------------------------- 4. FORMULA INVARIANTS ------------------------------

class TestInvariants:
    def _random_works(self, rng, n):
        vocab = [f"t{i}" for i in range(300)]
        return [Work(f"W{i}", f"W{i}", "x", f"RH-{i}",
                     " ".join(rng.choice(vocab) for _ in range(rng.randint(50, 800))),
                     in_print=rng.random() > 0.5, retail_available=rng.random() > 0.5,
                     pub_year=rng.randint(1950, 2025)) for i in range(n)]

    def test_shares_sum_to_one_across_random_configs(self):
        rng = random.Random(3)
        for trial in range(10):
            works = self._random_works(rng, rng.randint(2, 15))
            wv = round(rng.uniform(0.1, 0.9), 2)
            fl = round(rng.uniform(0.0, 0.4), 2)
            cfg = WeightConfig(w_volume=wv, w_market=round(1 - wv, 2), base_floor=fl)
            claims = CorpusApportionmentEngine(cfg).analyze(works)
            assert sum(c.share for c in claims) == pytest.approx(1.0)

    def test_floor_guarantee(self):
        """Every claim gets at least floor/n — the per-se inclusion value."""
        rng = random.Random(4)
        works = self._random_works(rng, 8)
        works.append(Work("Z", "Z", "z", "RH-EMPTY", ""))  # worst case: empty text
        cfg = WeightConfig(base_floor=0.2)
        claims = CorpusApportionmentEngine(cfg).analyze(works)
        n = len(claims)
        for c in claims:
            assert c.share >= 0.2 / n - 1e-12

    def test_volume_monotonicity(self):
        """More unique volume, same market -> strictly larger share."""
        big = " ".join(f"b{i}" for i in range(500))
        small = " ".join(f"s{i}" for i in range(100))
        works = [Work("B", "B", "x", "RH-BIG", big, in_print=True, retail_available=True, pub_year=2020),
                 Work("S", "S", "x", "RH-SML", small, in_print=True, retail_available=True, pub_year=2020)]
        claims = {c.rightsholder_id: c for c in CorpusApportionmentEngine().analyze(works)}
        assert claims["RH-BIG"].share > claims["RH-SML"].share

    def test_allocation_arithmetic(self):
        works = self._random_works(random.Random(5), 6)
        eng = CorpusApportionmentEngine()
        rows = eng.allocate(eng.analyze(works), 600_000)
        for r in rows:
            assert r["delta_usd"] == pytest.approx(r["libra_usd"] - r["flat_usd"], abs=0.011)
        assert sum(r["libra_usd"] for r in rows) == pytest.approx(600_000, abs=1.0)


# ---------------------------- 5. CONSOLIDATION -----------------------------------

class TestConsolidation:
    def test_same_rightsholder_editions_not_punished(self):
        base = " ".join(f"u{i}" for i in range(400))
        works = [
            Work("E1", "Ed1", "a", "RH-SAME", base),
            Work("E2", "Ed2", "a", "RH-SAME", base),               # identical edition
            Work("C", "Ctrl", "b", "RH-CTRL", " ".join(f"v{i}" for i in range(400))),
        ]
        claims = {c.rightsholder_id: c for c in CorpusApportionmentEngine().analyze(works)}
        assert len(claims) == 2                                    # consolidation happened
        assert claims["RH-SAME"].uniqueness == pytest.approx(1.0)  # not self-discounted
        assert claims["RH-SAME"].distinct_volume == claims["RH-CTRL"].distinct_volume

    def test_cross_rightsholder_copy_discounted(self):
        donor = " ".join(f"d{i}" for i in range(400))
        works = [Work("D", "Donor", "a", "RH-D", donor),
                 Work("P", "Copy", "b", "RH-P", donor)]            # 100% cross-claimant copy
        claims = {c.rightsholder_id: c for c in CorpusApportionmentEngine().analyze(works)}
        assert claims["RH-P"].uniqueness == pytest.approx(0.0)
        assert claims["RH-D"].uniqueness == pytest.approx(0.0)     # symmetric (documented v1 behaviour)


# ---------------------------- 6. EDGE CASES --------------------------------------

class TestEdges:
    def test_single_claim_full_share(self):
        eng = CorpusApportionmentEngine()
        claims = eng.analyze([Work("W", "W", "a", "RH", "x " * 100)])
        assert claims[0].share == pytest.approx(1.0)

    def test_empty_corpus_raises_friendly(self):
        with pytest.raises(ValueError, match="empty"):
            CorpusApportionmentEngine().allocate([], 1000.0)

    def test_weights_must_sum_to_one(self):
        with pytest.raises(AssertionError):
            WeightConfig(w_volume=0.7, w_market=0.7).validate()

    def test_sensitivity_structure(self):
        eng = CorpusApportionmentEngine()
        s = eng.sensitivity(build_demo_corpus())
        assert len(s["scenarios"]) == 6                # 2 weights + 2 k + 2 floor
        assert {sc["parameter"] for sc in s["scenarios"]} == {"w_volume", "shingle_k", "base_floor"}
        assert 0 <= s["min_spearman"] <= 1


# ---------------------------- 7. END-TO-END --------------------------------------

class TestEndToEnd:
    def test_demo_corpus_engineered_behaviour(self):
        eng = CorpusApportionmentEngine()
        claims = {c.rightsholder_id: c for c in eng.analyze(build_demo_corpus())}
        assert claims["RH-005"].uniqueness == pytest.approx(1.0)   # editions consolidated
        assert claims["RH-DERIV"].uniqueness < 0.6                 # 60% copier discounted
        assert claims["RH-ANTH"].uniqueness < 0.5                  # anthology discounted

    def test_report_contains_mandatory_disclosures(self):
        eng = CorpusApportionmentEngine()
        works = build_demo_corpus()
        rows = eng.allocate(eng.analyze(works), 1_000_000)
        md = report_markdown(rows, eng.sensitivity(works), eng.config, 1_000_000, 8, True)
        for required in ["Validation status", "Synthetic-metadata disclosure",
                         "mapping table", "Consolidation statement",
                         "Sensitivity analysis", "Statement of limits", SPEC_VERSION]:
            assert required in md

    def test_csv_and_json_exports_parse(self):
        eng = CorpusApportionmentEngine()
        works = build_demo_corpus()
        rows = eng.allocate(eng.analyze(works), 1_000_000)
        df = pd.read_csv(io.StringIO(rows_to_csv(rows)))
        assert len(df) == len(rows)
        import json
        j = json.loads(full_json(rows, eng.sensitivity(works), eng.config, 1_000_000))
        assert j["standard_version"] == SPEC_VERSION


# ---------------------------- 8. APP PARSING HELPERS -----------------------------

class TestAppParsers:
    def setup_method(self):
        src = open("app.py", encoding="utf-8").read()
        ast.parse(src)
        ns = {}
        exec(src.split("st.set_page_config")[0], ns)
        self.to_bool, self.to_int = ns["_to_bool"], ns["_to_int"]

    @pytest.mark.parametrize("raw,expected", [
        ("True", True), ("FALSE", False), (" yes ", True), ("0", False),
        ("1", True), ("nonsense", False), (float("nan"), False), (True, True),
    ])
    def test_to_bool(self, raw, expected):
        assert self.to_bool(raw) is expected

    @pytest.mark.parametrize("raw,expected", [
        ("1999", 1999), (1999.0, 1999), (float("nan"), 2000), ("", 2000), (None, 2000),
    ])
    def test_to_int(self, raw, expected):
        assert self.to_int(raw) == expected


# ---------------------------- 9. BENCHMARK THRESHOLDS ----------------------------

class TestBenchmarkThresholds:
    """Re-runs Benchmark v1 and asserts the published error characteristics hold."""

    def test_benchmark_metrics(self):
        from benchmark import evaluate
        r = evaluate()
        assert r["M1_calibration"]["MAE"] < 0.01
        assert r["M1_calibration"]["max_error"] < 0.02
        assert r["M2_false_positive_baseline"]["max_false_overlap"] < 0.01
        assert r["M3_consolidation"]["pass"] is True
        assert r["M4_anthology"]["abs_error"] < 0.05
