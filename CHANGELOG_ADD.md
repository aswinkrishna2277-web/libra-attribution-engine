### Added (Phase 2 — benchmarking)
- `benchmarks/` — scale-and-noise benchmark measuring shared-text detection (AUC)
  and allocation-share drift as corpus noise rises (OCR, edition variants,
  paraphrase). Deterministic synthetic corpus; also runs on a folder of real
  `.txt` files via `--texts`.
- `benchmarks/README.md` — methodology, results table, and AUC-vs-noise plot,
  with the OCR robustness threshold (~2% character error) disclosed as a limitation.
- `benchmarks/test_benchmark.py` — regression guards (perfect clean-baseline
  detection; reproducibility).
- CI extended to lint the benchmark, run its tests, and run a quick benchmark smoke.
