# Libra — Compliance & Legal Posture Memo v1
**Scope:** the Libra Attribution Engine as publicly deployed (GitHub repo + Streamlit demo). Prepared before public announcement. This memo records analysis and implemented mitigations; it is internal work product, not legal advice to third parties.

---

## 1. EU AI Act — is Libra itself an "AI system"? Almost certainly NOT.

The Act's obligations attach to "AI systems" — machine-based systems that infer, from inputs, how to generate outputs, with elements of autonomy/adaptiveness. Libra is **deterministic, rule-based arithmetic**: cryptographic shingle counting, a published lookup table, disclosed linear formulas. It learns nothing, adapts nothing, and infers nothing in the Act's sense; identical inputs produce bit-identical outputs by design. Deterministic software executing human-defined rules is the paradigm case *outside* the AI-system definition.

This is not an accident — it is the methodology's evidentiary core (Tier A = deterministic = reproducible by opposing experts), and it doubles as the compliance posture. **Marketing line that is also true:** *Libra is not AI; it is a transparent calculator for an AI-era problem.*

**Watch items (reopen analysis if):** (a) a future version incorporates ML components (e.g., Module B's semantic signals — those WILL need this analysis done properly); (b) the tool is marketed specifically to judicial authorities, which implicates a sensitive Annex III area. Neither applies to v1 as deployed.

## 2. GDPR — the real European exposure, and the mitigation now implemented

Works lists contain author names and rightsholder identifiers — **personal data**. The public demo runs on third-party US-based cloud infrastructure; the engine itself stores nothing (no database, no logging of uploads in our code), but processing occurs on that infrastructure.

**Architecture answer:** two lawful paths, now made explicit in-app:
- **Public demo** = synthetic/sample data only. The app now displays a data-protection notice: *do not upload confidential or personal data to this public demo.*
- **Real data** = local execution (README instructions). Data never leaves the user's machine; no transfer, no processor relationship. This is the GDPR-clean production path and should be the only path ever recommended for live matters.

Residual note: we are not, by design, a controller/processor of users' real data, because the tool's stated terms direct real data away from the hosted demo. Honest posture, clearly signposted — implemented this build.

## 3. Liability & unauthorized-practice posture — implemented

Every generated dossier now embeds: research/demonstration output, **not legal advice**, no professional relationship created, professional review required before use in any live matter. The same notice appears in the app interface and footer. The tool outputs *methodology results*; characterizing their legal significance remains the work of qualified counsel — saying so explicitly is both accurate and protective.

## 4. Currency — implemented, with the doctrinally pleasing answer

USD/EUR/GBP selector added. Crucially: **Libra's mathematics is proportional** — shares of a pool — so currency is purely a denomination label. No exchange-rate conversion is performed or implied, and every report now states its denomination and says so. A cross-jurisdictional standard that never touches FX is *more* defensible, not less: nothing in the methodology varies by jurisdictional currency.

## 5. Code licence — DECISION REQUIRED (yours)

The repo currently has **no LICENSE file** → default: all rights reserved (viewing/forking within GitHub permitted by its ToS, nothing more). Options:

| Option | Effect | Fit with strategy |
|---|---|---|
| **MIT / Apache-2.0** | Anyone may use/modify/commercialize the engine code (Apache adds patent grant + requires preserving notices) | Maximizes adoption — and standards win by adoption; your moat was always authorship + benchmark + brand, not the engine code. **Recommended** (Apache-2.0 slightly preferred for the notice-preservation) |
| PolyForm Noncommercial | Free for non-commercial use; commercial use needs your licence | Preserves commercialization option; slows adoption; "open standard" claim weakens |
| No licence (status quo) | Legal ambiguity; serious users won't touch it | Worst of both — decide soon |

Whatever you choose: copyright notices ("© 2026 Aswin Krishna") are now in the code headers and app footer. The **Standard documents, benchmark, and validation assets remain unpublished and yours** regardless of the code licence — that separation is the "spec open, infrastructure owned" architecture working as intended.

## 6. Trademark — open item, unchanged

"Libra" clearance (legal-tech/SaaS classes) before commercialization or paid offerings. Not a blocker for announcing a research project by name. Search noise from Meta's abandoned "Libra" cryptocurrency is a discoverability nuisance, not a legal conflict in our classes — but verify properly before money changes hands under the name.

## 7. What "verified and compliant" honestly means (for your announcement)

You may truthfully state: deterministic methodology; 41-test automated suite; published benchmark error characteristics; cross-platform reproducibility confirmed to the cent; legal notices and data-protection signposting embedded; not an AI system under the EU AI Act as deployed; GDPR-clean local path documented. You should **not** state: "100% compliant," "guaranteed," "court-approved," or "validated for production use" — absolutes are the one claim that can always be falsified. The honest formulation is stronger anyway: *verified, disclosed, and adversarially tested.*

---
### Action list
- [x] Currency support (USD/EUR/GBP) — implemented & tested
- [x] In-app legal + data-protection notices — implemented
- [x] Dossier-embedded disclaimer — implemented (every report, all formats)
- [x] Copyright notices — implemented
- [ ] **Your call:** licence choice (recommendation: Apache-2.0)
- [ ] Trademark clearance before commercialization
- [ ] Re-upload `app.py` + `libra_engine.py` to GitHub (auto-redeploys in ~2 min)
