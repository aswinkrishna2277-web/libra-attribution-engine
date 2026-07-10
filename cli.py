"""
Copyright 2026 Aswin Krishna. Licensed under the Apache License, Version 2.0 (see LICENSE).
Libra Attribution Engine — command-line interface.

Usage examples:
  libra demo
  libra score corpus.csv --pool 1000000 --format md -o report.md
  libra score corpus.jsonl --w-volume 0.6 --floor 0.10 --format json
  libra sensitivity corpus.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from libra_engine import (
    ENGINE_VERSION,
    SPEC_VERSION,
    CorpusApportionmentEngine,
    Work,
    build_demo_corpus,
    full_json,
    report_markdown,
    rows_to_csv,
)

REQUIRED_COLUMNS = ("work_id", "title", "author", "rightsholder_id", "text")
BOOL_TRUE = {"1", "true", "yes", "y", "t"}


def _to_bool(v, default=False) -> bool:
    if isinstance(v, bool):
        return v
    if v is None:
        return default
    return str(v).strip().lower() in BOOL_TRUE


def _to_int(v, default=0) -> int:
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return default


def load_corpus(path: Path) -> list:
    """Load works from CSV or JSONL. Text may be inline ('text') or a file path ('text_path')."""
    if not path.exists():
        raise SystemExit(f"corpus file not found: {path}")
    works, rows = [], []
    if path.suffix.lower() in (".jsonl", ".ndjson"):
        with path.open(encoding="utf-8") as f:
            rows = [json.loads(line) for line in f if line.strip()]
    elif path.suffix.lower() == ".json":
        rows = json.loads(path.read_text(encoding="utf-8"))
    elif path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
    else:
        raise SystemExit(f"unsupported corpus format: {path.suffix} (use .csv, .json, or .jsonl)")

    for i, r in enumerate(rows, 1):
        missing = [c for c in REQUIRED_COLUMNS if c not in r and not (c == "text" and "text_path" in r)]
        if missing:
            raise SystemExit(f"row {i}: missing required column(s): {', '.join(missing)}")
        text = r.get("text") or ""
        if not text and r.get("text_path"):
            tp = Path(r["text_path"])
            if not tp.exists():
                raise SystemExit(f"row {i}: text_path not found: {tp}")
            text = tp.read_text(encoding="utf-8")
        works.append(
            Work(
                work_id=str(r["work_id"]),
                title=str(r.get("title", "")),
                author=str(r.get("author", "")),
                rightsholder_id=str(r["rightsholder_id"]),
                text=text,
                in_print=_to_bool(r.get("in_print")),
                retail_available=_to_bool(r.get("retail_available")),
                pub_year=_to_int(r.get("pub_year"), 0),
                notes=str(r.get("notes", "")),
            )
        )
    if not works:
        raise SystemExit("corpus is empty")
    return works


def _emit(text: str, out: str | None) -> None:
    if out:
        Path(out).write_text(text, encoding="utf-8")
        print(f"written: {out}", file=sys.stderr)
    else:
        print(text)


def cmd_score(args: argparse.Namespace) -> int:
    works = build_demo_corpus() if args.corpus == "demo" else load_corpus(Path(args.corpus))
    engine = CorpusApportionmentEngine(shingle_k=args.k)
    claims = engine.analyze(works, k=args.k, w_volume=args.w_volume, base_floor=args.floor,
                            measure=args.measure)
    rows = engine.allocate(claims, args.pool)
    sens = engine.sensitivity(works)
    cfg = engine.config
    synthetic = args.corpus == "demo"
    if args.format == "md":
        _emit(report_markdown(rows, sens, cfg, args.pool, args.k, synthetic_metadata=synthetic,
                              currency=args.currency), args.out)
    elif args.format == "csv":
        _emit(rows_to_csv(rows), args.out)
    else:
        _emit(full_json(rows, sens, cfg, args.pool, currency=args.currency), args.out)
    return 0


def cmd_sensitivity(args: argparse.Namespace) -> int:
    works = build_demo_corpus() if args.corpus == "demo" else load_corpus(Path(args.corpus))
    engine = CorpusApportionmentEngine(shingle_k=args.k)
    sens = engine.sensitivity(works)
    _emit(json.dumps(sens, indent=2, ensure_ascii=False), args.out)
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    args.corpus = "demo"
    return cmd_score(args)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="libra",
        description=f"Libra Attribution Engine v{ENGINE_VERSION} (Standard v{SPEC_VERSION}) — "
                    "deterministic, reproducible apportionment of a fixed pool across a known corpus.",
    )
    p.add_argument("--version", action="version",
                   version=f"libra-attribution-engine {ENGINE_VERSION} (standard {SPEC_VERSION})")
    sub = p.add_subparsers(dest="command", required=True)

    def common(sp):
        sp.add_argument("--k", type=int, default=8, help="shingle length (default: 8)")
        sp.add_argument("--w-volume", type=float, default=None, dest="w_volume",
                        help="weight on the exposure measure, 0..1 (default: engine default 0.70)")
        sp.add_argument("--floor", type=float, default=None,
                        help="disclosed minimum-share floor, 0..1 (default: engine default 0.15)")
        sp.add_argument("--measure", choices=("per-word", "per-work"), default=None,
                        help="exposure basis: 'per-word' (default, volume-weighted) or "
                             "'per-work' (length-normalised)")
        sp.add_argument("--pool", type=float, default=1_000_000.0,
                        help="pool size to allocate (default: 1,000,000)")
        sp.add_argument("--currency", default="USD", help="currency label for reports (default: USD)")
        sp.add_argument("--format", choices=("md", "csv", "json"), default="md",
                        help="output format (default: md)")
        sp.add_argument("-o", "--out", default=None, help="write output to file instead of stdout")

    sp = sub.add_parser("score", help="score a corpus and emit the audit report")
    sp.add_argument("corpus", help="corpus file (.csv/.json/.jsonl) or 'demo'")
    common(sp)
    sp.set_defaults(func=cmd_score)

    sp = sub.add_parser("sensitivity", help="emit the mandatory sensitivity analysis as JSON")
    sp.add_argument("corpus", help="corpus file (.csv/.json/.jsonl) or 'demo'")
    common(sp)
    sp.set_defaults(func=cmd_sensitivity)

    sp = sub.add_parser("demo", help="run the built-in demonstration corpus")
    common(sp)
    sp.set_defaults(func=cmd_demo)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
