# New client

This repo is a GitHub template. A new client gets a **private** repo from it (Use this template > Create a new repository > Private); client data never goes into this public repo.
Everything that changes per client is in two places: `config/client.yaml` and the files in `data/input/`. There is no secret, so there is no `.env`.

## Done in the template

What the client gets with no work. Hours are an estimate of building each part from scratch.

| # | Part | Estimate (hours) |
|---|---|---|
| A | Branch file reader: header row found wherever it sits, title and totals rows skipped, every header spelling mapped to one name, one-line input checks (`run.py`, `config.py`) | 3 |
| B | Cleaning: spaces, the spelling map, each branch's date format (never guessed), amounts and quantities read from text (`run.py`) | 2 |
| C | Five rules and duplicates; the set-aside list with reason, file, Excel row and values as sent; the file log; rows read = clean + set aside for every file (`run.py`) | 2 |
| D | The weekly Excel report: Summary, Weekly sales, Set aside, Clean data; `run.bat` | 1.5 |
| E | Client settings: `config/client.yaml`, `config.py` (`load_config()`), the Power BI theme written from the config (`theme.py`) | 1.5 |
| F | Analysis notebook: every number, a SQL recount, the answer-key checks, three charts (`analysis/analysis.ipynb`) | 3 |
| G | Power BI build pack: 5 queries, the model, 14 measures, 2 pages with 22 visuals, interactions, checks, a 32-step checklist (`powerbi/`) | 6 |
| H | README with its diagrams, and the input file guide (`data/input/README.md`) | 3 |
| | **Total** | **22** |

## Configure

Per client, file by file. Hours are an estimate.

| File | Key | Example | Estimate (hours) |
|---|---|---|---|
| `config/client.yaml` | `client.name`, `client.currency`, `report.title`, `report.colours` | `EGP`, `"#0F766E"` | 0.25 |
| `config/client.yaml` | `inputs.file_name`, `inputs.sheet`, `inputs.totals_row_label` | `'Nile - (?P<branch>[A-Za-z ]+) - (?P<month>\d{4}-\d{2})\.xlsx'`, `Daily`, `Grand total` | 0.5 |
| `config/client.yaml` | `columns`: every header spelling the branches use | `sales: [Net Sales, Sales EGP]` | 1 |
| `config/client.yaml` | `date_formats`: branches that type dates as text | `Giza: "%d/%m/%Y"` | 0.25 |
| `data/input/value_map.csv` | the spellings to unify | `category,bath,Bathroom` | 1 |
| `config/client.yaml` | `rules.min_quantity` | `2` | 0.25 |
| Run `run.py`, `theme.py` and the notebook; go through the set-aside list with the client and fix the config | | | 1.25 |
| | **Subtotal without Power BI** | | **4.5** |
| `powerbi/` | build from `08-build-checklist.md`; in the Sales query list the client's columns; fill `06-checks.md` from the notebook's report numbers and SQL recount | | 2.5 |
| | **Total with Power BI** | | **7** |

## Custom, by offering

Each offering on the site uses part of the template. Template hours count only the parts (A to H above) that the offering delivers. Hours are estimates.

### 16. Merge many Excel files into one report

Uses A, B, C, D, E, F, H (16 hours); configure 4.5 hours.

| Work | Estimate (hours) |
|---|---|
| CSV files as well as Excel | 1 |
| A summary by supplier or month instead of branch, as the client asks | 1 |
| Weeks starting Saturday or Sunday (`run.py`, the notebook, the Date query's `Day.Monday`) | 1 |
| The one-page guide in the client's words: where to drop files, how to run | 0.5 |
| **Total** | **3.5** |

If the client wants a Power Query workbook instead of the Python tool, the cleaning and the rules are rebuilt in M: add 6 hours.

### 15. Excel data cleanup

Uses A, B, C, D, E, F, H (16 hours); configure 4.5 hours.

| Work | Estimate (hours) |
|---|---|
| A change log of every value changed, before and after (the set-aside list covers rows set aside, not values fixed) | 3 |
| One file with no branch or month in its name: a simpler `file_name` and no month rule | 1 |
| Broken formulas and formats fixed in the client's own workbook | 2 |
| **Total** | **6** |

### 18. One-click Excel report automation

Uses A, B, C, D, E, F, H (16 hours); configure 4.5 hours.

| Work | Estimate (hours) |
|---|---|
| The client's own report layout filled in (their Excel template) instead of the four standard sheets | 4 |
| Tested against the client's last real report: every total reconciled | 2 |
| Scheduled run and the report e-mailed (Advanced) | 2 |
| **Total** | **8** |

### 3. Spreadsheets to a real SQL database

Uses A, B, C, E, F, H (14.5 hours); configure 4.5 hours. This repo writes files, not a database, so the load step is custom.

| Work | Estimate (hours) |
|---|---|
| PostgreSQL in Docker, the password in `.env`, and a load step for the clean table, the set-aside list and the file log, with row-count and total checks | 3 |
| Table design: keys and relationships around how the business works | 4 |
| Views for Excel and Power BI | 2 |
| Data dictionary | 1.5 |
| Backup | 1 |
| **Total** | **11.5** |

## Share already done (estimate)

Template hours ÷ (template + configure + custom) hours, per offering:

| Offering | Arithmetic | Share already done |
|---|---|---|
| 16. Merge many Excel files into one report | 16 ÷ (16 + 4.5 + 3.5) = 16 ÷ 24 | **67%** (66.7%) |
| 16, as a Power Query workbook instead of Python | 16 ÷ (16 + 4.5 + 3.5 + 6) = 16 ÷ 30 | **53%** (53.3%) |
| 15. Excel data cleanup | 16 ÷ (16 + 4.5 + 6) = 16 ÷ 26.5 | **60%** (60.4%) |
| 18. One-click Excel report automation | 16 ÷ (16 + 4.5 + 8) = 16 ÷ 28.5 | **56%** (56.1%) |
| 3. Spreadsheets to a real SQL database | 14.5 ÷ (14.5 + 4.5 + 11.5) = 14.5 ÷ 30.5 | **48%** (47.5%) |
| The whole demo: offering 16 plus the Power BI report | 22 ÷ (22 + 7 + 3.5) = 22 ÷ 32.5 | **68%** (67.7%) |

## Steps

1. Create the private repo from the template and clone it.
2. Delete the demo files: `git rm data/input/*.xlsx data/input/planted_errors.csv`. Keep `data/input/README.md`; replace `data/input/value_map.csv` with the client's spellings. `data/demo/` is demo only and can be deleted too.
3. Put the client's branch files in `data/input/` ([columns and examples](../data/input/README.md)). `.xlsx` files there are ignored by git.
4. Edit `config/client.yaml`.
5. `pip install -r requirements.txt`, then `python run.py`. It stops with one line if a file or a key is wrong; fix and run again.
6. `python theme.py`, then run the notebook (Run All). Go through `output/set_aside_rows.csv` with the client.
7. Build the Power BI report from `powerbi/08-build-checklist.md`.

## Second-client drill (2026-10-05)

The acceptance test of the template: a copy of the repo, a made-up second client, a run from scratch.

**Client B (drill):** "Nile Home Stores", currency `EGP`, title "Nile Home weekly report", teal colours (`#0F766E` main, page `#F0FDFA`), Excel report `nile_weekly.xlsx`.

- Files named `Nile - Cairo - 2025-03.xlsx` (Cairo, Giza, Alex), sheet `Daily`, 5 or 6 rows each.
- Its own headers: `Invoice No` / `Inv #`, `Invoice Date` / `Date`, `Item Group` / `Group`, `Pieces` / `Qty`, `Net Sales` / `Sales EGP`, `Margin`, `Item`. Cairo adds an extra `Cashier` column, a title row and a `Grand total` row.
- Giza types dates as text `dd/mm/yyyy` (declared in `date_formats`). Alex types one date as text with no format declared.
- `rules.min_quantity: 2`. Category spellings `KITCHEN`, `bath`, `decor`, `DECOR` mapped in `value_map.csv`. One amount sent as `EGP 1,200.50`, one as `n/a`.
- One case for each rule: a quantity of 1 and one of 0, a date in April in a March file, a line pasted twice, an unreadable date (`TBC`), a text date with no format, a missing order ID.

| What | Demo | Client B (drill) |
|---|---|---|
| Files, rows read | 192 files, 10,089 rows | 3 files, 16 rows |
| Clean + set aside | 9,836 + 253 | 8 + 8 |
| Set aside by reason | 96 duplicates, 37 amount, 31 date not readable, 30 outside the month, 30 quantity below 1, 29 missing ID | 2 date not readable, 2 quantity below 2, 1 each of the other four |
| Totals rows skipped | 48 (`Total`) | 1 (`Grand total`) |
| Sales, profit | USD 2,265,769.78, 282,653.43 | EGP 5,690.50, 1,240.00 |
| Margin, orders, average order | 12.5%, 4,971, 455.80 | 21.8%, 8, 711.31 |
| Excel report | `output/weekly_report.xlsx` | `output/nile_weekly.xlsx` |
| Power BI theme | "Branch Excel report", `#2563EB` | "Nile Home weekly report", `#0F766E`, page `#F0FDFA` |
| Notebook | 0 errors; checks 1 and 2 pass | 0 errors; checks 1 and 2 skipped (no answer key); titles name Nile Home Stores, amounts in EGP |

**By hand:** clean sales Cairo 500.00 + 1,200.50 = 1,700.50; Giza 180.00 + 900.00 + 640.00 = 1,720.00; Alex 350.00 + 1,500.00 + 420.00 = 2,270.00; total 5,690.50. Profit 420 + 230 + 590 = 1,240.00; margin 1,240 ÷ 5,690.50 = 21.8%. Categories Kitchen 3,840.50, Bathroom 1,080.00, Decor 770.00. Every output number matched.

**Clear failures**, one line each, run on the Client B copy:

```
config/client.yaml is missing rules.min_quantity
config/client.yaml is missing columns.profit
config/client.yaml is not valid YAML near line 13 (quote a value with # or :)
missing data/input/value_map.csv (inputs.value_map in config/client.yaml)
no branch files (*.xlsx) in data/input/
data/input/Nile - Alex - 2025-03.xlsx: missing column(s): profit
data/input/alex march.xlsx: the name does not match inputs.file_name in config/client.yaml
data/input/Nile - Giza - 2025-03.xlsx: no sheet named Daily (inputs.sheet)
config/client.yaml: date_formats names a branch with no file: giza
data/input/value_map.csv: names column(s) that are not in columns: ship_mode
```

The drill found two gaps, both fixed: an unquoted `Inv #` in `columns` made the YAML invalid with a long traceback (`load_config()` now stops with the line above), and the weekly sales chart printed every value from 500 to 1,499 as "1k" (the axis now shows full numbers).

**Nothing hard-coded:** this search over `run.py`, `config.py`, `theme.py`, `run.bat`, `powerbi/03-measures.dax`, the Power Query M code in `powerbi/01-power-query.md` and the notebook's code cells finds nothing:

```
Sample retail chain|USD|\$\d|\$\{|West|East|Central|South|Order No|\bQty\b|\bAmount\b|Subcategory|Customer Type|\bSKU\b|Shipping|Standard Class|2nd class|\bStd\b|Office Supplies|Furniture|Technology|%d/%m/%Y|%b %d %Y|[Ss]uperstore|weekly_report\.xlsx|sheet_name=.Sales|TOTAL|startswith\(.total|below 1|> 0|#[0-9A-Fa-f]{6}|\(\?P<branch>
```

These keep the demo's values on purpose: the README and the diagrams in `docs/`, `powerbi/06-checks.md` and `powerbi/08-build-checklist.md` (the demo run's numbers), `data/input/` (the demo files and their answer key) and `data/demo/` (the demo source and the script that made the branch files).

**Nothing broke:** after the change, `python run.py` on the demo files gives the same outputs as before, row for row (192 files, 10,089 rows read, 9,836 clean, 253 set aside), apart from the file names (now `West_2016-01.xlsx`) and the quantity reason, now "quantity missing or below 1".

## Beyond the template standard

What this repo needed that `portfolio/docs/template-standard.md` does not say:

- **Demo tooling folder:** `data/demo/` (the source and the generator) is exempt from the search, like the README and the diagrams.
- **Answer-key checks:** the notebook's checks against the planted mistakes run only when `data/input/planted_errors.csv` exists, so a client run skips them instead of failing.
- **Branch and month from the file name:** `inputs.file_name` is a regular expression with named parts, checked for every file.
- **A spelling map instead of a mapping table:** with no database, the mapping is `data/input/value_map.csv`, checked against `columns`.
- **Invalid YAML** stops with one line, like a missing key.
