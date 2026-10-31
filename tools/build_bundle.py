"""Rebuilds data/tablo.json from documents exported from the Claude page database.

Usage: python3 tools/build_bundle.py <export_folder>
The folder must contain season/2026.json, season/2026-wta.json, draws/*.json, rankings/*.json and results/*.json
(the layout ArtifactData uses with out_dir).
"""
import json, os, sys

src = sys.argv[1]
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
seasons = {
    "atp": json.load(open(os.path.join(src, "season", "2026.json"))),
    "wta": json.load(open(os.path.join(src, "season", "2026-wta.json"))),
}
draws = {}
ddir = os.path.join(src, "draws")
for f in sorted(os.listdir(ddir)):
    if f.endswith(".json"):
        draws[f[:-5]] = json.load(open(os.path.join(ddir, f)))
for tour, s in seasons.items():
    assert len(s.get("tournaments", [])) > 40, f"the {tour} calendar has suspiciously few tournaments"
rankings = {}
rdir = os.path.join(src, "rankings")
if os.path.isdir(rdir):
    for f in sorted(os.listdir(rdir)):
        if f.endswith(".json"):
            rankings[f[:-5]] = json.load(open(os.path.join(rdir, f)))
results = {}
xdir = os.path.join(src, "results")
if os.path.isdir(xdir):
    for f in sorted(os.listdir(xdir)):
        if f.endswith(".json"):
            results[f[:-5]] = json.load(open(os.path.join(xdir, f))).get("players", {})
updated = max(s.get("updatedAt", "") for s in seasons.values())
out = os.path.join(root, "data", "tablo.json")
json.dump({"updatedAt": updated, "seasons": seasons, "draws": draws, "rankings": rankings, "results": results}, open(out, "w"), ensure_ascii=False, separators=(",", ":"))
print("ok:", out, "| draws:", len(draws), "| updated:", updated)
