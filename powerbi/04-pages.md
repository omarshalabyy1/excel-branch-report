# 4. Pages and visuals

Canvas: 16:9, 1280 × 720 (the default). Set each visual's position and size in **Format > General > Properties**. `x, y, w, h` are in pixels from the top-left corner. Apply the theme (`05-theme.json`) first so colours and fonts are already right.

Rename the pages (double-click the tab) to **Weekly report** and **Data quality**.

## Page 1: Weekly report

The week's numbers by branch, from the one clean table.

| # | Visual | x, y, w, h | Fields | Settings |
|---|---|---|---|---|
| 1 | Text box | 24, 16, 600, 52 | "Branch sales: one clean table, rebuilt every week" | Font 20, bold |
| 2 | Slicer | 640, 12, 260, 56 | Field: `Date[Year]` | Slicer settings > Style: Tile. Selection: multi-select with Ctrl, "Select all" on |
| 3 | Slicer | 916, 12, 340, 56 | Field: `Branch[branch]` | Style: Tile. Selection: multi-select with Ctrl, "Select all" on |
| 4 | Card | 24, 84, 240, 96 | `[Sales]` | Category label on |
| 5 | Card | 272, 84, 240, 96 | `[Profit]` | Category label on |
| 6 | Card | 520, 84, 240, 96 | `[Profit Margin %]` | Category label on |
| 7 | Card | 768, 84, 240, 96 | `[Orders]` | Category label on |
| 8 | Card | 1016, 84, 240, 96 | `[Average Order Value]` | Category label on |
| 9 | Line chart | 24, 196, 820, 300 | X-axis: `Date[Week Start]`; Y-axis: `[Sales]`; Legend: `Branch[branch]` | Title "Weekly sales by branch". X-axis type: Continuous. Legend: top |
| 10 | Clustered bar chart | 860, 196, 396, 300 | Y-axis: `Branch[branch]`; X-axis: `[Sales]`; Tooltips: `[Profit]`, `[Profit Margin %]`, `[Orders]` | Title "Sales by branch". Sort by Sales, descending. Data labels on |
| 11 | Matrix | 24, 512, 820, 192 | Rows: `Date[Year]`, then `Date[Month]`; Columns: `Branch[branch]`; Values: `[Sales]` | Title "Monthly sales by branch". Row subtotals on, column subtotals on. Expand to the month level with the double-arrow icon if you want every month shown |
| 12 | Clustered bar chart | 860, 512, 396, 192 | Y-axis: `Sales[category]`; X-axis: `[Sales]`, `[Profit]` | Title "Sales and profit by category". Sort by Sales, descending. Data labels on |

**Interactions:** keep the default (every visual filters the others). Clicking a branch in visual 10 filters the cards, the weekly line and the matrix to that branch.

## Page 2: Data quality

What each branch sent, and the list of rows to fix at the source.

| # | Visual | x, y, w, h | Fields | Settings |
|---|---|---|---|---|
| 1 | Text box | 24, 16, 700, 52 | "Data quality: what each branch sent" | Font 20, bold |
| 2 | Slicer | 916, 12, 340, 56 | Field: `Branch[branch]` | Same as page 1 (it is synced, see below) |
| 3 | Card | 24, 84, 240, 96 | `[Branch Files]` | Category label on |
| 4 | Card | 272, 84, 240, 96 | `[Rows Read]` | Category label on |
| 5 | Card | 520, 84, 240, 96 | `[Clean Rows]` | Category label on |
| 6 | Card | 768, 84, 240, 96 | `[Rows Set Aside]` | Category label on. Rename on the visual to "Errors caught" |
| 7 | Card | 1016, 84, 240, 96 | `[Error Rate %]` | Category label on |
| 8 | Clustered bar chart | 24, 196, 400, 250 | Y-axis: `Set Aside[reason]`; X-axis: `[Rows Set Aside]` | Title "Rows set aside by reason". Sort by Rows Set Aside, descending. Data labels on |
| 9 | Matrix | 440, 196, 816, 250 | Rows: `Set Aside[reason]`; Columns: `Branch[branch]`; Values: `[Rows Set Aside]` | Title "Reasons by branch". Row and column subtotals on. Conditional formatting > Background color on `Rows Set Aside`: gradient from white (lowest) to #2563EB (highest) |
| 10 | Table | 24, 462, 1232, 242 | `Set Aside[file]`, `Set Aside[excel_row]`, `Set Aside[reason]`, `Set Aside[order_id]`, `Set Aside[order_date]`, `Set Aside[quantity]`, `Set Aside[sales]` | Title "Rows to fix at the source". Sort by file, then excel_row, ascending. Totals off |

**Interactions:** keep the default. Clicking a reason in visual 8 filters the matrix and the table to that reason, so the table becomes the to-do list for one kind of mistake.

## Sync the Branch slicer

**View > Sync slicers**, select the Branch slicer, tick both **Sync** and **Visible** for Weekly report and Data quality. The Year slicer stays on page 1 only: the data quality numbers are per file, not per order date.

## Not used

No drill-through, bookmarks or tooltip pages: two pages and the default interactions answer both questions.
