# Libra Project — Audit & Review Report v1
**Scope:** Standard v0.3, Module A engine v0.1, Demonstration Report, Red-Team Memo, Authorities File
**Method:** spec consistency read; engine-vs-spec conformance check; live reproducibility test; legal-asset review
**Verdict: CLEARED TO PROCEED** to interface build, with the queue below binding on that build.

---

## Findings

### Critical — none found.

### Material (3) — two fixed now, one queued

**M1. §6 tier mapping omitted A4 and mis-listed A3.** The admissibility tiers — the Standard's core legal innovation — failed to classify A4 at all and listed deferred A3 without qualification. An opposing expert reads §6 first. **FIXED:** A4 classified Tier A *when metadata-sourced via the published mapping table*; A3 marked "(from v2)."

**M2. §7 database-right claim was jurisdictionally wrong for the author.** The spec claimed "EU database right" for the benchmark, but the EU sui generis right (Dir. 96/9/EC) requires **EEA establishment** — unavailable to a non-EEA maker, and the author is heading to the **UK** (post-Brexit: separate UK database right under the 1997 Regulations). For an IP lawyer's flagship project, claiming an IP right one doesn't qualify for would be a credibility wound. **FIXED:** §7 now conditions protection on the maker's establishment and flags benchmark-build location as a deliberate legal decision.

**M3. Demo report overclaims Tier A for synthetic market scores.** The report states "All factors Tier A" but the demo's market scores were randomly assigned, not metadata-mapped — exactly the discretion-dressed-as-number the red-team's Objection 4 condemned. Acceptable in a synthetic demo *only if said aloud.* **QUEUED (binding):** next report generation must label demo market scores as synthetic placeholders and restate the Tier A condition.

### Conformance gaps — engine v0.1 vs Standard v0.3 (expected; red-team postdates engine)
All four are **binding requirements for the interface build**, already acknowledged:
1. Rightsholder-claim consolidation before redundancy discount (§4 A2).
2. A4 mechanical mapping table replacing free-set market scores (§4 A4).
3. Sensitivity analysis extended to technical parameters — shingle k, floor (§5).
4. Validation-status disclosure box in every report (§5).
Plus hardening: stable cryptographic shingle hashing (see T1).

### Tests run

**T1. Cross-process reproducibility: PASS.** Two independent runs produced byte-identical schedules (matching MD5). Analysis: outputs depend only on shingle *equality structure*, which Python's per-process hash seeding does not disturb; theoretical hash-collision variance remains. Cryptographic hashing stays queued as principled hardening for cross-platform forensic claims — the Standard's reproducibility promise should hold by construction, not by luck.

**T2. Allocation math: PASS.** Shares provably sum to 1 (floor/n × n + (1−floor) × Σscores, Σscores = 1); floor verified live (minimum allocation $12,073 > 0); engineered redundancy cases discounted in the predicted direction and order.

### Minor (3)
- Spec filename still says v0.1 while content is v0.3 — rename at next version to `Libra_Attribution_Standard.md` with version inside only.
- §8 should add a visible changelog table (v0.1 → v0.2 → v0.3 with one-line rationales) — governance §8 promises logged changes; practice what's promised.
- Engine docstring should cite spec version it implements and gain a `SPEC_VERSION` constant checked at report time.

### Strategic notes (no action this build, decide before public launch)
- **S1. Name clearance.** "Libra" carries search-noise from Meta's abandoned cryptocurrency and is a common mark. Before anything public: trademark availability search in the classes that matter (legal-tech SaaS), and consider "Libra Standard"/distinctive composite. Low urgency, real before launch.
- **S2. Benchmark build location** (links to M2): if built during the Belfast year, UK database right applies; an EEA-established structure would be needed for EU sui generis cover. A deliberate choice, made on advice — not an accident.
- **S3. Authorities File discipline holds:** nothing in any document cites an unverified authority as settled; verification protocol embedded. Maintain this invariant — it is the project's reputation.

---

## Clearance
The methodology layer is internally consistent, adversarially tested, and honest about its validation status. The implementation layer has a defined, finite conformance queue. **Proceed to the interface build, which must ship with conformance items 1–4 + T1 hardening + M3 disclosure.**

---

# Audit v2 — Final Pre-Release Pass (full-project error check)

**Scope:** every deliverable as of engine v0.2 / app v1 / Standard v0.3. **Method:** torture tests on engine edge cases and the CSV upload path; reboot test; document consistency closeout.

## Bugs found and FIXED this pass
1. **CRITICAL (upload path): blank `pub_year` crashed the app.** `int(NaN)` raised ValueError on any CSV with an empty metadata cell — guaranteed with real-world works lists. Fixed with guarded `_to_int` (default 2000).
2. **Latent (upload path): string-typed booleans.** A CSV cell like `"False"` arriving as a string would evaluate truthy under `bool()`. Fixed with `_to_bool` accepting true/1/yes/y/t case-insensitively; verified against deliberately dirty CSV (`FALSE`, `" True "`, `nonsense`, empty) — all parse sanely.
3. **Hardening: replaced `pd.io.common.BytesIO`** (semi-private pandas API, works on pandas 3.0.2 but fragile across versions) with standard `io.BytesIO`.

## Tests passed this pass
- Single-claim corpus: allocates 100%, sensitivity returns Spearman 1.0, no division errors.
- Empty-text work: floor guarantees nonzero allocation ($20,250 on test pool); no crash.
- Cross-process reproducibility (blake2 hashing): byte-identical schedules, two independent runs.
- Dirty-CSV upload simulation: no crashes, sane values.
- App reboot after fixes: HTTP 200, zero errors in log.
- Engine invariant: shares sum to 100.00% (asserted programmatically).
- All mandatory disclosures (validation status, synthetic metadata, mapping table, consolidation statement) verified present in generated report.

## Document closeout
- Canonical spec created as `Libra_Attribution_Standard.md` with §8 changelog table (audit v1 minor items closed). The earlier `..._v0.1.md` filename is retained only as history; use the canonical file.
- Engine v0.1 (`libra_module_a.py`) is **superseded** by `libra_engine.py` — archive, do not deploy.

## Verdict
**RELEASE-READY at prototype grade.** No known crashes; all spec conformance items closed; all mandatory disclosures generated; reproducibility proven. Remaining known limitations are *disclosed by design* (pre-validation status; synthetic demo metadata; cross-claimant symmetric discount pending v2 provenance-priority factor).
