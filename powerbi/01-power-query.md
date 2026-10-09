# 1. Power Query

Open Power BI Desktop, then **Home > Transform data** to open the Power Query editor. For each query below: **Home > New source > Blank query**, rename it (right-click > Rename) to the name in the heading, open **Home > Advanced editor**, delete what is there and paste the code.

Every query sets its column types with the `en-US` culture, so dates like `2016-01-03` and amounts like `261.96` read the same on any Windows language setting.

| Query | Source | Columns | Renames | Load |
|---|---|---|---|---|
| `OutputFolder` | parameter (text) | none | none | no (parameter) |
| `Sales` | `output/clean_sales.csv` | 15 | none: names stay as `run.py` writes them | yes |
| `Set Aside` | `output/set_aside_rows.csv` | 17 | none | yes |
| `Files` | `output/file_log.csv` | 7 | none | yes |
| `Branch` | the `Files` query | 1 | none | yes |
| `Date` | generated from `Sales[order_date]` | 5 | none | yes |

Why no renames: the column names match the CSV headers and the checks SQL, so a refresh never breaks on a renamed column.

## OutputFolder (parameter)

**Home > Manage parameters > New parameter**

- Name: `OutputFolder`
- Type: Text
- Current value: the full path of the repo's `output` folder, ending with a backslash, for example `C:\GitHub\excel-branch-report\output\`

## Sales (loads)

The clean, trusted table: one row per order line that passed every rule.

```m
let
    Source = Csv.Document(
        File.Contents(OutputFolder & "clean_sales.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    ChangedTypes = Table.TransformColumnTypes(
        PromotedHeaders,
        {
            {"branch", type text}, {"file", type text}, {"order_id", type text},
            {"order_date", type date}, {"ship_mode", type text}, {"segment", type text},
            {"city", type text}, {"state", type text}, {"product_id", type text},
            {"category", type text}, {"sub_category", type text}, {"product_name", type text},
            {"quantity", Int64.Type}, {"sales", Currency.Type}, {"profit", Currency.Type}
        },
        "en-US"
    )
in
    ChangedTypes
```

`Currency.Type` is Power BI's fixed decimal number, so sums stay exact to the cent.

## Set Aside (loads)

One row per row set aside, with the reason and the values exactly as the branch sent them (kept as text on purpose: they are what was wrong).

```m
let
    Source = Csv.Document(
        File.Contents(OutputFolder & "set_aside_rows.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    ChangedTypes = Table.TransformColumnTypes(
        PromotedHeaders,
        {
            {"file", type text}, {"excel_row", Int64.Type}, {"branch", type text},
            {"reason", type text}, {"order_id", type text}, {"order_date", type text},
            {"ship_mode", type text}, {"segment", type text}, {"city", type text},
            {"state", type text}, {"product_id", type text}, {"category", type text},
            {"sub_category", type text}, {"product_name", type text}, {"quantity", type text},
            {"sales", type text}, {"profit", type text}
        },
        "en-US"
    )
in
    ChangedTypes
```

## Files (loads)

One row per branch file: rows read, clean rows, rows set aside, and the totals rows skipped as layout.

```m
let
    Source = Csv.Document(
        File.Contents(OutputFolder & "file_log.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    ChangedTypes = Table.TransformColumnTypes(
        PromotedHeaders,
        {
            {"file", type text}, {"branch", type text}, {"month", type text},
            {"rows_read", Int64.Type}, {"totals_rows_skipped", Int64.Type},
            {"clean_rows", Int64.Type}, {"set_aside_rows", Int64.Type}
        },
        "en-US"
    )
in
    ChangedTypes
```

## Branch (loads)

The four branches, one row each, so one slicer filters sales, files and rows set aside together.

```m
let
    Source = Files,
    Branches = Table.Distinct(Table.SelectColumns(Source, {"branch"})),
    Sorted = Table.Sort(Branches, {{"branch", Order.Ascending}})
in
    Sorted
```

## Date (loads)

One row per day, from `report.date_start` to `report.date_end` in `config/client.yaml` (2016-01-01 to 2019-12-31 in the demo). The range is fixed, never read from Sales, so the Date table is not built from the fact; when the config dates change, type the same two dates here. `run.py` stops if a clean order date falls outside them. Weeks start on Monday, the same as the Python report.

```m
let
    FirstDay = #date(2016, 1, 1),
    LastDay = #date(2019, 12, 31),
    Dates = List.Dates(FirstDay, Duration.Days(LastDay - FirstDay) + 1, #duration(1, 0, 0, 0)),
    AsTable = Table.FromList(Dates, Splitter.SplitByNothing(), {"Date"}),
    Typed = Table.TransformColumnTypes(AsTable, {{"Date", type date}}),
    AddYear = Table.AddColumn(Typed, "Year", each Date.Year([Date]), Int64.Type),
    AddMonthNumber = Table.AddColumn(AddYear, "Month Number", each Date.Month([Date]), Int64.Type),
    AddMonth = Table.AddColumn(AddMonthNumber, "Month", each Date.ToText([Date], [Format = "MMM", Culture = "en-US"]), type text),
    AddWeekStart = Table.AddColumn(AddMonth, "Week Start", each Date.StartOfWeek([Date], Day.Monday), type date)
in
    AddWeekStart
```

All five queries load (no staging queries). Click **Home > Close & apply**.
