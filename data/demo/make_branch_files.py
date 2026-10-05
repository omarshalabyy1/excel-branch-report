"""Demo only: make the messy monthly branch files from the Superstore orders.

Run once; the files are committed. Each branch sends its own template, and a seeded
set of mistakes is planted and listed in data/input/planted_errors.csv, so run.py can be
tested against a known answer. A client's own files replace all of this (docs/new-client.md).
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).parents[2]
SOURCE = ROOT / "data" / "demo" / "source_orders.csv"
BRANCH_DIR = ROOT / "data" / "input"

BRANCH_STATES = {
    "west": ["Arizona", "California", "Colorado", "Idaho", "Montana", "Nevada", "New Mexico",
             "Oregon", "Utah", "Washington", "Wyoming"],
    "east": ["Connecticut", "Delaware", "District of Columbia", "Maine", "Maryland",
             "Massachusetts", "New Hampshire", "New Jersey", "New York", "Ohio", "Pennsylvania",
             "Rhode Island", "Vermont", "West Virginia"],
    "central": ["Illinois", "Indiana", "Iowa", "Kansas", "Michigan", "Minnesota", "Missouri",
                "Nebraska", "North Dakota", "Oklahoma", "South Dakota", "Texas", "Wisconsin"],
    "south": ["Alabama", "Arkansas", "Florida", "Georgia", "Kentucky", "Louisiana", "Mississippi",
              "North Carolina", "South Carolina", "Tennessee", "Virginia"],
}
COLUMNS = ["Order ID", "Order Date", "Ship Mode", "Segment", "City", "State", "Product ID",
           "Category", "Sub-Category", "Product Name", "Quantity", "Sales", "Profit"]
EAST_HEADERS = ["Order No", "Date", "Shipping", "Customer Type", "City", "State", "SKU",
                "Category", "Subcategory", "Item", "Qty", "Amount", "Profit"]
SOUTH_SHIP_MODES = {"Standard Class": "Std", "Second Class": "2nd class",
                    "First Class": "1st class", "Same Day": "same day"}
PROBLEMS = ["missing order id", "date not readable", "date outside the file's month",
            "quantity missing or below 1", "amount not a number"]

rng = np.random.default_rng(7)


def branch_date(day, branch):
    """A date the way this branch writes it."""
    if branch == "east":
        return day.strftime("%d/%m/%Y")
    if branch == "south":
        return day.strftime("%b %d %Y")
    return day


def branch_style(row, branch):
    """One order line in this branch's own template."""
    row = dict(row)
    row["Order Date"] = branch_date(row["Order Date"], branch)
    if branch == "central":
        for col in ["Segment", "Category", "Sub-Category"]:
            row[col] = row[col].upper()
        row["Product Name"] = row["Product Name"].replace(" ", "  ") + " "
        for col in ["Sales", "Profit"]:
            sign = "-" if row[col] < 0 else ""
            row[col] = f"{sign}${abs(row[col]):,.2f}"
    if branch == "south":
        row["Ship Mode"] = SOUTH_SHIP_MODES[row["Ship Mode"]]
        row["Quantity"] = f"{row['Quantity']} pcs"
    return row


def plant(row, problem, branch, day):
    """Break one value the way branch files really go wrong."""
    if problem == "missing order id":
        row["Order ID"] = None
    elif problem == "date not readable":
        row["Order Date"] = rng.choice(["TBC", None])
    elif problem == "date outside the file's month":
        row["Order Date"] = branch_date(day + pd.DateOffset(months=1), branch)
    elif problem == "quantity missing or below 1":
        quantity = rng.choice([0, -2])
        row["Quantity"] = f"{quantity} pcs" if branch == "south" else quantity
    elif problem == "amount not a number":
        row["Sales"] = rng.choice(["n/a", "TBC", None])
    return row


orders = pd.read_csv(SOURCE, parse_dates=["Order Date"])
orders = orders.drop_duplicates(subset=COLUMNS)  # the source repeats one order line exactly
orders["Sales"] = orders["Sales"].round(2)
orders["Profit"] = orders["Profit"].round(2)
orders["branch"] = orders["State"].map({s: b for b, states in BRANCH_STATES.items() for s in states})
assert orders["branch"].notna().all(), "a state has no branch"
orders["month"] = orders["Order Date"].dt.strftime("%Y-%m")

BRANCH_DIR.mkdir(parents=True, exist_ok=True)
planted = []
for (branch, month), group in orders.groupby(["branch", "month"]):
    file = f"{branch.title()}_{month}.xlsx"
    start_row = 3 if branch == "west" else 0  # west puts a title block above the table
    rows = []
    for _, source_row in group.sort_values("Order Date")[COLUMNS].iterrows():
        row = branch_style(source_row, branch)
        roll = rng.random()
        if roll < 0.015:
            problem = PROBLEMS[rng.integers(len(PROBLEMS))]
            row = plant(row, problem, branch, source_row["Order Date"])
            planted.append((file, start_row + 2 + len(rows), problem))
        rows.append(row)
        if 0.015 <= roll < 0.025:  # the same line pasted twice
            planted.append((file, start_row + 2 + len(rows), "duplicate of an earlier row"))
            rows.append(dict(row))

    table = pd.DataFrame(rows, columns=COLUMNS)
    if branch == "west":
        totals = {"Order ID": "TOTAL"}
        for col in ["Quantity", "Sales", "Profit"]:
            totals[col] = round(pd.to_numeric(table[col], errors="coerce").sum(), 2)
        table = pd.concat([table, pd.DataFrame([totals])], ignore_index=True)
    if branch == "east":
        table.columns = EAST_HEADERS
    if branch == "central":
        table.columns = [c.lower().replace(" ", "_").replace("-", "_") for c in COLUMNS]

    with pd.ExcelWriter(BRANCH_DIR / file, engine="openpyxl") as writer:
        table.to_excel(writer, index=False, startrow=start_row, sheet_name="Sales")
        if branch == "west":
            sheet = writer.sheets["Sales"]
            sheet["A1"] = "West branch - monthly sales"
            sheet["A2"] = f"Month: {pd.Timestamp(month).strftime('%B %Y')}"

pd.DataFrame(planted, columns=["file", "excel_row", "problem"]).to_csv(
    BRANCH_DIR / "planted_errors.csv", index=False)
print(f"{orders.groupby(['branch', 'month']).ngroups} files, {len(orders)} source rows, "
      f"{len(planted)} planted problems")
