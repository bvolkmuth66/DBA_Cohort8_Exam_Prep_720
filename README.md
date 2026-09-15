# DBA 720 Comprehensive Exam Prep Lab

Excel practice for the computational portion of the DBA 720 comprehensive examination.

## Version 3.0 — what changed

Version 2.0 contained five survey-research datasets, all drilling the same exercise: identify variables,
export to Excel, run a multiple regression, interpret. That is one quadrant of the Excel work the
instructor's exam-preparation note describes, and it omitted the one topic he named by name.

### Added

| File | Covers |
|---|---|
| `DBA720_Deriv1_Futures.html` | Marking to market, margin calls, variation margin, minimum-variance hedge ratio, optimal contract count, basis risk. Hull Ch. 1–6. |
| `DBA720_Deriv2_Options.html` | Black–Scholes in Excel, delta/gamma/vega, two-step CRR binomial tree, put–call parity as an arbitrage check. Hull Ch. 8–13 and DerivaGem. |
| `DBA720_Quant1_MarketModel.html` | Regression of returns on an index: alpha, beta, R². Mean, variance, SD, skewness, excess kurtosis. Beta verified three ways including Cov/Var. |
| `DBA720_Quant2_Portfolio.html` | Covariance and correlation matrices, equally weighted portfolio variance via MMULT, diversification benefit, Sharpe ratio, two-asset minimum-variance weight. |
| `DBA720_Quant3_EventStudy.html` | Estimation versus event window, expected returns from the market model, abnormal returns, CAR, t-statistic. |
| `DBA720_Quant4_MonteCarlo.html` | GBM simulation of terminal prices, valuation by simulation, standard error and the √n rule, validation against Black–Scholes. |
| `lab.css` | Shared stylesheet. |
| `lab.js` | Shared helpers: Excel-equivalent statistics, tolerance-based grading, table rendering, CSV export. |

### Revised

**`DBA720_Dataset1.html`** — the original data had predictor intercorrelations of 0.71–0.91, VIFs near 9,
and R² = 0.976. Under collinearity that severe the individual coefficients are unstable, so the graded
"strongest predictor" question had no well-defined answer. The data has been regenerated with
near-orthogonal predictors (VIFs 1.01–1.24), and a third phase now asks the student to compute the VIFs
and decide whether ranking the predictors is defensible at all.

**`index.html`** — rewritten. Modules are grouped by type, with derivatives first and flagged as priority.

### Unchanged

Datasets 2 through 5 are untouched and still work. They carry their own inline styles, so they look
slightly different from the new modules until migrated to `lab.css`. Migrating them is straightforward:
delete the inline `<style>` block, add `<link rel="stylesheet" href="lab.css">`, and replace the bespoke
grading functions with `Lab.gradeItems` / `Lab.report`.

## Design changes in v3.0

**Tolerance-based grading.** v2.0 compared entered values for exact equality, so a correct answer rounded
differently was marked wrong. `Lab.gradeItems` grades within a per-item tolerance and reports the expected
value on a miss.

**Per-item feedback.** Results show which specific entries were wrong and what was expected, rather than a
bare percentage.

**Model responses.** Every module ends with interpretation questions and a reveal-on-demand model response
that connects the computation back to the course readings. The exam pairs numbers with interpretation —
Assignment 5 asked "which trader does better?" alongside the arithmetic — so the lab does too.

**Excel traps flagged.** The Data Analysis ToolPak's Covariance tool returns *population* covariance while
`COVARIANCE.S` returns sample covariance; `KURT` returns *excess* kurtosis; `RAND()` is volatile. Each is
called out where it bites.

## Installing

Drop every file into the repository root alongside the existing `DBA720_Dataset*.html` files and commit.
No build step, no dependencies, no external requests — GitHub Pages serves it as-is.

```
index.html
lab.css
lab.js
DBA720_Dataset1.html          (replaces existing)
DBA720_Deriv1_Futures.html
DBA720_Deriv2_Options.html
DBA720_Quant1_MarketModel.html
DBA720_Quant2_Portfolio.html
DBA720_Quant3_EventStudy.html
DBA720_Quant4_MonteCarlo.html
```

## Answer keys

Every figure in every module was computed with the Excel-equivalent estimator — `VAR.S`, `COVARIANCE.S`,
`SKEW`, `KURT`, `SLOPE`, `INTERCEPT`, `STEYX` — so Excel results match the keys rather than approximating
them. The generating script is `genkeys.py`; `keys.json` holds the computed values.

## Still not covered

**The essays.** This lab is the computational half only. The reading list is the primary preparation
resource for the rest, per the instructor's note.

**Whether any of this is examined.** The exam note summarised preparation for the Summer 2025 *course
final*. If the comprehensive examination is a pure essay instrument set at program level, the derivatives
and Excel work here is not required. Worth confirming before spending hours on DerivaGem.
