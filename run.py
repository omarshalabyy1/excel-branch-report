"""One click: read every branch file, clean it to one standard, set aside the rows that
break a rule (with the reason), merge, and rebuild the weekly report.

    python run.py        (or double-click run.bat)
"""
import re
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).parent
BRANCH_DIR = ROOT / "data" / "branches"
OUT = ROOT / "output"

# Every header any branch uses, written lower case with single spaces, mapped to one name.
COLUMNS = {
    "order id": "order_id", "order no": "order_id",
    "order date": "order_date", "date": "order_date",
    "ship mode": "ship_mode", "shipping": "ship_mode",
    "segment": "segment", "customer type": "segment",
    "city": "city", "state": "state",
    "product id": "product_id", "sku": "product_id",
    "category": "category",
    "sub category": "sub_category", "subcategory": "sub_category",
    "product name": "product_name", "item": "product_name",
    "quantity": "quantity", "qty": "quantity",
    "sales": "sales", "amount": "sales",
    "profit": "profit",
}
STANDARD = ["order_id", "order_date", "ship_mode", "segment", "city", "state", "product_id",
            "category", "sub_category", "product_name", "quantity", "sales", "profit"]
# Branches that type their dates as text, and the format they use.
DATE_FORMATS = {"East": "%d/%m/%Y", "South": "%b %d %Y"}
SHIP_MODES = {"standard class": "Standard Class", "std": "Standard Class",
              "second class": "Second Class", "2nd class": "Second Class",
              "first class": "First Class", "1st class": "First Class", "same day": "Same Day"}


def header_key(value):
    return re.sub(r"[\s_\-]+", " ", str(value).strip().lower())


def read_branch_file(path):
    """The order lines of one file, under the standard column names."""
    branch, month = path.stem.split("_")
    raw = pd.read_excel(path, header=None, dtype=object)
    keys = raw.map(header_key)
    header_at = keys.index[(keys.map(COLUMNS.get) == "order_id").any(axis=1)][0]
    lines = raw.iloc[header_at + 1:].copy()
    lines.columns = [COLUMNS[k] for k in keys.iloc[header_at]]
    lines["excel_row"] = lines.index + 1
    is_total = lines["order_id"].astype(str).str.strip().str.lower().str.startswith("total")
    lines = lines[~is_total]
    lines.insert(0, "branch", branch.title())
    lines.insert(1, "file", path.name)
    lines.insert(2, "month", month)
    return lines, int(is_total.sum())


def to_date(value, date_format):
    if isinstance(value, datetime):
        return pd.Timestamp(value)
    try:
        return pd.to_datetime(str(value).strip(), format=date_format)
    except ValueError:
        return pd.NaT


def clean(lines):
    """Fix every value to one standard. A value that cannot be read becomes empty."""
    df = lines.copy()
    for col in ["order_id", "ship_mode", "segment", "city", "state", "product_id", "category",
                "sub_category", "product_name"]:
        df[col] = (df[col].astype("string").str.strip().str.replace(r"\s+", " ", regex=True)
                   .replace("", pd.NA))
    for col in ["segment", "category", "sub_category"]:
        df[col] = df[col].str.title()
    df["ship_mode"] = df["ship_mode"].str.lower().map(SHIP_MODES).fillna(df["ship_mode"])
    df["order_date"] = [to_date(v, DATE_FORMATS.get(b)) for v, b in zip(df["order_date"], df["branch"])]
    df["quantity"] = pd.to_numeric(df["quantity"].astype("string").str.extract(r"(-?\d+)")[0])
    for col in ["sales", "profit"]:
        df[col] = pd.to_numeric(df[col].astype("string").str.replace(r"[$,\s]", "", regex=True),
                                errors="coerce")
    return df


def check(df):
    """The reason each row is set aside, or "" when it passes every rule."""
    reason = np.select(
        [df["order_id"].isna(),
         df["order_date"].isna(),
         df["order_date"].dt.strftime("%Y-%m") != df["month"],
         ~(df["quantity"] > 0),
         df["sales"].isna() | df["profit"].isna()],
        ["missing order id", "date not readable", "date outside the file's month",
         "quantity missing or not above zero", "amount not a number"],
        default="")
    passed = reason == ""
    duplicate = passed & df[STANDARD + ["branch"]].duplicated(keep="first")
    return np.where(duplicate, "duplicate of an earlier row", reason)


def write_report(sales, aside, files):
    summary = files.groupby("branch")[["rows_read", "clean_rows", "set_aside_rows"]].sum()
    summary.insert(0, "files", files.groupby("branch").size())
    summary["sales"] = sales.groupby("branch")["sales"].sum().round(2)
    summary["profit"] = sales.groupby("branch")["profit"].sum().round(2)
    summary.loc["All branches"] = summary.sum().round(2)
    weekly = (sales.assign(week_start=sales["order_date"].dt.to_period("W-SUN").dt.start_time)
              .pivot_table(index="week_start", columns="branch", values="sales", aggfunc="sum",
                           fill_value=0).round(2))
    weekly["All branches"] = weekly.sum(axis=1).round(2)
    with pd.ExcelWriter(OUT / "weekly_report.xlsx", engine="openpyxl",
                        date_format="yyyy-mm-dd", datetime_format="yyyy-mm-dd") as writer:
        summary.to_excel(writer, sheet_name="Summary")
        weekly.sort_index(ascending=False).to_excel(writer, sheet_name="Weekly sales")
        aside.to_excel(writer, sheet_name="Set aside", index=False)
        sales.to_excel(writer, sheet_name="Clean data", index=False)
        for sheet in writer.sheets.values():
            sheet.freeze_panes = "B2"
            for column in sheet.columns:
                sheet.column_dimensions[column[0].column_letter].width = 16


def main():
    started = time.perf_counter()
    OUT.mkdir(exist_ok=True)
    paths = sorted(BRANCH_DIR.glob("*.xlsx"))
    read = [read_branch_file(p) for p in paths]
    lines = pd.concat([r[0] for r in read], ignore_index=True)

    df = clean(lines)
    df["reason"] = check(df)
    ok = df["reason"] == ""
    sales = df.loc[ok, ["branch", "file"] + STANDARD]
    aside = lines.loc[~ok, ["file", "excel_row", "branch"] + STANDARD]
    aside[STANDARD] = aside[STANDARD].astype("string")  # the values exactly as the branch sent them
    aside.insert(3, "reason", df.loc[~ok, "reason"])

    files = pd.DataFrame({"file": [p.name for p in paths],
                          "branch": [p.stem.split("_")[0].title() for p in paths],
                          "month": [p.stem.split("_")[1] for p in paths],
                          "rows_read": lines.groupby("file").size().reindex([p.name for p in paths]).values,
                          "totals_rows_skipped": [r[1] for r in read]})
    files["clean_rows"] = files["file"].map(sales.groupby("file").size()).fillna(0).astype(int)
    files["set_aside_rows"] = files["file"].map(aside.groupby("file").size()).fillna(0).astype(int)
    assert (files["rows_read"] == files["clean_rows"] + files["set_aside_rows"]).all()

    sales.to_csv(OUT / "clean_sales.csv", index=False, date_format="%Y-%m-%d")
    aside.to_csv(OUT / "set_aside_rows.csv", index=False)
    files.to_csv(OUT / "file_log.csv", index=False)
    write_report(sales, aside, files)

    print(f"{len(paths)} files, {len(lines)} rows read: {len(sales)} clean, {len(aside)} set aside")
    print(aside["reason"].value_counts().to_string())
    print(f"Report rebuilt in {time.perf_counter() - started:.1f} seconds: output/weekly_report.xlsx")


if __name__ == "__main__":
    main()
