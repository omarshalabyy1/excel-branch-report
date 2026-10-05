# 6. Checks: the numbers the report must show

These are the demo run's numbers (amounts in USD). For a client, copy the numbers from their notebook run.

Every number below comes from `analysis/analysis.ipynb` and is counted a second time with plain SQL in the notebook ("Check 3"). Check with no slicer selected unless a row says otherwise. If a card is off, the usual causes are a missing relationship, a wrong column type in Power Query, or a filter left on a slicer.

## Page 1: Weekly report (all years, all branches)

| Card or total | Must show |
|---|---|
| Sales | 2,265,770 (exact: 2,265,769.78) |
| Profit | 282,653 (exact: 282,653.43) |
| Profit Margin % | 12.5% |
| Orders | 4,971 |
| Average Order Value | 455.80 |
| Order Lines (not on a card) | 9,836 |

**Sales by branch** (visual 10; click a branch and the cards must change to its row):

| Branch | Sales | Profit | Margin | Orders |
|---|---|---|---|---|
| West | 714,519.07 | 107,342.94 | 15.0% | 1,600 |
| East | 666,739.35 | 90,362.30 | 13.6% | 1,391 |
| Central | 496,613.97 | 39,073.61 | 7.9% | 1,169 |
| South | 387,897.39 | 45,874.58 | 11.8% | 811 |

**By year** (pick one year in the Year slicer):

| Year | Sales | Profit | Orders |
|---|---|---|---|
| 2016 | 479,525.73 | 49,522.56 | 964 |
| 2017 | 458,825.00 | 60,373.85 | 1,027 |
| 2018 | 601,889.95 | 80,337.91 | 1,306 |
| 2019 | 725,529.10 | 92,419.11 | 1,674 |

**By category** (visual 12):

| Category | Sales | Profit | Margin |
|---|---|---|---|
| Technology | 831,236.01 | 144,984.03 | 17.4% |
| Furniture | 724,968.37 | 17,082.68 | 2.4% |
| Office Supplies | 709,565.40 | 120,586.72 | 17.0% |

**Weekly line** (visual 9): the last three weeks in the data start on Monday 2019-12-16 (18,185.02), 2019-12-23 (16,408.68) and 2019-12-30 (713.79, a one-day week).

## Page 2: Data quality (all branches)

| Card | Must show |
|---|---|
| Branch Files | 192 |
| Rows Read | 10,089 |
| Clean Rows | 9,836 |
| Errors caught (Rows Set Aside) | 253 |
| Error Rate % | 2.5% |

Rows Read = Clean Rows + Rows Set Aside: 10,089 = 9,836 + 253. Set aside = 157 rule breaks + 96 duplicate lines. The 48 totals rows at the bottom of the West files are layout, not errors, and are counted apart (`[Totals Rows Skipped]`).

**Rows set aside by reason** (visual 8):

| Reason | Rows |
|---|---|
| duplicate of an earlier row | 96 |
| amount not a number | 37 |
| date not readable | 31 |
| date outside the file's month | 30 |
| quantity missing or below 1 | 30 |
| missing order id | 29 |

**Reasons by branch** (visual 9, column totals) and the cards with one branch selected:

| Branch | Files | Rows Read | Clean Rows | Set Aside | Error Rate % |
|---|---|---|---|---|---|
| Central | 48 | 2,347 | 2,292 | 55 | 2.3% |
| East | 48 | 2,879 | 2,805 | 74 | 2.6% |
| South | 48 | 1,628 | 1,588 | 40 | 2.5% |
| West | 48 | 3,235 | 3,151 | 84 | 2.6% |

## The SQL used

The notebook loads the three files from `output/` into SQLite and runs:

```sql
SELECT (SELECT COUNT(*) FROM file_log)       AS files,
       (SELECT SUM(rows_read) FROM file_log) AS rows_read,
       (SELECT COUNT(*) FROM clean_sales)    AS clean_rows,
       (SELECT COUNT(*) FROM set_aside_rows) AS set_aside_rows;

SELECT branch,
       COUNT(*)                 AS order_lines,
       COUNT(DISTINCT order_id) AS orders,
       ROUND(SUM(sales), 2)     AS sales,
       ROUND(SUM(profit), 2)    AS profit
FROM clean_sales
GROUP BY branch
ORDER BY branch;
```
