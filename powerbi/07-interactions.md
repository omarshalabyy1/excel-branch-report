# 7. Interactions

## Report setting (once)

**File > Options and settings > Options > Current file > Report settings**: tick **Change default visual interaction from cross highlighting to cross filtering**.

Why: clicking a bar then filters the other visuals to it instead of greying out part of each bar, so every card and chart shows the selected branch's real numbers.

## How to set a cell

Select the source visual (the one you click), then **Format > Edit interactions**. Each other visual shows icons in its top-right corner: **Filter** (funnel) or **None** (circle with a line). Click the one the table below says. Click **Edit interactions** again to finish.

Numbers are the visual `#` in `04-pages.md`. Text boxes (#1) take no part.

## Page 1: Weekly report

| Source (click) | Year slicer #2 | Branch slicer #3 | Cards #4-8 | Weekly line #9 | Branch bar #10 | Monthly matrix #11 | Category bar #12 |
|---|---|---|---|---|---|---|---|
| Year slicer #2 | | Filter | Filter | Filter | Filter | Filter | Filter |
| Branch slicer #3 | Filter | | Filter | Filter | Filter | Filter | Filter |
| Weekly line #9 | None | None | Filter | | Filter | Filter | Filter |
| Branch bar #10 | None | None | Filter | Filter | | Filter | Filter |
| Monthly matrix #11 | None | None | Filter | Filter | Filter | | Filter |
| Category bar #12 | None | None | Filter | Filter | Filter | Filter | |

Cards (#4-8) are never a source: clicking a card selects nothing.

Why None on the slicers: a click on a chart should not shrink the slicer's list, so all years and all branches always stay pickable.

## Page 2: Data quality

| Source (click) | Branch slicer #2 | Cards #3-7 | Reason bar #8 | Reasons matrix #9 | Rows table #10 |
|---|---|---|---|---|---|
| Branch slicer #2 | | Filter | Filter | Filter | Filter |
| Reason bar #8 | None | Filter | | Filter | Filter |
| Reasons matrix #9 | None | Filter | Filter | | Filter |
| Rows table #10 | None | None | None | None | |

What a click changes:

- **A reason in #8:** the matrix and the table show that reason only. Of the cards, only Errors caught and Error Rate % change (the file cards count files, which have no reason).
- **A cell in #9 (reason and branch):** every card shows that branch; the bar and the table show that reason for that branch.
- **A row in #10:** nothing. The table is a to-do list to read or export, not a filter.

## Not used

- Drill-through pages: none.
- Bookmarks and buttons: none.
- Tooltip pages: none. Visual 10 on page 1 uses the default tooltip with Profit, Profit Margin % and Orders added to its Tooltips well.
- Filters pane: no visual-, page- or report-level filters.
