# The Libra Attribution Standard
## Methodology Specification — v0.3 (Working Draft; legal due diligence + adversarial red-team applied)

**Author:** Aswin Krishna
**Status:** Internal working draft for iteration. Not for circulation.

---

## 1. Purpose and Positioning

The Libra Attribution Standard ("Libra") is a methodology for **apportioning AI training-data compensation among rightsholders where the training relationship is established** — in settlement allocation, collective licensing pools, and post-disclosure litigation.

The need is demonstrated, not hypothetical. In *Bartz v. Anthropic*, the largest copyright recovery in U.S. history (~$1.5B) was allocated at a flat ~$3,000 per work across ~500,000 works — identical treatment for works of vastly different contribution, expressive weight, and market exposure. Class members formally objected to allocation fairness. No principled alternative methodology existed for the court, the administrator, or the objectors to invoke. Libra is designed to be that methodology.

**Positioning statement:** Libra translates ninety years of copyright apportionment doctrine (the *Sheldon v. MGM* line; UK account-of-profits apportionment) into a computable, auditable, evidentiary-grade method for the AI training context.

## 2. Scope Boundary (What Libra Does Not Claim)

This section is a feature, not a disclaimer. Libra's credibility rests on claiming only what current science can defend.

- Libra does **not** infer what a black-box model was trained on. Training-data attribution for production LLMs from the outside remains an unsolved research problem, and any method claiming otherwise will not survive expert challenge.
- Libra operates only where the corpus or candidate source set is **known** — via contract, disclosure, discovery, or settlement works lists.
- Libra reports an **unattributable residual** wherever contribution cannot be responsibly assigned, rather than forcing a full allocation.
- Similarity is treated as evidence of *presence and weight*, never as proof of *causation*, and is tiered accordingly (§6).

## 3. Legal Foundations

1. **Apportionment doctrine.** *Sheldon v. Metro-Goldwyn Pictures*, 309 U.S. 390 (1940): an infringer's profits may be apportioned between infringing and non-infringing contributions by reasoned, evidence-based approximation — "not mathematical exactness but only a reasonable approximation." Libra extends this *principle of principled approximation* by explicit analogy from defendant-side profits apportionment to claimant-side allocation. UK equivalent: apportionment in account of profits.
2. **Plan-of-allocation doctrine (Module A's direct hook).** U.S. class settlement allocation plans are approved under Fed. R. Civ. P. 23(e) where they rest on a *reasonable, rational basis*; courts routinely accept differentiated allocation grounded in relative claim strength. Flat per-work allocation is permissible but not required — a methodology supplying a stronger rational basis enters through a door the law already holds open.
3. **Damages factors.** Statutory damages jurisprudence already weighs willfulness, market harm, and the nature of the work — establishing that *per-work differentiation is the doctrinal norm*, making flat-rate allocation the anomaly Libra corrects.
4. **Admissibility design constraints.** Every quantitative element is designed against *Daubert* (testability, known error characteristics, standards governing operation, general-acceptance trajectory) and CPR Part 35 (expert independence, statement of methodology limits).
5. **Regulatory context.** EU AI Act Art. 53 disclosure obligations, CDSM Art. 4 reservations, and state-level disclosure laws progressively convert "unknown corpus" cases into "known corpus" cases — expanding Libra's operative domain over time.
6. **Securities recognized-loss analogy (adopted positioning).** Differentiated, formula-driven settlement allocation by objective per-claimant criteria is the settled architecture of securities class actions ("recognized loss" plans), routinely approved under the reasonable-basis standard without triggering subclassing. Libra is the copyright analogue: a **recognized-contribution formula**. *Libra is to copyright settlements what recognized-loss plans are to securities settlements.*

## 4. Architecture: Two Modules, Two Live Markets

### Module A — Corpus Apportionment (the *Bartz* problem)
**Input:** a known training corpus (works list) + a compensation pool.
**Output:** a per-work allocation schedule with stated rationale per factor.

Per-work factors (each computable from the corpus itself):
- **A1. Volume share** — deduplicated token count of the work relative to corpus. *Rationale: volume is offered as **exposure**, not value — the deterministic measure of how much of the work the training process consumed, which is the conduct being compensated.*
- **A2. Redundancy discount** — applied only **after mandatory consolidation to the rightsholder-claim level** (editions/duplicates of one claimant merge into one claim, so no claimant is discounted for "duplicating" herself). Residual cross-claimant overlap is discounted symmetrically in v1; a provenance-priority factor (publication-date seniority) protects the senior work from v2.
- **A3. Expressive density** — deferred to v2 per locked decisions.
- **A4. Market-exposure factor** — a **mechanical mapping from observable, verifiable metadata** (in-print status, retail availability, publication recency) via a published lookup table. No expert discretion at scoring time; discretion lives only in the published table, contestable in advance.

### Module B — Output Apportionment (the licensing / per-inference problem)
**Input:** an AI output + a known candidate source set.
**Output:** per-source contribution scores with admissibility tier and residual.

Signals:
- **B1. Verbatim / near-verbatim overlap** — longest common spans, n-gram overlap. Deterministic; highest evidentiary weight; mirrors substantial-similarity reasoning.
- **B2. Structural / paraphrase overlap** — ordered-sequence and paraphrase detection; medium weight.
- **B3. Semantic proximity** — baseline-corrected embedding similarity; corroborative only, never dispositive.

## 5. Apportionment Computation

- Each factor/signal is scored 0–1 and combined by **doctrinally justified weights** (each weight carries a written legal rationale, not merely a statistical one).
- Scores are normalised across the work/source set into proportional shares.
- The **base floor** (Module A) is expressly a **tribunal-set policy parameter with a disclosed default** — Libra makes explicit a choice flat-rate plans make implicitly (flat rate is a 100% floor, undisclosed). The **residual** (Module B) is always reported.
- **Sensitivity analysis is mandatory and extends to technical parameters:** every Libra report shows how allocations shift under reasonable variation of weights *and* technical parameters (e.g., shingle size). Stability under perturbation is a *Daubert* virtue; hiding it is a litigation liability.
- **Validation-status disclosure is mandatory:** every report states the methodology's current validation status against the §7 benchmark (current status: pre-validation prototype).

## 6. Admissibility Tiers

- **Tier A — Evidentiary.** Driven by deterministic measures: A1–A2, B1, and A4 *when sourced from verifiable metadata via the published mapping table*. Reproducible by opposing experts from the same inputs. Offered as primary evidence.
- **Tier B — Corroborative.** Model-assisted measures: B2, B3, and A3 (from v2). Offered in support, never alone.
- **Tier C — Indeterminate.** Below threshold. Explicitly reported as *no finding*, not as zero contribution.

## 7. Validation Programme (the owned asset)

A ground-truth benchmark: a controlled corpus with known composition and engineered overlap relationships, against which Libra's scores are validated and error characteristics published. The benchmark design and dataset are proprietary — protected by **database right under the law of the maker's establishment** (UK database right under the Copyright and Rights in Databases Regulations 1997 if made while UK-established; EU sui generis right under Directive 96/9/EC requires EEA establishment and is *not* available to non-EEA makers) — plus copyright in selection and arrangement. Where the benchmark is built matters legally and must be decided deliberately. The methodology specification is public. *Spec open, infrastructure owned.*

## 8. Versioning and Governance

The Standard is versioned (v0.1 → v1.0 at first public release). Changes are logged with rationale. Reference implementation: the **Libra Attribution Engine**.

---

### Decisions locked by the author (v0.2)
1. **Module priority:** Module A first — the documented allocation void, deterministic-friendly, lawyer-shaped.
2. **Weighting philosophy:** context-adjustable weights with **mandatory disclosure** of weights and rationale in every report (Daubert-aligned; honesty as brand).
3. **Expressive density (A3):** deferred to v2 — launch lean and defensible; add the model-assisted refinement once the deterministic core is established.

---

## Changelog (§8 governance, practiced)

| Version | Change | Rationale |
|---|---|---|
| v0.1 | Initial specification: scope boundary, two-module architecture, three-tier admissibility, residual discipline. | Founding draft. |
| v0.2 | *Sheldon* reframed as explicit defendant-to-claimant analogy; Rule 23(e) plan-of-allocation doctrine added as Module A's direct hook; author's three decisions locked (Module A first; adjustable weights w/ disclosure; A3 deferred). | Legal due diligence. |
| v0.3 | Securities recognized-loss analogy adopted (§3.6); mandatory rightsholder-claim consolidation before redundancy discount; A4 redefined as mechanical mapping from verifiable metadata; floor reframed as tribunal-set parameter; sensitivity extended to technical parameters; mandatory validation-status disclosure; §6 tiers corrected (A4 classified; A3 marked v2); §7 database-right claim conditioned on maker's establishment (UK vs EEA). | Adversarial red-team (8 objections) + audit v1 (findings M1, M2). |
