# DBA 720 Comprehensive Exam Prep Lab

Excel practice for the computational portion of the DBA 720 comprehensive examination.

## Version 3.0 — what changed

Version 2.0 contained five survey-research datasets, all drilling the same exercise: identify variables,
export to Excel, run a multiple regression, interpret. That is one quadrant of the Excel work the
instructor's exam-preparation note describes, and it omitted the one topic he named by name — derivatives.

Version 3.0 adds the missing coverage and consolidates the survey material into a single, better module.

### Files

| File | Covers |
|---|---|
| `index.html` | Module index, grouped by type, derivatives first. |
| `lab.css` | Shared stylesheet. |
| `lab.js` | Shared helpers: Excel-equivalent statistics, tolerance-based grading, table rendering, CSV export. |
| `DBA720_Deriv1_Futures.html` | Marking to market, margin calls, variation margin, minimum-variance hedge ratio, optimal contract count, basis risk. Hull Ch. 1–6. |
| `DBA720_Deriv2_Options.html` | Black–Scholes in Excel, delta/gamma/vega, two-step CRR binomial tree, put–call parity as an arbitrage check. Hull Ch. 8–13 and DerivaGem. |
| `DBA720_Quant1_MarketModel.html` | Regression of returns on an index: alpha, beta, R². Mean, variance, SD, skewness, excess kurtosis. Beta verified three ways including Cov/Var. |
| `DBA720_Quant2_Portfolio.html` | Covariance and correlation matrices, equally weighted portfolio variance via MMULT, diversification benefit, Sharpe ratio, two-asset minimum-variance weight. |
| `DBA720_Quant3_EventStudy.html` | Estimation versus event window, expected returns from the market model, abnormal returns, CAR, t-statistic. |
| `DBA720_Quant4_MonteCarlo.html` | GBM simulation of terminal prices, valuation by simulation, standard error and the √n rule, validation against Black–Scholes. |
| `DBA720_Dataset1.html` | Variable identification, multiple regression in Excel, VIF diagnostics, interpretation. Rebuilt — see below. |

### Dataset 1 was rebuilt

The original data had predictor intercorrelations of 0.71–0.91, variance inflation factors near 9, and
R² = 0.976. Under collinearity that severe the individual coefficients are unstable, so the graded
"strongest predictor" question had no well-defined answer.

The data has been regenerated with near-orthogonal predictors (VIFs 1.01–1.24), and a third phase now asks
the student to compute the VIFs and decide whether ranking the predictors is defensible at all. Recognising
when a question *cannot* be answered from the data is the judgement the examination is testing, and a
regression output does not announce it.

### Datasets 2–5 were retired

They ran the same exercise as one another and as Dataset 1, on the same kind of Likert perception data, and
added no coverage the rebuilt Dataset 1 does not provide. They are not referenced anywhere in v3.0.

They remain in the repository's git history and can be recovered at any time — deleting a file in git does
not destroy it. GitHub keeps every version, reachable through the repository's commit history.

### The `data/` folder

The five CSVs under `data/` were parallel copies of data already embedded in the page JavaScript; no page
ever read them. `Dataset1.csv` holds the superseded multicollinear data. The folder is unused by v3.0 and
can be deleted.

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

Upload all eleven files to the repository root and commit. No build step, no dependencies, no external
requests — GitHub Pages serves it as-is.

```
index.html
lab.css
lab.js
DBA720_Dataset1.html
DBA720_Deriv1_Futures.html
DBA720_Deriv2_Options.html
DBA720_Quant1_MarketModel.html
DBA720_Quant2_Portfolio.html
DBA720_Quant3_EventStudy.html
DBA720_Quant4_MonteCarlo.html
README.md
```

## Answer keys

Every figure in every module was computed with the Excel-equivalent estimator — `VAR.S`, `COVARIANCE.S`,
`SKEW`, `KURT`, `SLOPE`, `INTERCEPT`, `STEYX` — so Excel results match the keys rather than approximating
them. The generating script is `genkeys.py`; `keys.json` holds the computed values. Neither is needed by the
site; keep them if you want to regenerate or extend the data.

## Still not covered

**The essays.** This lab is the computational half only. The reading list is the primary preparation
resource for the rest, per the instructor's note.

**Whether any of this is examined.** The exam note summarised preparation for the Summer 2025 *course
final*. If the comprehensive examination is a pure essay instrument set at program level, the derivatives
and Excel work here is not required. Worth confirming before spending hours on DerivaGem.
