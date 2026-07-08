# Libra Module A — Red-Team Memo / Design Record
**Against:** Demonstration Report v0.1 / Standard v0.2 · **Disposition:** amendments applied in Standard v0.3
**Record status: LIVING DOCUMENT (v1.1).** Objections 1–8 were raised in pre-release adversarial review conducted by the author with AI assistance, simulating opposing counsel. Objection 9 was raised in post-release external review and added with its answer — this record grows under fire, which is its purpose. Dispositions marked *superseded* were implemented after the objection was recorded.

Each objection is stated at full strength, then answered. Where the answer required changing the Standard, the change is recorded. Objections are ordered by danger.

---

## Objection 1 — "Differentiated allocation invites intra-class conflict" (THE STRONGEST)
*"Flat-rate in Bartz was not ignorance; it was negotiated administrability. A differentiated plan pits class members against each other, raising adequacy-of-representation concerns under Amchem/Ortiz, inviting subclassing fights and a wave of objections. Your 'better' methodology makes settlements harder, not fairer."*

**Response — and the discovery that turns this objection into Libra's best authority.** Differentiated, formula-driven allocation is not novel or destabilizing: it is the *standard architecture of securities class action settlements*, where "recognized loss" formulas allocate by objective per-claimant criteria (shares, dates, price drops) and are approved routinely under the reasonable-basis standard. Courts do not subclass securities settlements because the formula differentiates; differentiation by **objective, mechanically-applied criteria** is precisely what avoids adequacy problems. Libra is the copyright analogue: a **"recognized contribution" formula**. The objection, answered properly, supplies Module A's strongest precedent family.
**Amendment:** Securities recognized-loss analogy added to Standard §3. Positioning language adopted: *Libra is to copyright settlements what recognized-loss plans are to securities settlements.*

## Objection 2 — "You discounted the victim" (symmetric redundancy)
*"Work W005's author did nothing but be copied by W101, and your engine cut her allocation 25%. You punish the plagiarized to spare the pool."*

**Response.** Two-part fix, and the first part dissolves most real-world cases: in a Bartz-type corpus, duplication is overwhelmingly *edition-level* — the same work appearing twice — meaning both copies typically belong to the **same rightsholder**. The Standard now requires **consolidation to the rightsholder-claim level before any redundancy discount**: editions/duplicates of one claimant merge into one claim, so the discount never fires against a claimant for "duplicating" herself. For the residual case of genuinely distinct claimants with overlapping content, v2's provenance-priority factor (publication-date metadata) protects the senior work.
**Amendment:** §4 A2 now begins with mandatory rightsholder-level consolidation. Provenance-priority confirmed on the v2 roadmap.

## Objection 3 — "Word-counting is not valuation"
*"A 900-page potboiler outweighs a Pulitzer-winning novella ten to one in your schedule. Copyright has never priced works by the pound."*

**Response.** Volume is not offered as *value* — it is offered as **exposure**: token count is the deterministic measure of how much of a work the training process actually consumed, which is the conduct being compensated. It is one factor (default 70%), bounded by the market factor and the floor, with expressive-density refinement scheduled (A3, v2). And the governing standard is *Sheldon*'s reasonable approximation: the legally relevant comparison is not volume-vs-perfection but volume-vs-flat-rate, and flat rate is the cruder approximation by any measure.
**Amendment:** Written defense of the volume proxy added to §4 A1 (exposure rationale).

## Objection 4 — "Your market score is an opinion wearing a number"
*"Who decided Work 17 is a 0.96 and Work 39 a 0.15? An expert's vibe is not Tier A."*

**Response.** Conceded as to the demo's random assignment; cured by construction. The Standard now defines A4 as a **mechanical mapping from observable, verifiable metadata** — in-print status, retail availability, publication recency — via a published lookup table. Anyone with the same metadata reproduces the same scores. Discretion is removed from scoring and relocated to the *published table*, where it is visible and contestable in advance.
**Amendment:** §4 A4 redefined as closed-taxonomy mechanical mapping; published mapping table required.

## Objection 5 — "Why 15%? Why 70/30? Why 8-word shingles?"
*"Every parameter is a confession of arbitrariness."*

**Response.** Three different answers for three different parameters. The **floor** is now expressly a *tribunal-set policy parameter with a disclosed default* — Libra's contribution is making explicit a choice flat-rate plans make implicitly (flat rate is a 100% floor, undisclosed). The **weights** were always adjustable-with-disclosure. The **technical parameters** (shingle k) get the same treatment as weights: the mandatory sensitivity analysis now extends to them, so the report shows allocation stability under parameter variation rather than asking anyone to trust the defaults.
**Amendment:** §5 sensitivity analysis extended to technical parameters; floor reframed in §5 as tribunal parameter with disclosed default.

## Objection 6 — "Deterministic is not valid" (the Daubert error-rate gap)
*"Tier A means reproducible, not correct. Where is your known error rate against ground truth?"*

**Response.** Correct, and the Standard says so itself: that is what the §7 validation benchmark exists to supply, and until it runs, every report must say so. Candor here is cheap now and priceless later.
**Amendment:** Mandatory **validation-status disclosure** in every report. *(Superseded: Benchmark v1 has since been run and its error characteristics published — see Libra_Validation_Report.md. Reports now carry the validated-measurable-layer status; independent replication remains pending and is invited.)*

## Objection 7 — "Shares are unstable across claim filing"
*"Every late claim reshuffles everyone's allocation. Your schedule is a moving target."*

**Response.** Inherent to apportioning any fixed pool — flat-rate plans recalculate per-work amounts as claims arrive too (Bartz's own payout estimates moved with the claim rate). Pro-rata recalculation at the claims deadline is ordinary settlement administration. Noted in the Standard; no design change required.

## Objection 8 — "Python's hash() is not forensic-grade"
*"Your shingle hashing is runtime-seeded and collision-prone; two runs on two machines may disagree."*

**Response.** Fair at the implementation level (not the methodology level). The reference implementation will move to a stable cryptographic hash (e.g., SHA-1 over shingle bytes) so identical inputs yield bit-identical outputs across machines — a property an evidentiary tool should have.
**Amendment:** Queued for the engine's next build (with rightsholder consolidation). *(Superseded: implemented — engine v0.2 ships blake2b cryptographic shingle hashing; cross-platform reproducibility subsequently confirmed to the cent.)*

## Objection 9 — "Bartz was a statutory-damages case; flat allocation TRACKED the legal theory" (ADDED v1.1, raised in external review)
*"Each timely-registered work carried an identical statutory claim under 17 U.S.C. § 504(c), regardless of whether it shaped the model or barely registered. Flat per-work allocation therefore tracked the legal theory of the case — one registered work, one statutory claim — plus administrability, itself a recognized Rule 23(e) fairness factor. Contribution-weighting answers a question the cause of action never asks. Your formula is fighting the doctrine, not filling a void."*

**Response — concede the frame, contest the conclusion, relocate the strength.** Three parts. *First*, the concession: flat per-work is indeed a principle (claim parity plus administrability), and Libra's accurate claim is narrower than "the court lacked a methodology" — it is that objectors and the court lacked a principled **alternative** to weigh, which is precisely what Rule 23(e) fairness review needs to be meaningful. *Second*, the doctrinal contest: § 504(c) statutory damages are not a fixed sum but a per-work **band** ($750–$150,000), calibrated in every contested case by work-specific factors — the value of the work, the harm, willfulness. Per-work differentiation is therefore *inside* the statutory scheme, and Libra's market-exposure factor proxies exactly the calibration factors courts already apply; the objection proves too much, since it would condemn ordinary statutory-damages calibration alongside Libra. The factor that sits least comfortably in the statutory frame — volume-as-exposure — is candidly strongest elsewhere. *Third*, the relocation: Libra's primary homes are the contexts whose legal theory genuinely prices contribution — actual-damages and lost-licensing-value theories, negotiated licensing pools, and CMO distribution (where EU law requires fair, published policies and parties may adopt any allocation rule). In statutory-damages class settlements, Libra's honest role is the **objectors' instrument**: the concrete alternative placed before the court — the same role recognized-loss critiques played in securities law before they became the standard.
**Amendment:** this two-track positioning (objectors' instrument in litigation; distribution policy itself in licensing/CMO contexts) is adopted into all public framing and will be a dedicated section of the specification paper.

---

### Net effect
Nine objections (eight pre-release, one from post-release external review); none survives at full strength; five forced amendments that make the Standard harder to attack; one (Objection 1) converted into Libra's best supporting authority. This memo becomes Annex I of the eventual article — showing the methodology was adversarially tested *by design*.
