# 8. Build checklist

Follow in order. A **Check** line is a number to verify before going on (all from `06-checks.md`); if it is off, fix that step first.

## Prepare

1. In the repo folder run `python run.py` (or double-click `run.bat`).
   **Check:** it prints `192 files, 10089 rows read: 9836 clean, 253 set aside`.
2. Open Power BI Desktop, then **Blank report**.
3. **File > Options and settings > Options > Current file**:
   - **Data load:** untick **Auto date/time**.
   - **Report settings:** tick **Change default visual interaction from cross highlighting to cross filtering**.
4. **View > Themes > Browse for themes**, pick `powerbi/05-theme.json`.

## Power Query (`01-power-query.md`)

5. **Home > Transform data**. Create the `OutputFolder` parameter with your repo's `output\` path.
6. Create the queries in this order, pasting each one's M code: `Sales`, `Set Aside`, `Files`, `Branch`, `Date`.
7. **Home > Close & apply**.
8. Open **Table view** (second icon on the left) and click each table; the row count is at the bottom left.
   **Check:** Sales 9,836 · Set Aside 253 · Files 192 · Branch 4 · Date 1,461.

## Model (`02-model.md`)

9. **Model view**: delete any relationship Power BI made on its own, then create the four relationships in the table, each One to many, Single, Active.
10. Mark `Date` as the date table (column `Date`).
11. Hide the columns listed under "Hide columns".
12. Sort `Date[Month]` by `Month Number`.
13. Set the column formats.

## Measures (`03-measures.dax`)

14. **Home > Enter data**, name the table `_Measures`, **Load**.
15. Paste the 14 measures one by one into `_Measures`, setting each one's format string and display folder. Hide the empty column.
16. On a blank page, drop a card with `[Sales]` and one with `[Rows Read]` (Display units: None).
   **Check:** 2,265,770 and 10,089. Delete both cards.

## Page 1: Weekly report (`04-pages.md`)

17. Rename the page to **Weekly report**. Build visuals 1 to 12 in order, with their position and size.
18. **Check** with no slicer selected: Sales 2,265,770 · Profit 282,653 · Profit Margin % 12.5% · Orders 4,971 · Average Order Value 455.80.
19. **Check** visual 10 data labels: West 714,519 · East 666,739 · Central 496,614 · South 387,897.
20. **Check** visual 12 Sales labels: Technology 831,236 · Furniture 724,968 · Office Supplies 709,565.
21. **Check:** pick 2019 in the Year slicer: Sales 725,529 · Orders 1,674. Clear the slicer.

## Page 2: Data quality (`04-pages.md`)

22. Add a page, rename it **Data quality**. Build visuals 1 to 10 in order.
23. **Check** cards: Branch Files 192 · Rows Read 10,089 · Clean Rows 9,836 · Errors caught 253 · Error Rate % 2.5%.
24. **Check** visual 8: duplicate of an earlier row 96 · amount not a number 37 · date not readable 31 · date outside the file's month 30 · quantity missing or below 1 30 · missing order id 29.
25. **Check** visual 9 column totals: Central 55 · East 74 · South 40 · West 84.

## Slicers and interactions

26. **View > Sync slicers**: Branch slicer synced and visible on both pages; Year slicer on page 1 only.
27. Set every interaction as in `07-interactions.md`, page by page.
28. **Check:** on page 1 click West in visual 10: Sales 714,519 · Orders 1,600. Click it again to clear.
29. **Check:** on page 2 pick Central in the Branch slicer: Rows Read 2,347 · Clean Rows 2,292 · Errors caught 55 · Error Rate % 2.3%. Clear the slicer.

## Save and screenshots

30. **File > Save as** `powerbi/branch-report.pbix`.
31. With no slicer selected, export each page at 1280 × 720 (**File > Export > Export to PDF**, or a screenshot of the page) to `powerbi/screenshots/weekly-report.png` and `powerbi/screenshots/data-quality.png`.
32. In the main `README.md`, add a "Power BI report" section with both images after "The result". Commit and push.
