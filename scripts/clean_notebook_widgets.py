import json
import sys
from pathlib import Path

WIDGET_VIEW_MIME = "application/vnd.jupyter.widget-view+json"
WIDGET_STATE_MIME = "application/vnd.jupyter.widget-state+json"

def clean_notebook(path):
    with path.open("r", encoding="utf-8") as f:
        nb = json.load(f)
        
    meta = nb.setdefault("metadata", {})
    if "widgets" in meta:
        del meta["widgets"]
    if "colab" in meta:
        del meta["colab"]

    for cell in nb.get("cells", []):
        cell_meta = cell.setdefault("metadata", {})
        if "widgets" in cell_meta:
            del cell_meta["widgets"]

        if cell.get("outputs"):
            kept = []
            for out in cell["outputs"]:
                data = out.get("data", {}) or {}
                if WIDGET_VIEW_MIME in data or WIDGET_STATE_MIME in data:
                    continue
                kept.append(out)
            cell["outputs"] = kept

    with path.open("w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        f.write("\n")

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        clean_notebook(Path(arg))
    print("Notebooks limpos com sucesso.")
