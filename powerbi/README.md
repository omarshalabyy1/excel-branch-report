# Power BI: build the report step by step

The report reads the three files `run.py` writes to `output/` and answers two questions:

1. **Weekly report:** how much each branch sold and earned, week by week, from one trusted table.
2. **Data quality:** how many rows each branch sent, how many were clean, and which rows were set aside and why, so each branch can fix them at the source.

Everything below is copy and paste. **Start with [`08-build-checklist.md`](08-build-checklist.md)**: 32 numbered steps from opening Power BI Desktop to the last screenshot, with a check number at each point. It points to the other files:

| File | What it holds |
|---|---|
| [`01-power-query.md`](01-power-query.md) | The `OutputFolder` parameter and five queries (M code) |
| [`02-model.md`](02-model.md) | Tables, date table, four relationships, hidden columns, sort, formats, display folders, with the reason for each |
| [`03-measures.dax`](03-measures.dax) | The `_Measures` table and 14 measures, grouped by page |
| [`04-pages.md`](04-pages.md) | Two pages, 22 visuals: type, fields, position and size, settings |
| [`05-theme.json`](05-theme.json) | The theme: **View > Themes > Browse for themes**, pick this file |
| [`06-checks.md`](06-checks.md) | The numbers every card and total must show |
| [`07-interactions.md`](07-interactions.md) | Which visual filters which, per page |
| [`08-build-checklist.md`](08-build-checklist.md) | The build, step by step |

The theme uses the portfolio site's colours (navy `#0E1630`, blue `#2563EB`, soft grey page `#F4F6FB`), so every project report looks like one family. The site's font, Geist, is not in Power BI's font list, so the theme uses Segoe UI.

Before you start, run `python run.py` once so `output/` is up to date. After a new week of branch files, run it again (or double-click `run.bat`) and press **Refresh** in Power BI: that is the one click.

When the report is built:

- Save it as `powerbi/branch-report.pbix`.
- Export one image per page (File > Export > PDF, or a screenshot at 1280 × 720) to `powerbi/screenshots/weekly-report.png` and `powerbi/screenshots/data-quality.png`.
- Add a "Power BI report" section with both images to the main README, after "The result".
