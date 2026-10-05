"""One click: read every branch file, clean it to one standard, set aside the rows that
break a rule (with the reason), merge, and rebuild the weekly report.

    python run.py        (or double-click run.bat)

Every client value comes from config/client.yaml through load_config().
"""
import re
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

from config import load_config

OUT = Path(__file__).parent / "output"
NUMBERS = ["quantity", "sales", "profit"]


def header_key(value):
    return re.sub(r"[\s_\-]+", " ", str(value).strip().lower())


def stop(path, problem):
    raise SystemExit(f"data/input/{path.name}: {problem}")


def read_branch_file(path, cfg, headers):
    """The order lines of one file under the standard column names, and its totals rows skipped."""
    name = re.fullmatch(cfg["inputs"]["file_name"], path.name)
    if not name:
        stop(path, "the name does not match inputs.file_name in config/client.yaml")
    if not re.fullmatch(r"\d{4}-\d{2}", name["month"]):
        stop(path, "the month in the name must be YYYY-MM")
    try:
        raw = pd.read_excel(path, sheet_name=cfg["inputs"]["sheet"], header=None, dtype=object)
    except ValueError:
        stop(path, f"no sheet named {cfg['inputs']['sheet']} (inputs.sheet)")
    keys = raw.map(header_key)
    found = keys.index[(keys.map(headers.get) == "order_id").any(axis=1)]
    if found.empty:
        stop(path, "no header row with an order id column (columns.order_id)")
    standard = [headers.get(k) for k in keys.iloc[found[0]]]
    missing = [c for c in cfg["columns"] if c not in standard]
    if missing:
        stop(path, f"missing column(s): {', '.join(missing)}")

    lines = raw.iloc[found[0] + 1:].copy()
    lines.columns = [s or f"extra {i}" for i, s in enumerate(standard)]  # extra columns are dropped below
    lines = lines[list(cfg["columns"])]
    lines["excel_row"] = lines.index + 1
    label = cfg["inputs"]["totals_row_label"].lower()
    is_total = lines["order_id"].astype(str).str.strip().str.lower().str.startswith(label)
    lines = lines[~is_total]
    lines.insert(0, "branch", name["branch"])
    lines.insert(1, "file", path.name)
    lines.insert(2, "month", name["month"])
    return lines, int(is_total.sum()), name["branch"], name["month"]


def to_date(value, date_format):
    """A real Excel date as it is; a text date only with its branch's format, never guessed."""
    if isinstance(value, datetime):
        return pd.Timestamp(value)
    if date_format is None:
        return pd.NaT
    try:
        return pd.to_datetime(str(value).strip(), format=date_format)
    except ValueError:
        return pd.NaT


def clean(lines, cfg, value_map):
    """Fix every value to one standard. A value that cannot be read becomes empty."""
    df = lines.copy()
    for col in [c for c in cfg["columns"] if c not in NUMBERS + ["order_date"]]:
        df[col] = (df[col].astype("string").str.strip().str.replace(r"\s+", " ", regex=True)
                   .replace("", pd.NA))
    for col, spellings in value_map.groupby("column"):
        lookup = dict(zip(spellings["as_sent"].str.strip().str.lower(), spellings["standard"]))
        df[col] = df[col].str.lower().map(lookup).fillna(df[col])
    df["order_date"] = [to_date(v, cfg["date_formats"].get(b)) for v, b in zip(df["order_date"], df["branch"])]
    df["quantity"] = pd.to_numeric(df["quantity"].astype("string").str.extract(r"(-?\d+)")[0])
    for col in ["sales", "profit"]:  # keep digits, the minus sign and the decimal point
        df[col] = pd.to_numeric(df[col].astype("string").str.replace(r"[^0-9.\-]", "", regex=True),
                                errors="coerce")
    return df


def check(df, cfg):
    """The reason each row is set aside, or "" when it passes every rule."""
    min_quantity = cfg["rules"]["min_quantity"]
    reason = np.select(
        [df["order_id"].isna(),
         df["order_date"].isna(),
         df["order_date"].dt.strftime("%Y-%m") != df["month"],
         ~(df["quantity"] >= min_quantity),
         df["sales"].isna() | df["profit"].isna()],
        ["missing order id", "date not readable", "date outside the file's month",
         f"quantity missing or below {min_quantity}", "amount not a number"],
        default="")
    passed = reason == ""
    duplicate = passed & df[list(cfg["columns"]) + ["branch"]].duplicated(keep="first")
    return np.where(duplicate, "duplicate of an earlier row", reason)


def write_report(sales, aside, files, excel_file):
    summary = files.groupby("branch")[["rows_read", "clean_rows", "set_aside_rows"]].sum()
    summary.insert(0, "files", files.groupby("branch").size())
    summary["sales"] = sales.groupby("branch")["sales"].sum().round(2)
    summary["profit"] = sales.groupby("branch")["profit"].sum().round(2)
    summary = summary.fillna(0)
    summary.loc["All branches"] = summary.sum().round(2)
    weekly = (sales.assign(week_start=sales["order_date"].dt.to_period("W-SUN").dt.start_time)
              .pivot_table(index="week_start", columns="branch", values="sales", aggfunc="sum",
                           fill_value=0).round(2))
    weekly["All branches"] = weekly.sum(axis=1).round(2)
    with pd.ExcelWriter(OUT / excel_file, engine="openpyxl",
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
    cfg = load_config()
    input_dir = cfg["input_dir"]
    headers = {header_key(h): std for std, names in cfg["columns"].items() for h in names}

    map_path = input_dir / cfg["inputs"]["value_map"]
    if not map_path.exists():
        raise SystemExit(f"missing data/input/{map_path.name} (inputs.value_map in config/client.yaml)")
    value_map = pd.read_csv(map_path, dtype=str)
    missing = {"column", "as_sent", "standard"} - set(value_map.columns)
    if missing:
        stop(map_path, f"missing column(s): {', '.join(sorted(missing))}")
    unknown = set(value_map["column"]) - set(cfg["columns"])
    if unknown:
        stop(map_path, f"names column(s) that are not in columns: {', '.join(sorted(unknown))}")

    paths = sorted(p for p in input_dir.glob("*.xlsx") if not p.name.startswith("~$"))
    if not paths:
        raise SystemExit("no branch files (*.xlsx) in data/input/")
    read = [read_branch_file(p, cfg, headers) for p in paths]
    lines = pd.concat([r[0] for r in read], ignore_index=True)
    unknown = set(cfg["date_formats"]) - set(r[2] for r in read)
    if unknown:
        raise SystemExit(f"config/client.yaml: date_formats names a branch with no file: {', '.join(sorted(unknown))}")

    df = clean(lines, cfg, value_map)
    df["reason"] = check(df, cfg)
    ok = df["reason"] == ""
    sales = df.loc[ok, ["branch", "file"] + list(cfg["columns"])]
    aside = lines.loc[~ok, ["file", "excel_row", "branch"] + list(cfg["columns"])]
    aside[list(cfg["columns"])] = aside[list(cfg["columns"])].astype("string")  # exactly as the branch sent them
    aside.insert(3, "reason", df.loc[~ok, "reason"])

    names = [p.name for p in paths]
    files = pd.DataFrame({"file": names, "branch": [r[2] for r in read], "month": [r[3] for r in read],
                          "rows_read": lines.groupby("file").size().reindex(names, fill_value=0).values,
                          "totals_rows_skipped": [r[1] for r in read]})
    files["clean_rows"] = files["file"].map(sales.groupby("file").size()).fillna(0).astype(int)
    files["set_aside_rows"] = files["file"].map(aside.groupby("file").size()).fillna(0).astype(int)
    assert (files["rows_read"] == files["clean_rows"] + files["set_aside_rows"]).all()

    OUT.mkdir(exist_ok=True)
    sales.to_csv(OUT / "clean_sales.csv", index=False, date_format="%Y-%m-%d")
    aside.to_csv(OUT / "set_aside_rows.csv", index=False)
    files.to_csv(OUT / "file_log.csv", index=False)
    write_report(sales, aside, files, cfg["report"]["excel_file"])

    print(f"{len(paths)} files, {len(lines)} rows read: {len(sales)} clean, {len(aside)} set aside")
    print(aside["reason"].value_counts().to_string())
    print(f"Report rebuilt in {time.perf_counter() - started:.1f} seconds: output/{cfg['report']['excel_file']}")


if __name__ == "__main__":
    main()
