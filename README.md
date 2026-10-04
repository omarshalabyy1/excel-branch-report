<p align="center">
  <img width="100%" src="docs/header.svg" alt="Branch Excel report: every branch file, one clean table. 192 branch files, 10,089 rows read, 253 errors caught, one click to rebuild.">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10">
  <img src="https://img.shields.io/badge/pandas-2-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="pandas 2">
  <img src="https://img.shields.io/badge/Excel-openpyxl-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white" alt="Excel with openpyxl">
  <img src="https://img.shields.io/badge/Power_BI-Report-F2C811?style=for-the-badge&logo=powerbi&logoColor=black" alt="Power BI report">
</p>

<h3 align="center">192 branch Excel files merged into one weekly report in one click:<br>10,089 rows read, 253 errors caught and set aside with the reason.</h3>

## The problem

Every branch sends its own monthly Excel file in its own format. One puts a title block on top and a totals row at the bottom. One names its columns differently and types dates as text. One sends amounts as "$1,234.50" and categories in capitals. One writes "3 pcs" and "2nd class". So each week someone opens every file, copies, fixes and pastes before anyone sees a total, and the mistakes inside the files (a missing order ID, a date from next month, a line pasted twice) slip into the numbers without anyone noticing.

## The solution

<p align="center">
  <img width="100%" src="docs/how-it-works.svg" alt="How it works: 01 Collect, every branch's monthly Excel file in one folder; 02 Clean, headers, dates, amounts and spellings to one standard; 03 Check, five rules and duplicates, bad rows set aside with the reason; 04 Merge, one clean table across all branches and months; 05 Report, weekly Excel and Power BI report rebuilt in one click.">
</p>

<p align="center">
  <img width="100%" src="docs/mental-model.svg" alt="The mental model: four branches each send 48 monthly files in their own template. They pour into a funnel that cleans them to one standard and checks five rules plus duplicates. Out come one clean table of 9,836 rows and a set-aside list of 253 rows, each with its reason.">
</p>

One script, [`run.py`](run.py), does the week's work:

1. **Collect:** reads every file in `data/branches/`, finds the header row wherever it sits, and skips the title rows and the totals row.
2. **Clean:** maps every branch's headers to one set of names (one dictionary), reads each branch's own date format, turns "$1,234.50" and "3 pcs" into numbers, and fixes capitals, extra spaces and ship-mode spellings.
3. **Check:** five rules (missing order ID, date not readable, date outside the file's month, quantity missing or not above zero, amount not a number), then duplicates. A row that fails is set aside with its reason, its file and Excel row number, and its values exactly as the branch sent them, so it can be fixed at the source.
4. **Merge:** one clean table across all branches and months.
5. **Report:** `output/weekly_report.xlsx` (Summary, Weekly sales, Set aside, Clean data sheets) and three CSV files that the Power BI report refreshes from.

## The result

| | |
|---|---|
| Branch files merged | 192 (4 branches, 48 months each) |
| Rows read | 10,089 |
| Clean rows | 9,836 |
| Errors caught | 253: 157 rows that break a rule and 96 lines pasted twice (2.5% of rows) |
| Report rebuilt in | under a minute, with one command |

- **Nothing is dropped silently:** 10,089 rows read = 9,836 clean + 253 set aside. The 48 totals rows are layout, not orders, and are counted apart.
- **Tested against a known answer:** the mistakes were planted on purpose and listed in [`data/planted_errors.csv`](data/planted_errors.csv). All 253 were caught at the right file, row and reason, and nothing else was set aside. Every clean row matches its source line exactly.
- **It found a real problem too:** 225 order lines (47 products) in the source carry hidden non-breaking spaces in the product name, the kind that makes a VLOOKUP fail. The cleaner turns them into normal spaces.

![253 rows set aside, each with its reason](docs/errors-by-reason.png)

![Where each kind of mistake comes from, by branch](docs/errors-by-branch.png)

![Weekly sales, all branches, from the one clean table](docs/weekly-sales.png)

Every number here comes from [`analysis/analysis.ipynb`](analysis/analysis.ipynb), which runs the pipeline, checks the result three ways (planted mistakes, source lines, SQL) and draws the charts.

## Power BI report

[`powerbi/`](powerbi/) builds a two-page report in Power BI Desktop step by step, ready to copy and paste: the Power Query code, the model, 14 DAX measures, every visual with its fields, the theme, and the numbers each page must show.

- **Weekly report:** sales, profit, margin, orders and average order value; weekly sales by branch; monthly sales by branch; sales and profit by category.
- **Data quality:** files, rows read, clean rows, errors caught and error rate; rows set aside by reason and by branch; the list of rows to fix at the source.

## Run it

```bash
pip install -r requirements.txt
python run.py
```

On Windows you can double-click `run.bat` instead. Then open `analysis/analysis.ipynb` and run all cells to recompute every number and chart. The branch files are already in the repo; `python make_branch_files.py` makes them again from the source.

```
run.py                   the one click: read, clean, check, merge, report
run.bat                  the same, as a double-click on Windows
make_branch_files.py     makes the 192 branch files and plants the mistakes
data/branches/           the branch files run.py reads
data/planted_errors.csv  every mistake planted on purpose: the test's answer key
data/source/             the orders the branch files were made from
output/                  clean_sales.csv, set_aside_rows.csv, file_log.csv, weekly_report.xlsx
analysis/analysis.ipynb  every number in this README, with the checks
powerbi/                 the Power BI report, step by step
docs/                    the diagrams and charts in this README
```

## Data

Tableau's Sample Superstore orders: 9,994 US order lines from 2016 to 2019, in `data/source/`. `make_branch_files.py` splits them into one file per region (West, East, Central, South) and month, gives each region its own template, and plants mistakes on purpose with a fixed random seed. One line that the source repeats exactly was removed first, so the only duplicates are the planted ones.

---

Built by [Omar Shalaby](https://github.com/omarshalabyy1) · Python, pandas, Excel, Power BI
