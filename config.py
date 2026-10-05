"""The one place client values come from: config/client.yaml."""

from pathlib import Path

import yaml

ROOT = Path(__file__).parent
REQUIRED = [
    "client.name", "client.currency",
    "inputs.file_name", "inputs.sheet", "inputs.totals_row_label", "inputs.value_map",
    "columns", "date_formats", "rules.min_quantity",
    "report.title", "report.excel_file",
    "report.colours.data", "report.colours.text", "report.colours.muted",
    "report.colours.page", "report.colours.line", "report.colours.danger",
]
# The standard columns the rules, the notebook and the Power BI report need in every file.
REQUIRED_COLUMNS = ["order_id", "order_date", "quantity", "sales", "profit", "category"]


def load_config():
    try:
        cfg = yaml.safe_load((ROOT / "config" / "client.yaml").read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        line = error.problem_mark.line + 1 if getattr(error, "problem_mark", None) else "?"
        raise SystemExit(f"config/client.yaml is not valid YAML near line {line} (quote a value with # or :)")
    for key in REQUIRED:
        node = cfg
        for part in key.split("."):
            if not isinstance(node, dict) or part not in node:
                raise SystemExit(f"config/client.yaml is missing {key}")
            node = node[part]
    missing = [c for c in REQUIRED_COLUMNS if c not in cfg["columns"]]
    if missing:
        raise SystemExit(f"config/client.yaml is missing columns.{', columns.'.join(missing)}")

    cfg["date_formats"] = cfg["date_formats"] or {}
    cfg["input_dir"] = ROOT / "data" / "input"
    return cfg
