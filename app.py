"""
Libra — Attribution Engine (web interface)
Reference implementation of the Libra Attribution Standard v0.3 · Module A
Methodology: Aswin Krishna
Run locally:  streamlit run app.py
"""

import io

import streamlit as st
import pandas as pd


def _to_bool(v) -> bool:
    """Robust against dirty CSV metadata: 'True', 'false', 'YES', 1, NaN…"""
    if isinstance(v, bool):
        return v
    try:
        if pd.isna(v):
            return False
    except (TypeError, ValueError):
        pass
    return str(v).strip().lower() in ("true", "1", "yes", "y", "t")


def _to_int(v, default: int = 2000) -> int:
    try:
        if pd.isna(v):
            return default
        return int(float(v))
    except (TypeError, ValueError):
        return default

from libra_engine import (
    CorpusApportionmentEngine, WeightConfig, Work,
    build_demo_corpus, report_markdown, rows_to_csv, full_json,
    MARKET_MAPPING_TABLE, VALIDATION_STATUS, SPEC_VERSION, ENGINE_VERSION,
)

st.set_page_config(page_title="Libra Attribution Engine", page_icon="⚖️", layout="wide")

# ------------------------------- header ----------------------------------------
st.title("⚖️ Libra Attribution Engine")
st.markdown(
    f"**Reference implementation of the Libra Attribution Standard v{SPEC_VERSION} · "
    f"Module A: Corpus Apportionment · Engine v{ENGINE_VERSION}**  \n"
    "Methodology: **Aswin Krishna** — a recognized-contribution formula for AI training-data "
    "compensation: *to copyright settlements what recognized-loss plans are to securities settlements.*"
)
st.warning(f"**Validation status (Standard §5, mandatory disclosure):** {VALIDATION_STATUS}")
st.caption("**Legal notice:** research & demonstration tool — not legal advice; outputs require professional review. "
           "**Data protection:** do NOT upload confidential or personal data to this public demo "
           "(it is processed on third-party cloud infrastructure). For real or sensitive works lists, "
           "run Libra locally per the README — your data then never leaves your machine.")

# ------------------------------- sidebar ----------------------------------------
st.sidebar.header("Methodology parameters")
st.sidebar.caption("Context-adjustable with mandatory disclosure (Standard §5). "
                   "Every report embeds these values and their written rationale.")
w_volume = st.sidebar.slider("Weight: volume (exposure)", 0.0, 1.0, 0.70, 0.05)
st.sidebar.caption(f"Weight: market-exposure = **{1 - w_volume:.2f}** (weights sum to 1)")
base_floor = st.sidebar.slider("Base floor (tribunal-set parameter)", 0.0, 0.5, 0.15, 0.05,
                               help="Per-se inclusion value: share of the pool allocated equally per claim. "
                                    "Flat-rate is a 100% floor, undisclosed. Libra makes the choice explicit.")
currency = st.sidebar.selectbox("Currency", ["USD", "EUR", "GBP"], index=0,
                                help="Denomination label only — Libra's allocation is proportional and currency-agnostic; no exchange-rate conversion is performed.")
CSYM = {"USD": "$", "EUR": "€", "GBP": "£"}[currency]
pool = st.sidebar.number_input(f"Compensation pool ({currency})", min_value=1000.0,
                               value=1_500_000.0, step=50_000.0, format="%.0f")
with st.sidebar.expander("A4 published mapping table"):
    st.table(pd.DataFrame(MARKET_MAPPING_TABLE, columns=["Metadata condition", "Score"]))
    st.caption("Discretion lives in this published table, contestable in advance — "
               "never at scoring time (Standard §4 A4).")

# ------------------------------- data input -------------------------------------
st.header("1 · Corpus")
tab_demo, tab_upload = st.tabs(["Demonstration corpus (engineered ground truth)", "Upload works list (CSV)"])

works = None
synthetic = False

with tab_demo:
    st.markdown(
        "28 synthetic works → 27 rightsholder claims, with three **engineered cases**: "
        "same-rightsholder editions (consolidation protects the claimant), a cross-rightsholder "
        "derivative (redundancy discount fires), and an anthology lifted from four donors."
    )
    if st.button("Load demonstration corpus", type="primary"):
        st.session_state["works_source"] = "demo"

with tab_upload:
    st.markdown(
        "CSV columns: `work_id, title, author, rightsholder_id, text, in_print, retail_available, pub_year`"
    )
    up = st.file_uploader("Works list CSV", type=["csv"])
    if up is not None:
        st.session_state["works_source"] = "upload"
        st.session_state["uploaded_csv"] = up.getvalue()

src = st.session_state.get("works_source")
if src == "demo":
    works = build_demo_corpus()
    synthetic = True
elif src == "upload" and st.session_state.get("uploaded_csv"):
    try:
        df = pd.read_csv(io.BytesIO(st.session_state["uploaded_csv"]))
        required = {"work_id", "title", "author", "rightsholder_id", "text"}
        missing = required - set(df.columns)
        if missing:
            st.error(f"Missing required columns: {sorted(missing)}")
        else:
            works = [Work(
                work_id=str(r.work_id), title=str(r.title), author=str(r.author),
                rightsholder_id=str(r.rightsholder_id), text=str(r.text),
                in_print=_to_bool(getattr(r, "in_print", False)),
                retail_available=_to_bool(getattr(r, "retail_available", False)),
                pub_year=_to_int(getattr(r, "pub_year", 2000)),
            ) for r in df.itertuples()]
    except Exception as e:
        st.error(f"Could not parse CSV: {e}")

# ------------------------------- run --------------------------------------------
if works:
    st.header("2 · Allocation")
    cfg = WeightConfig(w_volume=round(w_volume, 2), w_market=round(1 - w_volume, 2),
                       base_floor=round(base_floor, 2))
    engine = CorpusApportionmentEngine(cfg)
    claims = engine.analyze(works)
    rows = engine.allocate(claims, pool)
    flat = pool / len(claims)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Works", len(works))
    c2.metric("Claims (after consolidation)", len(claims))
    c3.metric("Flat-rate baseline / claim", f"{CSYM}{flat:,.0f}")
    c4.metric("Pool", f"{CSYM}{pool:,.0f}")

    df_rows = pd.DataFrame(rows)
    eng_rows = df_rows[df_rows["notes"] != ""]
    if not eng_rows.empty:
        st.subheader("Engineered / flagged cases")
        st.dataframe(eng_rows[["rightsholder", "n_works", "uniqueness", "market",
                               "share_pct", "libra_usd", "flat_usd", "delta_usd", "notes"]],
                     use_container_width=True)

    st.subheader("Libra vs flat-rate — top 15 claims")
    chart_df = df_rows.head(15).set_index("rightsholder")[["libra_usd", "flat_usd"]]
    st.bar_chart(chart_df)

    st.subheader("Full allocation schedule")
    st.caption(f"Monetary columns denominated in {currency}. Column keys retain the engine's internal *_usd naming for stability; values are {currency}.")
    st.dataframe(df_rows.drop(columns=["works"]), use_container_width=True, height=380)

    st.header("3 · Sensitivity analysis (Standard §5, mandatory)")
    with st.spinner("Re-running allocation under perturbed weights, shingle size, and floor…"):
        sens = engine.sensitivity(works)
    st.dataframe(pd.DataFrame(sens["scenarios"]), use_container_width=True)
    st.success(f"Minimum rank stability (Spearman): **{sens['min_spearman']}** · "
               f"max share swing **{sens['max_swing_pct_points']:.2f}** percentage points — "
               "disclosed, not hidden.")

    st.header("4 · Download the dossier")
    md = report_markdown(rows, sens, cfg, pool, engine.shingle_k, synthetic_metadata=synthetic, currency=currency)
    d1, d2, d3 = st.columns(3)
    d1.download_button("📄 Allocation report (Markdown)", md, "libra_allocation_report.md")
    d2.download_button("🗂 Schedule (CSV)", rows_to_csv(rows), "libra_allocation_schedule.csv")
    d3.download_button("🧾 Machine-readable (JSON)", full_json(rows, sens, cfg, pool, currency),
                       "libra_allocation_report.json")

    with st.expander("Statement of limits (Standard §2)"):
        st.markdown(
            "This allocation operates on a **known corpus** (works list). It asserts relative "
            "contribution within that corpus; it does **not** assert what any black-box model was "
            "trained on. Similarity is treated as evidence of presence and weight, never causation."
        )
else:
    st.info("Load the demonstration corpus or upload a works list to run an allocation.")

st.divider()
st.caption(f"Libra Attribution Standard v{SPEC_VERSION} · Engine v{ENGINE_VERSION} · "
           "Methodology: Aswin Krishna · © 2026 Aswin Krishna · Spec open, infrastructure owned. Not legal advice.")
