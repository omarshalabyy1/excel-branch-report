# 2. The model

Open **Model view** (the third icon on the left).

## Tables

| Table | Grain (one row per) | Key | Rows |
|---|---|---|---|
| `Sales` | order line that passed every rule | none needed (it is the fact table) | 9,836 |
| `Set Aside` | row set aside, with its reason | `file` + `excel_row` | 253 |
| `Files` | branch file | `file` | 192 |
| `Branch` | branch | `branch` | 4 |
| `Date` | day, 2016-01-01 to 2019-12-31 | `Date` | 1,461 |
| `_Measures` | holds the measures only | none | 1 (hidden) |

The `_Measures` table is created in step 3 (`03-measures.dax`). There are no calculated columns and no calculated tables: every column comes from Power Query.

## Mark the date table

Select the `Date` table, then **Table tools > Mark as date table**, and pick the `Date` column.

Why: the `Date` table (M code in `01-power-query.md`) has one row per day with no gaps, so weeks, months and years group correctly. Turn off **File > Options and settings > Options > Current file > Data load > Auto date/time** so Power BI does not add hidden date tables of its own.

## Relationships

Drag each "one" column onto its "many" column, then open the relationship (double-click the line) and check the settings.

| From (one) | To (many) | Cardinality | Cross-filter direction | Active | Why |
|---|---|---|---|---|---|
| `Branch[branch]` | `Sales[branch]` | One to many | Single | Yes | One Branch slicer filters the sales |
| `Branch[branch]` | `Files[branch]` | One to many | Single | Yes | ...the file counts |
| `Branch[branch]` | `Set Aside[branch]` | One to many | Single | Yes | ...and the rows set aside |
| `Date[Date]` | `Sales[order_date]` | One to many | Single | Yes | Weeks, months and years come from the Date table |

Power BI may create some of these on its own when you close Power Query. Delete any other relationship it made (for example between `Files` and `Set Aside`): a second path from `Branch` makes the model ambiguous.

Why single direction everywhere: filters flow from the small tables (Branch, Date) to the big ones, never back, so every number has one meaning.

Why `Files` and `Set Aside` have no Date relationship: they are counted per file, not per order date (a set-aside row may have no readable date at all).

## Hide columns

Hide the columns a report builder should not pick, so slicers and axes always use the dimension (right-click > Hide in report view):

- `Sales[branch]`, `Files[branch]`, `Set Aside[branch]`: use `Branch[branch]`.
- `Sales[order_date]`: use the `Date` columns.
- `Date[Month Number]`: used only for sorting.
- The empty column of `_Measures` (after step 3).

## Sort by column

Select `Date[Month]`, then **Column tools > Sort by column > Month Number**, so months run Jan to Dec, not alphabetically.

## Column formats

Set in **Column tools > Format** with the column selected.

| Column | Format | Why |
|---|---|---|
| `Sales[sales]`, `Sales[profit]` | Currency, 2 decimals | Money to the cent, as in the files |
| `Sales[quantity]`, `Files[rows_read]`, `Files[clean_rows]`, `Files[set_aside_rows]`, `Files[totals_rows_skipped]` | Whole number, thousands separator on | Counts |
| `Set Aside[excel_row]` | Whole number, thousands separator off | A row number to find in Excel, not a count |
| `Date[Date]`, `Date[Week Start]`, `Sales[order_date]` | Short date (`yyyy-mm-dd`) | Same as the CSV files and the checks |
| All `Set Aside` value columns | Text | They are the values exactly as the branch sent them |

## Display folders

Set on each measure in step 3 (**Properties pane > Display folder**):

| Folder | Measures |
|---|---|
| Sales report | Sales, Profit, Profit Margin %, Orders, Order Lines, Average Order Value |
| Data quality | Branch Files, Rows Read, Clean Rows, Rows Set Aside, Duplicate Lines, Rule Breaks, Error Rate %, Totals Rows Skipped |
