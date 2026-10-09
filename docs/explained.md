# The project explained, from zero

This page explains the whole project in plain words: what it does, what every word means, where every number comes from, and how to talk about it in an interview. You do not need to know Python, Excel formulas or Power BI to read it.

[← Back to the README](../README.md)

## 1. The project in one minute

A retail chain has four branches: West, East, Central and South. Every month each branch sends head office an Excel file with its order lines. Each branch uses its own layout:

- West puts a title block on top and a TOTAL row at the bottom.
- East calls its columns "Order No", "Qty" and "Amount" and types dates as text, like 02/03/2019.
- Central writes amounts as text, like "$1,234.50", in CAPITALS, with double spaces in product names.
- South types dates as "Mar 05 2019", quantities as "3 pcs" and shipping as "Std" or "2nd class".

So every week someone opens all the files, copies, fixes and pastes before anyone sees a total. Mistakes inside the files (a missing order ID, a date from next month, a line pasted twice) slip into the numbers and nobody notices.

This project does that work with one command. It reads every file, cleans each value to one standard, checks every row against five rules and for duplicates, and merges the good rows into one clean table. Every bad row is set aside with the reason, so the branch can fix it. Then it writes a weekly Excel report and three CSV files that a Power BI report reads.

Think of it like a post room. Letters arrive from four offices, each in its own handwriting. A clerk copies each letter onto one standard form, checks five things on it, and puts it on the "done" pile. A letter that fails a check goes into a tray with a note saying what is wrong. At the end, every letter that came in is in exactly one place: the done pile or the tray.

## 2. Words you will meet

| Word | What it means here |
|---|---|
| **Branch** | One shop region of the chain: West, East, Central or South. |
| **Branch file** | One Excel file from one branch for one month, like `South_2019-03.xlsx`. There are 192: 4 branches × 48 months. |
| **Workbook, sheet** | An Excel file is a workbook. Inside it are sheets (tabs). The order lines are on the sheet named `Sales` in every file. |
| **Order, order line** | An order is one customer purchase, with one **order ID** like `CA-2019-121804`. An order line is one product on that order. One order can have several lines. |
| **Header row** | The row with the column names. West's header sits on Excel row 4, the others on row 1. `run.py` finds it by looking for the order ID column. |
| **Title rows, totals row** | Rows that are layout, not orders: West's "West branch - monthly sales" title on top and its TOTAL row at the bottom. They are skipped and only counted. |
| **Rows read** | The order lines under the header row of every file. Title and totals rows are not counted. |
| **Clean** | To bring every value to one standard: one set of column names, real dates, numbers instead of "$1,234.50" or "3 pcs", one spelling for each value. |
| **Rule** | A check every row must pass. There are five, see section 3. |
| **Set aside** | A row that breaks a rule, or is a duplicate, is not used in the totals. It goes to `output/set_aside_rows.csv` with its reason, its file, its Excel row number and its values exactly as the branch sent them. Nothing is deleted. |
| **Errors caught** | The number of rows set aside: rule breaks plus duplicates. |
| **Duplicate** | A line pasted twice. After cleaning, a row that is identical in all 13 columns to an earlier row of the same branch is set aside. The first copy stays. |
| **Merge** | To put the clean rows of all branches and all months into one table. |
| **Spelling map** | `data/input/value_map.csv`. A list of how a branch writes a value and its standard spelling, like `Std` → `Standard Class`. Capitals are fixed the same way. |
| **Date format** | The pattern a branch uses for text dates. East is `%d/%m/%Y` (day/month/year), South is `%b %d %Y` (Mar 05 2019). These are Python's date codes, set in `config/client.yaml`. |
| **Non-breaking space** | A character that looks like a normal space but is not one. It makes Excel's **VLOOKUP** (a formula that finds a value in another table) fail to match. |
| **Planted errors, answer key** | The mistakes put into the branch files on purpose, and `data/input/planted_errors.csv`, the list of where each one is. It lets the project prove it finds exactly those mistakes. |
| **CSV** | A plain text file of a table, one row per line, values separated by commas. The outputs `clean_sales.csv`, `set_aside_rows.csv` and `file_log.csv` are CSV. |
| **Python, pandas, openpyxl** | Python is a programming language. pandas is its library for tables. openpyxl lets pandas read and write Excel files. |
| **Script** | A file of code you run. `run.py` is the main script. `run.bat` runs it with a double-click on Windows. |
| **`config/client.yaml`** | The settings a client would change: file name pattern, sheet name, the header spellings of each column, the date formats, the quantity rule, colours. YAML is a simple text format for settings. |
| **Regular expression** | A pattern for text. `inputs.file_name` is one: it reads the branch and the month (`YYYY-MM`) out of each file name. |
| **Notebook** | `analysis/analysis.ipynb`, a file that mixes code, its output and notes. It runs the pipeline, checks the result and computes every number in the README. |
| **Pipeline** | The steps the data goes through, in order: collect, clean, check, merge, report. |
| **Layers** | The six stages every project of this kind is named by, in order. **Bronze layer**: rows as received (`read_branch_file()`). **Silver layer**: one standard (`clean()`). **Gold layer**: the rules (`check()`), which split the rows into `clean_sales.csv` and the set-aside rows. **Semantic layer**: the Power BI model, the star of `Sales`, `Branch` and `Date`. **Analytical layer**: totals and KPIs, the Summary and Weekly sales tables and the DAX measures. **Reporting layer**: the Excel workbook and the Power BI pages. |
| **SQL, SQLite** | SQL is the language used to ask a database questions. SQLite is a small database that lives in memory. The notebook loads the three CSV files into it to count everything a second way. |
| **Power BI** | Microsoft's tool for interactive reports and dashboards. |
| **Power Query, M code** | The part of Power BI that loads and shapes data before the report uses it. Its formulas are written in a language called M. |
| **DAX, measure** | DAX is the formula language of Power BI. A measure is a DAX calculation like "Sales" or "Error Rate %". |
| **Fact table** | The big table of events you add up. Here `Sales`: one row per clean order line. |
| **Dimension table** | A small lookup table you filter and group by. Here `Branch` (4 rows) and `Date` (one row per day). |
| **Grain** | What one row of a table stands for. The grain of `Sales` is "one clean order line". |
| **Primary key (PK), foreign key (FK)** | A primary key makes each row unique (`file` + `excel_row` in `Set Aside`). A foreign key points to a row in another table (`Sales[branch]` points to `Branch[branch]`). |
| **Date table** | A table with one row per day, with no gaps, so Power BI can group by week, month and year. |
| **Profit margin** | Profit as a share of sales. Profit 12 on sales 100 is a 12% margin. |
| **Average order value** | Sales divided by the number of orders. |
| **Error rate** | Rows set aside divided by rows read. |
| **Theme** | A Power BI file that sets the report's colours and fonts. `theme.py` writes it from `config/client.yaml`. |

## 3. How it works, file by file

Run in this order (the commands are in the README's "Run it" section):

| Step | File | What it does |
|---|---|---|
| 0 | `config/client.yaml`, `config.py` | Hold every setting. `config.py` is the only file that reads them, and stops with one line if a setting is missing. |
| 0 | `data/demo/make_branch_files.py` | Demo only, run once. Splits the source orders (see Data in the README) into one file per branch and month, gives each branch its own layout, and plants mistakes with a fixed random seed. The 192 files it made are committed, so you do not need to run it. |
| 1 | `run.py`: `read_branch_file()` | **Collect (Bronze layer).** For each file: reads the branch and month from the name, opens the `Sales` sheet, finds the header row, maps each header to its standard name, skips title and totals rows, and notes each row's Excel row number. A broken file (wrong name, no `Sales` sheet, a missing column) stops the run with one line before anything is written. |
| 2 | `run.py`: `clean()` | **Clean (Silver layer).** Trims spaces and double spaces, applies the spelling map, reads dates (a real Excel date as it is; a text date only with its branch's format, never guessed), turns "3 pcs" into 3 and "$1,234.50" into 1234.50. A value that cannot be read becomes empty. |
| 3 | `run.py`: `check()` | **Check (Gold layer).** Gives each row its reason, or none if it passes. The five rules, in this order: missing order id; date not readable; date outside the file's month; quantity missing or below 1; amount not a number. Then: a row that passed but is identical to an earlier row of the same branch is a "duplicate of an earlier row". |
| 4 | `run.py`: `main()` | **Merge (Gold layer).** Rows with no reason go into one clean table. Set-aside rows keep the values the branch sent. For every file it checks rows read = clean + set aside, and stops if not. |
| 5 | `run.py`: `write_report()` | **Report (Analytical and Reporting layers).** Writes `output/clean_sales.csv`, `output/set_aside_rows.csv`, `output/file_log.csv` (one row per file) and `output/weekly_report.xlsx` with four sheets: Summary, Weekly sales, Set aside, Clean data. Weeks run Monday to Sunday. The Summary and Weekly sales sheets are the Analytical layer; the workbook is the Reporting layer. |
| 6 | `theme.py` | Writes the Power BI theme `powerbi/05-theme.json` from the colours in `client.yaml`. |
| 7 | `analysis/analysis.ipynb` | Runs `run.py`, checks the result three ways (the answer key, the source lines, SQL), computes every number in the README and draws the three charts in `docs/`. |
| 8 | `powerbi/` | The Semantic layer (the model), the Analytical layer (the measures) and the Reporting layer (the pages). Step-by-step instructions to build the Power BI report from the three CSV files: queries, model, 14 measures, two pages, and the numbers each card must show (`06-checks.md`). |

The inputs, all in `data/input/`: the 192 branch files, `value_map.csv` (the spelling map) and `planted_errors.csv` (the demo's answer key, read only by the notebook).

### The rules, with an example

One real file, `South_2019-03.xlsx` (South branch, March 2019). South has no title block, so the header is Excel row 1. Excel row 2 holds this line, exactly as South sent it:

| Order ID | Order Date | Ship Mode | Segment | City | State | Product ID | Category | Sub-Category | Product Name | Quantity | Sales | Profit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CA-2019-121804 | Mar 03 2019 | Std | Consumer | Murray | Kentucky | OFF-AP-10004859 | Office Supplies | Appliances | Acco 6 Outlet Guardian Premium Surge Suppressor | 5 pcs | 72.8 | 19.66 |

1. **Collect.** The name `South_2019-03.xlsx` matches the file name pattern, so the branch is South and the month is 2019-03. The headers already have the standard names. The file has 28 order lines and no totals row.
2. **Clean.** "Mar 03 2019" is text, and South's format is `%b %d %Y`, so it becomes the date 3 March 2019. "Std" is in the spelling map, so it becomes "Standard Class". "5 pcs" becomes the number 5. 72.8 and 19.66 are already numbers.
3. **Check.** The order ID is there. The date is readable. Its month, 2019-03, is the file's month. The quantity 5 is at least 1. Sales and profit are numbers. It is not a copy of an earlier row. So the row has no reason: it is clean.
4. **Merge.** It lands in `output/clean_sales.csv` as `South, South_2019-03.xlsx, CA-2019-121804, 2019-03-03, Standard Class, …, 5, 72.8, 19.66`. The notebook's check 2 finds the same line in the source orders.

The same file shows a duplicate. Excel rows 7 and 8 are the same line pasted twice (order `CA-2019-155698`, a Belkin surge protector, "8 pcs", 647.84). Row 7 passes every rule and goes into the clean table. Row 8 is identical after cleaning, so it is set aside as "duplicate of an earlier row", with its values as sent: "Mar 08 2019", "1st class", "8 pcs". `planted_errors.csv` lists `South_2019-03.xlsx, 8, duplicate of an earlier row`, so the answer key agrees. In `file_log.csv` this file reads: 28 rows read = 27 clean + 1 set aside.

## 4. Every number, explained

The README's numbers are printed by the notebook ([`analysis/analysis.ipynb`](../analysis/analysis.ipynb)). The cell numbers below count from 0, the first cell. Cell 1 runs `run.py`, cell 2 counts the headline, cell 3 counts reasons by branch, cell 5 runs checks 1 and 2, cell 7 runs the SQL check, cell 9 counts the report totals, cells 11 to 13 draw the charts.

### The headline and the results table

| Number | What it means | How it is worked out | Where |
|---|---|---|---|
| **192 branch files** | Every Excel file in `data/input/`. | Count of rows in `file_log.csv`, one per file. 4 branches × 48 months = 192. | notebook cell 2 |
| **4 branches, 48 months each** | West, East, Central, South; January 2016 to December 2019. | Distinct branches and months in `file_log.csv`. 4 years × 12 = 48 months. | notebook cell 2 |
| **10,089 rows read** | Every order line in every file, good or bad. | Sum of `rows_read` over the 192 files. | notebook cells 1, 2 |
| **9,836 clean rows** | Rows that passed every rule and are not duplicates. | Count of rows in `clean_sales.csv`. | notebook cells 1, 2 |
| **253 errors caught** | Rows set aside, each with its reason. | Count of rows in `set_aside_rows.csv`. 10,089 − 9,836 = 253. | notebook cells 1, 2 |
| **157 rows that break a rule** | Rows with one of the five rule reasons. | 37 amount not a number + 31 date not readable + 30 date outside the file's month + 30 quantity missing or below 1 + 29 missing order id = 157. | notebook cells 1, 2 |
| **96 lines pasted twice** | Rows with the reason "duplicate of an earlier row". | Count of that reason. 157 + 96 = 253. | notebook cells 1, 2 |
| **2.5% of rows** | The error rate. | 253 / 10,089 = 2.5077%, shown to one decimal. | notebook cell 2 |
| **48 totals rows** | West's TOTAL rows, one per West file. Layout, not orders. | Sum of `totals_rows_skipped` in `file_log.csv`. All 48 are in West files. | notebook cell 2 |
| **Under a minute, one command** | How long `python run.py` takes to rebuild everything. | `run.py` timed itself at 13.0 seconds; the notebook's own clock said 14 seconds, because it also counts starting Python. The time depends on the computer, so the README gives a limit, not an exact number. | notebook cells 1, 2, 15 |
| **All 253 caught at the right file, row and reason** | The rows set aside are exactly the 253 rows in the answer key, and nothing else. | The notebook joins `set_aside_rows.csv` to `planted_errors.csv` on file and Excel row and asserts every row matches, with the same reason. | notebook cell 5 (check 1) |
| **Every clean row matches its source line** | Cleaning fixed the format and changed no value. | Each of the 9,836 clean rows is joined to the source orders on all 13 columns; every one finds a match. | notebook cell 5 (check 2) |
| **225 order lines (47 products)** | Lines whose product name in the source holds a hidden non-breaking space. | Count of source lines whose product name contains one (225), and the distinct product names among them (47). The cleaner turns them into normal spaces. | notebook cell 5 |
| **14 DAX measures, two pages** | The size of the Power BI report. | 6 measures for the weekly report page + 8 for the data quality page = 14. | `powerbi/03-measures.dax` |
| **9,994 order lines, 2016 to 2019** | The source orders before they were split into branch files (see Data in the README). | Rows in `data/demo/source_orders.csv`. | `data/demo/source_orders.csv` |
| **One line that the source repeats exactly** | One order line appears twice in the source. It was removed before the files were made, so the only duplicates are the planted ones. | `make_branch_files.py` drops exact repeats on the 13 columns; there is 1. | `data/demo/make_branch_files.py` |

### The charts in the README

| Chart | What the numbers are | Where |
|---|---|---|
| **errors-by-reason.png** | The six reasons and their row counts: 96, 37, 31, 30, 30, 29. They add up to 253. | notebook cell 11 (counts in cell 1) |
| **errors-by-branch.png** | Each reason split by branch. The branch totals are Central 55, East 74, South 40, West 84. The biggest cells: East and West each have 32 duplicates; East has 12 of the 29 missing order IDs; West has 16 of the 37 bad amounts. | notebook cell 12 (table in cell 3) |
| **weekly-sales.png** | Sales of the clean table added up per week (Monday to Sunday), in USD, all branches. The thin line is each week, the thick line is the average of the last 4 weeks, which smooths out the ups and downs. | notebook cell 13 |

### The report totals

The README does not print these, but the Power BI cards must show them (`powerbi/06-checks.md`).

| Number | What it means | How it is worked out | Where |
|---|---|---|---|
| **USD 2,265,769.78 sales** | All sales in the clean table. | Sum of `sales` over the 9,836 clean rows. | notebook cell 9 |
| **USD 282,653.43 profit** | All profit in the clean table. | Sum of `profit`. | notebook cell 9 |
| **12.5% profit margin** | Profit per 100 of sales. | 282,653.43 / 2,265,769.78 = 12.47%. | notebook cell 9 |
| **4,971 orders** | Distinct order IDs. | Count of distinct `order_id`. | notebook cell 9 |
| **455.80 average order value** | Sales per order. | 2,265,769.78 / 4,971 = 455.80. | `powerbi/06-checks.md` |
| **West 714,519.07, East 666,739.35, Central 496,613.97, South 387,897.39** | Sales by branch. | Sum of `sales` per branch, counted by pandas and again by SQL; the two must match. | notebook cell 7 |
| **Margins: West 15.0%, East 13.6%, South 11.8%, Central 7.9%** | Profit margin per branch. | Profit / sales per branch from cell 7, for example West 107,342.94 / 714,519.07 = 15.0%. The notebook does not print them. | `powerbi/06-checks.md` |
| **Technology 831,236.01, Furniture 724,968.37, Office Supplies 709,565.40** | Sales by category. Margins 17.4%, 2.4% and 17.0%, worked out the same way. | Sum per category. | notebook cell 9; margins in `powerbi/06-checks.md` |

### The diagrams

| Number | Where you see it | What it means |
|---|---|---|
| **192, 10,089, 253** | header.svg | Branch files, rows read, errors caught. See the table above. |
| **1 click to rebuild** | header.svg | One command (`python run.py`, or a double-click on `run.bat`) rebuilds everything. |
| **01 to 05** | how-it-works.svg | The five steps: collect, clean, check, merge, report. |
| **48 files** (four times) | mental-model.svg | Each branch sends 48 monthly files. |
| **02/03/2019, "$1,234.50", "Mar 05 2019", "3 pcs"** | mental-model.svg | Examples of how East, Central and South write dates, amounts and quantities. 02/03/2019 is East's day/month/year, so it means 2 March 2019. |
| **5 rules + duplicates** | mental-model.svg | The five rules in section 3, then the duplicate check. |
| **9,836 rows; 253 rows** | mental-model.svg | The clean table and the set-aside list. |
| **96, 37, 31, 30, 30, 29** | mental-model.svg | The six reasons, short names: pasted twice, amount not a number, bad date (date not readable), wrong month, qty ≤ 0 (quantity missing or below 1), no ID. |
| **Six layers** | data-flow.svg | Bronze, Silver, Gold, Semantic, Analytical and Reporting layer, left to right. Under each, the function or tool that does it. `file_log.csv` sits in a grey strip: it is the run log, not a layer. |
| **10,089 rows, 48 skipped** | data-flow.svg | Order lines read; totals rows skipped and only counted in `file_log.csv`. |
| **9,836 / 253 (157 + 96) rows** | data-flow.svg | Passed every rule / set aside: broke a rule plus pasted twice. |
| **192 rows, one per workbook** | data-flow.svg | `file_log.csv` has one row per branch file. |
| **9,836 rows** | data-model.svg | The `Sales` fact table. The picture is the Semantic layer. |
| **253 rows** | data-model.svg | The `Set Aside` table. Its key is `file` + `excel_row`. |
| **192 rows** | data-model.svg | The `Files` table, one row per branch file. |
| **4 rows** | data-model.svg | The `Branch` table: one row per branch. |
| **1,461 rows** | data-model.svg | Days in the `Date` table: every day from 1 Jan 2016 to 31 Dec 2019. 366 (2016 is a leap year) + 365 + 365 + 365 = 1,461. |
| **1 and \*** | data-model.svg | "One to many": one branch (or one day) links to many rows in the other table. |

Things that can look wrong but are not:

- **The source has 9,994 lines, but 10,089 rows were read.** 9,994 − 1 line the source repeated (removed first) = 9,993 real lines. The demo then pasted 96 of them twice: 9,993 + 96 = 10,089 rows read. And 9,993 − 157 rule breaks = 9,836 clean rows. So every real line ends up either clean or set aside for a rule, and every pasted copy is set aside.
- **The 48 totals rows are not in the 10,089.** They are layout, not orders. They are counted apart, in `file_log.csv`.
- **Excel row numbers in West files start at 5.** West has two title rows, a blank row and the header on row 4. `excel_row` in `set_aside_rows.csv` is the real row number you see in Excel, so you can go straight to it.
- **The rule names differ between the diagram and the code.** mental-model.svg says "31 bad date" and "30 qty ≤ 0"; the code says "date not readable" and "quantity missing or below 1". They are the same rows. The 31 dates were 16 empty cells and 15 that said "TBC"; the 30 quantities were all 0 or −2.
- **A row that breaks two rules gets one reason.** The check takes the first rule it breaks, in the order listed in section 3.
- **Set-aside values look messy.** On purpose: they are kept exactly as the branch sent them ("8 pcs", "1st class"), so the branch can find the row and see what was wrong.
- **Profit in the clean row is 19.66, in the source file 19.656.** The demo rounds amounts to the cent when it makes the branch files. The clean row matches the branch file exactly.
- **2.5% for South too.** South's error rate is 40 / 1,628 = 2.457%, which rounds to 2.5%. The overall 2.5% is 253 / 10,089.
- **4,971 orders but 9,836 order lines.** One order can hold several products, each on its own line.
- **The Date table runs 1 Jan 2016 to 31 Dec 2019, the orders 3 Jan 2016 to 30 Dec 2019.** The table covers whole years on purpose, so no day is missing.
- **The Excel report has no Semantic layer step.** pandas sums `clean_sales.csv` straight into the Summary and Weekly sales sheets, and the Set aside and Clean data sheets copy the Gold layer's two files. Only Power BI has a model. At 10 thousand rows a model would add nothing to the workbook.
- **The set-aside rows sit in the Gold layer, not the Bronze layer.** Their values are the ones the branch sent (Bronze), but it is `check()` that picks them, so the file is written after the rules run.
- **The Power BI `Date` table takes its first and last year from `Sales`.** Only the range; every day in between is generated. `Branch` is built from `Files`, the run log.
- **The last week's sales are only 713.79.** The week starting Monday 30 Dec 2019 has one day of data (`powerbi/06-checks.md`).

## 5. What the results mean for the business

- **Nothing is lost and nothing is guessed.** Every row read lands in the clean table or the set-aside list: 10,089 = 9,836 + 253. A manager can trust that the total is the total.
- **1 row in 40 had a mistake.** 253 of 10,089 rows (2.5%). Copied by hand, each of them would have gone into the totals unnoticed.
- **Lines pasted twice are the biggest single problem.** 96 of the 253 errors (96 / 253 = 37.9%). Each one would have counted the same sale twice.
- **Each branch has its own typical mistake.** East left out 12 of the 29 missing order IDs; West sent 16 of the 37 amounts that were not numbers. The set-aside list tells each branch exactly which rows to fix, by file and Excel row, so the same mistake can stop at the source.
- **No branch is much worse than the others.** Error rates run from 2.3% (Central) to 2.6% (East and West). West has the most errors (84) because it sends the most rows (3,235).
- **The sales report can now be trusted.** West sells the most (USD 714,519.07) at the best margin (15.0%). Central has the lowest margin (7.9%). Furniture sells USD 724,968.37 but keeps only 2.4% as profit, against about 17% for Technology and Office Supplies.
- **A hidden problem came out too.** 225 order lines carried invisible non-breaking spaces in product names. In Excel that breaks a VLOOKUP without any warning. The cleaner fixes them.

## 6. Interview questions you can expect

**Explain the project in 30 seconds.**
A retail chain gets one Excel file per branch per month, each in its own layout, and someone was copying them together by hand every week. I wrote one Python script that reads all 192 files, cleans every value to one standard, checks every row against five rules and for duplicates, and merges the good rows into one table for a weekly Excel report and a Power BI report. Of 10,089 rows read, 253 were set aside with the reason, and a known answer key proves it caught exactly the planted mistakes and nothing else.

**Why set bad rows aside instead of fixing or deleting them?**
Fixing means guessing, and deleting hides the problem. A set-aside row keeps its file, its Excel row number and its values as sent, so the branch can fix it at the source and the next month's file comes in right. The totals only use rows that passed.

**How do you know nothing is lost?**
`run.py` asserts for every file that rows read = clean + set aside, and stops if not. The notebook then checks three ways: the rows set aside are exactly the 253 rows in the answer key; every clean row matches a source line on all 13 columns; and SQL in SQLite gives the same counts and totals as pandas.

**Why not let the computer guess the date format?**
Because 02/03/2019 is 2 March in East's format and 3 February in the US format. A guess would be wrong without any error. So a real Excel date is used as it is, and a text date is read only with the format set for that branch in `client.yaml`. A text date from any other branch is set aside as "date not readable".

**How do you catch lines pasted twice, and why after cleaning?**
After cleaning, a row that is identical in all 13 columns to an earlier row of the same branch is set aside; the first copy stays. It runs after cleaning so that "Std" and "Standard Class", or "5 pcs" and 5, compare as equal. The trade-off: a real order line that is truly identical to another would also be set aside. The source had one such line, and it was removed before the demo files were made.

**What happens when a whole file is wrong?**
A wrong file name, a missing `Sales` sheet or a missing column stops the run with one line naming the file and the problem, before anything is written. A wrong value inside a row never stops the run: the row is set aside. One broken file should be fixed, one bad row should not block the week's report.

**How did you test it?**
Against a known answer. The demo script planted 253 mistakes with a fixed random seed and wrote down each one's file, row and reason in `planted_errors.csv`. The notebook asserts the pipeline found exactly those, at the right place, for the right reason.

**How would you set it up for a real client?**
Change `config/client.yaml`: the file name pattern, the sheet name, every header spelling they use, the date format of each branch that types dates as text, the minimum quantity, the colours. Add their spellings to `value_map.csv`, put their files in `data/input/` and run the same command. No code changes.

**Why does it rebuild everything every time?**
The data is small (about 10 thousand rows), so a full rebuild takes seconds and can never leave a half-updated report. With millions of rows a week I would only read new files.

**How is the Power BI model built?**
`Sales` is the fact table. A `Branch` table with one row per branch filters `Sales`, `Files` and `Set Aside` together, so one slicer works on both pages. A `Date` table filters only `Sales`. `Files` and `Set Aside` have no date link on purpose: they are counted per file, and a set-aside row may have no readable date at all. Every filter runs one way, from the small tables to the big ones.

## 7. Limits, in plain words

- A text date is read only with its branch's format. A new branch that types dates differently needs its format added to `client.yaml`, or its dates are set aside.
- Amounts must use a minus sign for a loss (not brackets) and a dot for decimals (not a comma). "1.234,50" would be read wrong.
- The amount cleaner keeps only digits, the minus sign and the dot, so a typo that mixes letters into a number (like "12O.50") is read as a number, not set aside.
- Quantities are whole numbers.
- "Date outside the file's month" is judged against the month in the file name, so a file named with the wrong month sets every row aside.
- Two order lines that are truly identical in all 13 columns are treated as one line pasted twice.
- The demo's mistakes were planted on purpose. A client's files will have their own kinds of mistakes, and new ones may need a new rule.
