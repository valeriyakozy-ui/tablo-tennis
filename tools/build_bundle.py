"""Собирает data/tablo.json из документов, выгруженных из базы страницы Claude.

Запуск: python3 tools/build_bundle.py <папка_выгрузки>
В папке ожидаются season/2026.json, season/2026-wta.json и draws/*.json
(так их сохраняет ArtifactData с out_dir).
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
    assert len(s.get("tournaments", [])) > 40, f"в календаре {tour} подозрительно мало турниров"
updated = max(s.get("updatedAt", "") for s in seasons.values())
out = os.path.join(root, "data", "tablo.json")
json.dump({"updatedAt": updated, "seasons": seasons, "draws": draws}, open(out, "w"), ensure_ascii=False, separators=(",", ":"))
print("ok:", out, "| сеток:", len(draws), "| обновлено:", updated)
