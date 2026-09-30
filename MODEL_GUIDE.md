# Ultimate methodology and controls

All financial values are USD millions. The title and three revenue windows are fictional.

## Definitions

- **Historical revenue:** recognized before the modeled current period.
- **Current revenue:** recognized in the modeled current period, held fixed across outlook revisions.
- **Future revenue:** forecast after the current period, by window.
- **Lifetime revenue:** historical + current + future.
- **Available cost:** opening unamortized cost + current capitalized additions.
- **Historical production cost:** total production cost capitalized before current additions, including amounts already amortized. It is deliberately different from the opening carrying value.
- **Historical other cost:** previously incurred exploitation and participation costs, included once in lifetime economics.

## Sequence and formulas

1. Remaining revenue = current + future revenue. Future sales haircuts apply only to future windows.
2. Net remaining proceeds screen = max(0, remaining revenue × (1 − participation rate) − current exploitation − future exploitation).
3. Illustrative write-down = max(0, available cost − screened proceeds).
4. Prospective amortization = (available cost − illustrative write-down) × current revenue / remaining revenue. With no remaining revenue the ratio is zero and the screen writes off available cost.
5. Closing asset = available cost − screen write-down − amortization.
6. Current contribution = current revenue × (1 − participation rate) − current exploitation − amortization − screen write-down.
7. Lifetime contribution = lifetime revenue − historical production cost − current additions − historical other cost − current/future exploitation − current/future participation.

Historical other cost already includes historical participation, so the model does not apply the participation rate again to historical revenue. The participation percentage is a simplified economic charge, not a reproduction of Sony's liability accrual policy or a talent contract.

The amortization step uses **remaining carrying cost and current-plus-future revenue**, rather than original production cost divided by revised lifetime revenue. It illustrates prospective revision mechanics; it does not certify a required IFRS journal entry. The recovery screen is undiscounted and applied before amortization. A proper accounting assessment can require discounted cash flows, fair value less disposal costs, unit-of-account / CGU analysis and other policy-specific inputs absent here.

## Workbook map

Inputs D5 selects one active case. D8/D9 contain downside/stress haircuts. D12:D20 contain costs, actual revenues and the rate. D24:E26 hold prior and revised future-window estimates; F24:F26 links the active case into a single calculation on **Ultimate**. Sensitivity rows are an explicitly labeled sweep against the revised future estimate, independent of the case selector.

**Ultimate D23** reconciles the asset; **Inputs D38 / Ultimate D25** flag missing numerical fields or an invalid case. They are terminal checks and do not feed the financial math. A missing required input must be fixed before interpreting outputs. Cells are editable and not access-controlled; Python also validates nonnegative inputs and unique window names.

## Review design

| Control | Risk | Evidence |
|---|---|---|
| Actuals remain fixed across scenarios | Rewriting history | Mutation test and separated assumptions |
| Unique windows and valid cost basis | Double count or invalid asset | Input validation |
| Asset roll-forward in 101 stress points | Over-amortization / negative carrying cost | Python tests |
| Zero current/future revenue boundary | Divide-by-zero or stranded asset | Python tests |
| Model result vs independent workbook | Formula-reference error | Workbook validation record |

Reviewers should record source, owner, effective date, approval status and rationale for every changed window. No live ERP integration, transaction-level evidence, contract-specific participation model, financial-statement audit or SOX attestation is included.
