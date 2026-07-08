# Libra — Launch & Verification Guide (Zero Coding Knowledge Required)

Follow this top to bottom. Every command is type-exactly-this-and-press-Enter. At each stage you're told precisely what you should see — if you see it, that stage of the software is **proven working on your machine**.

---

## Part 0 · Your folder

Put ALL downloaded files in **one folder** (e.g., `Libra`). The ones that matter for running:

| File | Role |
|---|---|
| `app.py` | The web application |
| `libra_engine.py` | The engine (the brain) |
| `test_libra.py` | The 41-test automated suite |
| `benchmark.py` | The validation benchmark (optional locally) |
| `requirements.txt` | Dependency list |
| `sample_works.csv`, `sample_dirty.csv`, `sample_bad.csv` | Your test ammunition for Part 6 |

Everything else (.md documents, demo outputs) is documentation — needed for reading, not for running.

## Part 1 · Install Python (one time, ~5 minutes)

**Windows:** go to python.org → Downloads → install the latest Python 3. On the FIRST installer screen, **tick the checkbox "Add python.exe to PATH"** — this is the single most important click in this guide. Then Install.
**Mac:** open the Terminal app and type `python3 --version`. If you see a version number ≥ 3.10, you're done. If not, install from python.org.

**Verify:** open a fresh terminal (Part 2) and type `python --version` (Windows) or `python3 --version` (Mac). A version number = success.
*(Mac users: wherever this guide says `python`, type `python3`.)*

## Part 2 · Open a terminal INSIDE your Libra folder

**Windows:** open the Libra folder in File Explorer → click in the **address bar** at the top → type `cmd` → press Enter. A black window opens, already pointed at your folder.
**Mac:** Finder → right-click the Libra folder → Services → "New Terminal at Folder". (Or open Terminal, type `cd `, drag the folder onto the window, press Enter.)

**Verify:** type `dir` (Windows) or `ls` (Mac). You should see your file names listed, including `app.py`.

## Part 3 · Install the dependencies (one time, ~2 minutes)

```
python -m pip install streamlit pandas pytest
```
Lots of text will scroll. Look for `Successfully installed …` near the end. Warnings in yellow are fine; only red `ERROR` lines matter (see Part 7).

## Part 4 · Run the automated test suite — the machine checks itself

```
python -m pytest test_libra.py -v -k "not Benchmark"
```

**Expected:** a list of test names each ending in `PASSED`, finishing with:
```
40 passed, 1 deselected
```
That single line proves: the mapping table, the shingle math, the share formulas, consolidation, edge cases, dirty-CSV hardening, and end-to-end behaviour — all correct **on your machine**.

**Optional — all 41:** the last test needs the real-books corpus. In your browser, download
`https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/gutenberg.zip`,
extract it, and place the resulting `gutenberg` folder (full of .txt books) inside your Libra folder. Then run `python -m pytest test_libra.py -v` → **41 passed**, and the validation benchmark itself has just re-proven its published error rates locally.

## Part 5 · Launch the app

```
python -m streamlit run app.py
```
First time, it may ask for an email — just press Enter to skip. Your browser opens at `http://localhost:8501` showing **⚖️ Libra Attribution Engine** with your name in the header.

To stop the app later: click the terminal window and press `Ctrl + C`.

## Part 6 · The manual checklist — with the exact numbers you should see

### 6A. Demonstration corpus
1. Click **Load demonstration corpus**.
2. Metrics row reads: **Works 28 · Claims (after consolidation) 27**.
3. Engineered-cases table: **RH-005** with 2 works and **uniqueness 1.00** (consolidation protecting the editions claimant); **RH-DERIV** and **RH-ANTH** with uniqueness well below 1 and negative Δ.
4. Bar chart shows Libra vs flat side by side.
5. Sensitivity table: **6 scenarios**, Spearman values ≈ 0.98.
6. Download all three dossier buttons; open the Markdown report — it must contain the disclosure table, the mapping table, the validation-status line citing **Benchmark v1 (MAE 0.0005)**, and the Statement of limits.

### 6B. Upload `sample_works.csv` (clean data)
Go to the **Upload works list** tab, upload the file, set pool to **100000**. Expected schedule (rounded):

| Rightsholder | Uniqueness | Libra USD | Δ vs flat |
|---|---|---|---|
| RH-VOSS | 1.00 | $30,918 | +10,918 |
| RH-COLE | 1.00 | $26,132 | +6,132 |
| RH-CHEN | 1.00 | $17,489 | −2,511 |
| RH-RAO | 0.41 | $14,940 | −5,060 |
| RH-PILLAI | 0.41 | $10,520 | −9,480 |

**Why RH-RAO is 0.41, not 1.00 — read this, it's the teaching moment:** Rao has two identical editions; consolidation handled that perfectly (6 works → **5 claims**, no double-counted volume). But the sample also contains Pillai, a *different* rightsholder who copied 60% of Rao's text. Cross-claimant overlap triggers the redundancy discount **symmetrically** — both drop to ≈0.41 — which is exactly the documented v1 limitation (v2's provenance-priority factor will protect Rao as the senior work). Your sample data demonstrates the system's main protection *and* its honestly-disclosed limit in one screen.

### 6C. Upload `sample_dirty.csv` (sabotaged metadata)
Same six works, but with `TRUE`/`FALSE` as text, stray spaces, the word `nonsense` as a boolean, and a **blank pub_year** (the bug that used to crash the app). Expected: **no crash**, and the allocation table shows the *same numbers as 6B*. That equality is the proof the hardened parsing works.

### 6D. Upload `sample_bad.csv` (missing column)
Expected: a friendly red error — `Missing required columns: ['text']` — and no crash.

### 6E. Controls
Move the **volume-weight slider**: allocations shift live; market weight always shows 1 − volume. Move the **floor slider** to 0.30: small claims grow, big claims shrink, totals still equal the pool.

**If 6A–6E all match: the software is verified working, end to end, by your own hands.**

## Part 7 · Troubleshooting

| Symptom | Fix |
|---|---|
| `'python' is not recognized` | Python wasn't added to PATH. Re-run the installer → "Modify" → tick "Add to PATH". Or try `py` instead of `python`. |
| `'streamlit' is not recognized` | Always use the long form given here: `python -m streamlit run app.py`. |
| `No module named streamlit` | Re-run Part 3 in the same terminal. |
| Browser doesn't open | Open it yourself and go to `http://localhost:8501`. |
| `Port 8501 is already in use` | An old copy is running. Close other terminals, or run `python -m streamlit run app.py --server.port 8502`. |
| Tests can't find `gutenberg` | Only affects the optional 41st test — the folder must be named exactly `gutenberg` and sit beside `test_libra.py`. |
| Anything else | Copy the LAST 10 lines of the terminal text and paste them to me — that's the error message, and I'll fix it. |

## Part 8 · After it works

Deploying the public URL is these same files pushed to GitHub + share.streamlit.io (README has the clicks). The terminal skills you just used — open folder, `pip install`, `python -m …` — are the only ones the whole project ever needs from you.
