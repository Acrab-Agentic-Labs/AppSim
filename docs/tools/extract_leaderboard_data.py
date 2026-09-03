#!/usr/bin/env python3
"""Extract task-level correctness for each model from AppSim Valid-Model-Results
and emit a self-contained JS data file for the GitHub Pages leaderboard heatmap.

The output (static/data/leaderboard_data.js) sets window.APPSIM_LEADERBOARD and
contains NO machine paths or repo-relative dependencies, so it is safe to deploy.

Each task carries:
  app   - display label
  i     - local index within the app (0-based)
  ins   - instruction
  steps - human-annotated reference step count
  lang  - "zh" or "en"
  cats  - list of numerical-reasoning subtypes (count/calculate/compare_select/
          threshold_filter); empty list means not a numerical-reasoning task.

Status is BINARY: 1 = correct, 0 = wrong (a missing result row counts as wrong).

Run from anywhere; paths to the AppSim repo are configured below.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# --- Configure source locations (the private AppSim repo, NOT deployed) ---
APPSIM_SRC = Path("/root/AppSim/AppSim/src")
RESULT_DIR = Path("/root/AppSim/AppSim/scripts/results/Valid-Model-Results")
GRID_TOOL = Path("/root/AppSim/T01-interactive_agent_task_grid")
NUM_TASK_JSON = Path("/root/AppSim/Stat-Results-For-Paper/num_task_acc/XXX.json")
OUTPUT = Path("/root/AppSim/appsim-github-page/static/data/leaderboard_data.js")

# Paper-accurate display names + ordering (by overall accuracy, descending),
# mapped from result folder name -> paper label.
MODEL_ORDER = [
    ("0519_m3a_claude_opus_4.7", "Claude-Opus-4.7"),
    ("0522_m3a_gemini_3pro",     "Gemini-3-Pro"),
    ("0522_m3a_gpt_5.5",         "GPT-5.5"),
    ("0519_m3a_gemini_3.1pro",   "Gemini-3.1-Pro"),
    ("0525_full_test_seed16",    "Doubao-Seed-1.6"),
    ("0515_m3a_gpt_5",           "GPT-5"),
    ("0518_doubao_seed18_full",  "Doubao-Seed-1.8"),
    ("0518_full_qwen_3.6_plus",  "Qwen-3.6-Plus"),
    ("0518_doubao_seed20_full",  "Doubao-Seed-2.0"),
    ("0519_full_gpt_5_4",        "GPT-5.4"),
    ("0517_qwen_3.6_flash",      "Qwen-3.6-Flash"),
    ("0523_m3a_claude_sonnet_4.6", "Claude-Sonnet-4.6"),
    ("0523_m3a_claude_haiku_4.5",  "Claude-Haiku-4.5"),
    ("0515_m3a_claude_sonnet_4.5", "Claude-Sonnet-4.5"),
    ("0516_m3a_gemini_2.5_pro",  "Gemini-2.5-Pro"),
]

# ZH/EN app groups, keyed by catalog enum name (from paper Table: acc-by-language).
ZH_APPS = {"BILIBILI", "CTRIP", "ELEME", "GAODE", "MUSIC", "MYJD", "RED_NOTE", "TENCENT_MEETING", "WECHAT"}
EN_APPS = {"AMAZON", "BOOKING", "INSTAGRAM", "SPOTIFY", "UBEREATS", "WHATSAPP", "YOUTUBE", "ZOOM"}

# num_task_acc/XXX.json app key -> catalog enum name
JSON2ENUM = {
    "amazon": "AMAZON", "bilibili": "BILIBILI", "booking": "BOOKING", "ctrip": "CTRIP",
    "eleme": "ELEME", "gaode": "GAODE", "instagram": "INSTAGRAM", "jd": "MYJD",
    "music": "MUSIC", "rednote": "RED_NOTE", "spotify": "SPOTIFY",
    "tencentmeeting": "TENCENT_MEETING", "ubereats": "UBEREATS", "wechat": "WECHAT",
    "whatsapp": "WHATSAPP", "youtube": "YOUTUBE", "zoom": "ZOOM",
}

# binary status: success -> 1, everything else (failure or missing) -> 0
def status_code(status: str) -> int:
    return 1 if status == "success" else 0


def load_numerical_categories():
    """Return {(enum_name, local_index): [categories]} and the category definitions."""
    data = json.loads(NUM_TASK_JSON.read_text(encoding="utf-8"))
    mapping: dict[tuple[str, int], list[str]] = {}
    for jkey, info in data["apps"].items():
        enum_name = JSON2ENUM[jkey]
        for task in info["tasks"]:
            local_index = task["id"] - 1  # json id is 1-based; catalog is 0-based
            mapping[(enum_name, local_index)] = task["categories"]
    return mapping, data["category_definitions"]


def main() -> None:
    sys.path.insert(0, str(APPSIM_SRC))
    sys.path.insert(0, str(GRID_TOOL))
    import build_interactive_grid as B  # reuse the validated parser

    app_map = B.import_tasks(APPSIM_SRC)
    catalog, spans, id_lookup, instr_lookup = B.build_task_catalog(app_map)

    num_cats, cat_defs = load_numerical_categories()

    tasks = []
    for m in catalog:
        if m.app_key in ZH_APPS:
            lang = "zh"
        elif m.app_key in EN_APPS:
            lang = "en"
        else:
            lang = "?"
        tasks.append({
            "app": m.app_label,
            "i": m.local_index,
            "ins": m.instruction,
            "steps": m.human_steps,
            "lang": lang,
            "cats": num_cats.get((m.app_key, m.local_index), []),
        })

    # sanity: numerical-reasoning task count must match the paper (183)
    num_count = sum(1 for t in tasks if t["cats"])
    if num_count != 183:
        print(f"WARNING: numerical-reasoning task count = {num_count}, expected 183", file=sys.stderr)

    app_spans = [
        {"label": s["label"], "start": int(s["start"]), "end": int(s["end"]), "count": int(s["count"])}
        for s in spans
    ]

    folder_to_dir = {d.name: d for d in B.discover_agent_dirs(RESULT_DIR, None)}

    models = []
    for folder, label in MODEL_ORDER:
        if folder not in folder_to_dir:
            raise SystemExit(f"Missing result folder: {folder}")
        run = B.load_agent_run(folder_to_dir[folder], catalog, id_lookup, instr_lookup)
        statuses = [status_code(r.status) for r in run.results]
        # accuracy uses success/total exactly as the paper (missing counts as wrong)
        correct = sum(statuses)
        models.append({
            "name": label,
            "correct": correct,
            "wrong": len(catalog) - correct,
            "acc": round(correct / len(catalog) * 1000) / 10,
            "s": statuses,
        })

    payload = {
        "totalTasks": len(catalog),
        "categoryDefs": cat_defs,
        "tasks": tasks,
        "appSpans": app_spans,
        "models": models,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    data_json = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    OUTPUT.write_text("window.APPSIM_LEADERBOARD = " + data_json + ";\n", encoding="utf-8")

    print(f"Wrote {OUTPUT} ({OUTPUT.stat().st_size/1024:.0f} KB)")
    print(f"{len(catalog)} tasks ({num_count} numerical-reasoning), {len(models)} models")
    zh = sum(1 for t in tasks if t["lang"] == "zh")
    en = sum(1 for t in tasks if t["lang"] == "en")
    print(f"  ZH tasks={zh}  EN tasks={en}")
    from collections import Counter
    cc = Counter(c for t in tasks for c in t["cats"])
    print(f"  category counts: {dict(cc)}")
    for m in models:
        print(f"  {m['acc']:5.1f}%  {m['correct']:3d}/{m['wrong']:3d}  {m['name']}")


if __name__ == "__main__":
    main()
