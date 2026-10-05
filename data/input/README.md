# Input files

What the client supplies, in this folder. Names, sheet and header spellings are set in `config/client.yaml`. `python run.py` checks every file before it writes anything and stops with one line naming the file and the problem.

## Branch files (`inputs.file_name`, `inputs.sheet`)

- One Excel file (`.xlsx`) per branch per month, all in this folder.
- The file name must match `inputs.file_name`, a regular expression with two named parts: `branch` (shown in the report as written) and `month` (`YYYY-MM`). Demo: `West_2019-03.xlsx` with `'(?P<branch>.+)_(?P<month>\d{4}-\d{2})\.xlsx'`.
- The order lines are on the sheet named `inputs.sheet` (demo: `Sales`). Title rows above the table are fine: the header row is found by its order id header. A row whose order id starts with `inputs.totals_row_label` (demo: `Total`, any case) is a totals row and is skipped.
- Every column listed under `columns` must be in every file, under one of its header spellings (case, spaces, `_` and `-` are ignored). Extra columns are ignored.

| Standard column | Required | Type | Example, as a branch may send it |
|---|---|---|---|
| order_id | yes | text | CA-2019-152261 |
| order_date | yes | an Excel date, or text in the branch's `date_formats` format | 02/03/2019 |
| quantity | yes | whole number, may carry a unit | 3 pcs |
| sales | yes | number, may carry a currency sign and thousands commas | $1,234.50 |
| profit | yes | number, minus sign for a loss | -$12.30 |
| category | yes | text | OFFICE SUPPLIES |
| any other column in `columns` | no | text, kept as sent after spaces and spellings are fixed | Std |

The demo's other columns are `ship_mode`, `segment`, `city`, `state`, `product_id`, `sub_category` and `product_name`.

One example row (the East branch's template):

| Order No | Date | Shipping | Customer Type | City | State | SKU | Category | Subcategory | Item | Qty | Amount | Profit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CA-2019-152261 | 02/03/2019 | Standard Class | Consumer | Cuyahoga Falls | Ohio | OFF-BI-10002353 | Office Supplies | Binders | GBC VeloBind Cover Sets | 4 | 18.53 | -12.35 |

**Limits:** a text date is read only with its branch's format in `date_formats`, never guessed (02/03 can be March or February). Amounts use a minus sign for a negative number, not parentheses, and a dot for decimals, not a comma (`1.234,50` would be read wrong). Quantities are whole numbers.

## Spelling map (`inputs.value_map`)

A CSV file: `column, as_sent, standard`. Each `column` must be a standard column in `columns`. Matching ignores case and extra spaces; a value not in the map is kept as sent. List each standard value once (that also fixes its capitals) and every other spelling a branch uses.

| column | as_sent | standard |
|---|---|---|
| ship_mode | Std | Standard Class |
| category | office supplies | Office Supplies |

## What stops the run

One line each, before anything is written:

```
config/client.yaml is missing rules.min_quantity
missing data/input/value_map.csv (inputs.value_map in config/client.yaml)
no branch files (*.xlsx) in data/input/
data/input/<file>: the name does not match inputs.file_name in config/client.yaml
data/input/<file>: no sheet named <sheet> (inputs.sheet)
data/input/<file>: no header row with an order id column (columns.order_id)
data/input/<file>: missing column(s): <columns>
config/client.yaml: date_formats names a branch with no file: <branch>
```

A wrong value inside a row does not stop the run: the row is set aside with its reason in `output/set_aside_rows.csv`.

## The demo files

The 192 demo branch files, `value_map.csv` and `planted_errors.csv` (the demo's answer key, read only by the notebook's checks 1 and 2) are committed. For a client, delete the demo `.xlsx` files and `planted_errors.csv`, then put the client's files here: `.xlsx` files in this folder are ignored by git, so client data is never committed.
