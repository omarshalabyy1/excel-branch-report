# Power BI: build the report step by step

The report reads the three files `run.py` writes to `output/` and answers two questions:

1. **Weekly report:** how much each branch sold and earned, week by week, from one trusted table.
2. **Data quality:** how many rows each branch sent, how many were clean, and which rows were set aside and why, so each branch can fix them at the source.

Everything below is copy and paste. Follow the files in order:

| Step | File | What you do |
|---|---|---|
| 1 | [`01-power-query.md`](01-power-query.md) | Create the `OutputFolder` parameter and five queries (paste the M code) |
| 2 | [`02-model.md`](02-model.md) | Mark the date table, create four relationships, hide and sort columns |
| 3 | [`03-measures.dax`](03-measures.dax) | Create the `_Measures` table and paste 14 measures |
| 4 | [`05-theme.json`](05-theme.json) | View > Themes > Browse for themes, pick this file |
| 5 | [`04-pages.md`](04-pages.md) | Build the two pages, visual by visual |
| 6 | [`06-checks.md`](06-checks.md) | Compare every card and total with the numbers there |

Before you start, run `python run.py` once so `output/` is up to date. After a new week of branch files, run it again (or double-click `run.bat`) and press **Refresh** in Power BI: that is the one click.

When the report is built:

- Save it as `powerbi/branch-report.pbix`.
- Export one image per page (File > Export > PDF, or a screenshot at 1280 × 720) to `powerbi/screenshots/weekly-report.png` and `powerbi/screenshots/data-quality.png`.
- Add a "Power BI report" section with both images to the main README, after "The result".
