"""
Copyright 2026 Aswin Krishna. Licensed under the Apache License, Version 2.0 (see LICENSE).
Benchmark corpus: deterministic synthetic works + controlled noise injectors.

The generator produces works whose 8-grams are naturally near-unique (as with real
distinctive prose), so an unmodified work reads as high-uniqueness and a copied work
shares shingles with its source. Every function is seeded: identical seed -> identical
corpus, so results are reproducible by any third party (Standard: reproducibility).
"""
from __future__ import annotations

import random
import string

# a visually-plausible OCR confusion map (scanned-text errors)
_OCR = {
    "o": "0", "l": "1", "i": "1", "e": "c", "a": "s", "s": "5",
    "g": "9", "b": "6", "t": "f", "m": "rn", "n": "m", "u": "v",
}
# a small synonym map for the paraphrase injector
_SYN = {
    "large": "big", "small": "little", "quick": "fast", "begin": "start",
    "obtain": "get", "method": "approach", "however": "yet", "therefore": "thus",
    "demonstrate": "show", "utilise": "use", "sufficient": "enough",
    "numerous": "many", "purchase": "buy", "commence": "begin", "assist": "help",
}


def _vocab(rng: random.Random, size: int = 4000) -> list[str]:
    seen, out = set(), []
    while len(out) < size:
        w = "".join(rng.choices(string.ascii_lowercase, k=rng.randint(3, 9)))
        if w not in seen:
            seen.add(w)
            out.append(w)
    out.extend(_SYN.keys())  # ensure paraphrasable tokens can appear
    return out


def make_work_text(rng: random.Random, vocab: list[str], n_tokens: int) -> str:
    """A work: i.i.d. draws from a large vocabulary -> near-unique long n-grams."""
    return " ".join(rng.choices(vocab, k=n_tokens))


def ocr_noise(text: str, rate: float, rng: random.Random) -> str:
    out = []
    for ch in text:
        if ch != " " and rng.random() < rate:
            out.append(_OCR.get(ch, rng.choice(string.ascii_lowercase)))
        else:
            out.append(ch)
    return "".join(out)


def paraphrase(text: str, rate: float, rng: random.Random) -> str:
    toks = text.split()
    for i, t in enumerate(toks):
        if t in _SYN and rng.random() < rate:
            toks[i] = _SYN[t]
        elif rng.random() < rate * 0.15:      # light local reordering
            j = min(i + 1, len(toks) - 1)
            toks[i], toks[j] = toks[j], toks[i]
    return " ".join(toks)


def edition_variant(text: str, rate: float, rng: random.Random) -> str:
    """Minor edition differences: dropped/duplicated words, whitespace, punctuation."""
    toks = text.split()
    out = []
    for t in toks:
        r = rng.random()
        if r < rate * 0.4:
            continue                       # dropped word
        out.append(t)
        if r > 1 - rate * 0.2:
            out.append(t)                  # duplicated word
    return " ".join(out)


def copy_passages(source: str, target_filler: str, copy_frac: float,
                  contiguous: bool, rng: random.Random) -> str:
    """Build a copy: `copy_frac` of source text embedded in the target's own filler."""
    s = source.split()
    take = max(1, int(len(s) * copy_frac))
    if contiguous:
        start = rng.randint(0, max(0, len(s) - take))
        copied = s[start:start + take]
        filler = target_filler.split()
        return " ".join(filler[: len(filler) // 2] + copied + filler[len(filler) // 2:])
    # non-contiguous: scatter several source chunks through the filler
    filler = target_filler.split()
    n_chunks = rng.randint(3, 6)
    chunk = max(1, take // n_chunks)
    out = filler[:]
    for _ in range(n_chunks):
        st = rng.randint(0, max(0, len(s) - chunk))
        ins = rng.randint(0, len(out))
        out[ins:ins] = s[st:st + chunk]
    return " ".join(out)


NOISE_FUNCS = {
    "ocr": ocr_noise,
    "paraphrase": paraphrase,
    "edition": edition_variant,
}
