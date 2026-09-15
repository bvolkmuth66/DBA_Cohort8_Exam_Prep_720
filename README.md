# DBA 720 Comprehensive Exam Prep Lab

Excel practice for the computational portion of the DBA 720 comprehensive examination.

## How this lab is weighted

The instructor's exam-preparation note contains two instructions about Excel, and they are not equally strong:

> We did use Excel in class for derivatives, so you **may want to** review that material and DerivaGem
> spreadsheet.
>
> **Please also review** how to perform regression analysis in Excel, along with basic statistical functions
> such as mean, variance, covariance, correlation, etc **that you learned in your statistics course**.

One is a suggestion, the other a directive — and "that you learned in your statistics course" frames the
statistics as elementary prior knowledge being refreshed, not new machinery being acquired.

The expected exam task is therefore a **supplied dataset and a narrative**, with descriptive statistics,
correlation and regression run in Excel and interpreted in writing. Not formulas reconstructed from memory.
The modules are ordered and scoped to match.

## Modules

| File | Covers |
|---|---|
| `DBA720_Exam_FullAnalysis.html` | **Start here.** A narrative, 48 months of fund and market returns, and no instruction about what to compute. You choose the analyses, run them, and write a board recommendation. |
| `DBA720_Quant1_MarketModel.html` | Mean, variance, SD, skewness, excess kurtosis, covariance, correlation, and a regression of returns on an index. Beta verified three ways including Cov/Var. |
| `DBA720_Dataset1.html` | Variable identification, multiple regression in Excel, VIF diagnostics, interpretation. |
| `DBA720_Quant2_Portfolio.html` | Covariance and correlation matrices, portfolio variance, diversification benefit, Sharpe ratio, two-asset minimum-variance weight. |
| `DBA720_Quant3_EventStudy.html` | A narrative plus returns: regression on an estimation window, expected versus actual, abnormal returns, CAR, t-statistic. |
| `DBA720_Deriv1_Futures.html` | Minimum-variance hedge ratio — a Cov/Var calculation on supplied data — plus margin and marking to market. |
| `DBA720_Deriv2_Options.html` | Driving DerivaGem, reading its output, checking the result against put–call parity. |
| `index.html`, `lab.css`, `lab.js` | Index page, shared stylesheet, shared helper library. |

## Changes in 3.1

**Monte Carlo was cut.** No reading was assigned for Week 11 and the exam note does not mention simulation.
Asking for drift terms and diffusion coefficients was formula work the evidence does not support.

**The options module was rewritten as tool use.** It previously had students build Black–Scholes from d₁ and
d₂ in a spreadsheet. It now has them drive DerivaGem, read the values and Greeks it reports, switch to a
binomial tree to see convergence, and verify with put–call parity. The instructor pointed at a tool, not at a
derivation.

**The futures module leads with the hedge ratio.** The minimum-variance hedge ratio is
`COVARIANCE.S / VAR.S` on supplied data — the same estimator as beta, and squarely inside "basic statistical
functions." Margin arithmetic is now the second problem rather than the first.

**A full-analysis module was added**, in the predicted exam format. Its first phase asks which analyses the
question calls for, before any are named, because choosing them is the skill an open prompt tests. The dataset
is built so the naive answer is wrong: one fund has the higher mean return, the other has the better Sharpe
ratio, a positive alpha, and nothing resembling the first fund's −40% month, skewness of −2.9 and excess
kurtosis of 14.

## Changes in 3.0

**Dataset 1 was rebuilt.** The original data had predictor intercorrelations of 0.71–0.91, VIFs near 9, and
R² = 0.976. Under collinearity that severe the coefficients are unstable, so the graded "strongest predictor"
question had no well-defined answer. The data was regenerated with near-orthogonal predictors (VIFs
1.01–1.24), and a third phase now asks the student to compute the VIFs and decide whether ranking the
predictors is defensible at all.

**Datasets 2–5 were retired.** They ran the same exercise as one another and as Dataset 1, on the same kind of
Likert data, and added no coverage the rebuilt Dataset 1 does not provide. They remain in the repository's git
history and can be recovered at any time.

**The `data/` folder is unused.** Those five CSVs were parallel copies of data already embedded in the page
JavaScript; no page ever read them, and `Dataset1.csv` holds the superseded data. Safe to delete.

**Tolerance-based grading with per-item feedback.** v2.0 compared entered values for exact equality, so a
correct answer rounded differently was marked wrong. Results now show which entries were wrong and what was
expected.

**Model responses.** Every module ends with interpretation questions and a reveal-on-demand model response
connecting the computation back to the course readings.

**Excel traps flagged.** The Data Analysis ToolPak's Covariance tool returns *population* covariance while
`COVARIANCE.S` returns sample covariance; `KURT` returns *excess* kurtosis. Each is called out where it bites.

## Installing

Upload all ten files to the repository root and commit. No build step, no dependencies, no external requests.

```
index.html
lab.css
lab.js
DBA720_Exam_FullAnalysis.html
DBA720_Quant1_MarketModel.html
DBA720_Dataset1.html
DBA720_Quant2_Portfolio.html
DBA720_Quant3_EventStudy.html
DBA720_Deriv1_Futures.html
DBA720_Deriv2_Options.html
README.md
```

## Answer keys

Every figure was computed with the Excel-equivalent estimator — `VAR.S`, `COVARIANCE.S`, `SKEW`, `KURT`,
`SLOPE`, `INTERCEPT`, `STEYX` — so Excel results match the keys rather than approximating them. The generating
script is `genkeys.py` and `keys.json` holds the values. Neither is needed by the site.

## Still not covered

**The essays.** This lab is the computational half only. The reading list is the primary preparation resource
for the rest, per the instructor's note.

**Whether any of this is examined.** The exam note summarised preparation for the Summer 2025 *course final*.
If the comprehensive examination is a pure essay instrument set at program level, none of the Excel work here
is required. Worth confirming.
