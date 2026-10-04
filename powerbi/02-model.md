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

The `_Measures` table is created in step 3 (`03-measures.dax`).

## Mark the date table

Select the `Date` table, then **Table tools > Mark as date table**, and pick the `Date` column.

## Relationships

Drag each "one" column onto its "many" column, then open the relationship (double-click the line) and check the settings.

| From (one) | To (many) | Cardinality | Cross-filter direction | Active |
|---|---|---|---|---|
| `Branch[branch]` | `Sales[branch]` | One to many | Single | Yes |
| `Branch[branch]` | `Files[branch]` | One to many | Single | Yes |
| `Branch[branch]` | `Set Aside[branch]` | One to many | Single | Yes |
| `Date[Date]` | `Sales[order_date]` | One to many | Single | Yes |

Power BI may create some of these on its own when you close Power Query. Delete any other relationship it made (for example between `Files` and `Set Aside`): a second path from `Branch` makes the model ambiguous.

## Hide columns

Hide the columns a report builder should not pick, so slicers and axes always use the dimension (right-click > Hide in report view):

- `Sales[branch]`, `Files[branch]`, `Set Aside[branch]`: use `Branch[branch]`.
- `Sales[order_date]`: use the `Date` columns.
- `Date[Month Number]`: used only for sorting.

## Sort by column

Select `Date[Month]`, then **Column tools > Sort by column > Month Number**, so months run Jan to Dec, not alphabetically.

## Formats

- `Sales[sales]`, `Sales[profit]`: Currency, 2 decimals.
- `Date[Week Start]`: short date.

Display folders are set on the measures in step 3.
