"""
build.py — Scans trips/*.json and regenerates trips/index.json manifest.
Run locally or via GitHub Actions whenever a new trip file is added.
"""
import json
import glob
import os
import sys

TRIPS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trips")
INDEX_FILE = os.path.join(TRIPS_DIR, "index.json")

def build():
    pattern = os.path.join(TRIPS_DIR, "*.json")
    files = sorted(glob.glob(pattern))

    manifest = []
    for f in files:
        if os.path.basename(f) == "index.json":
            continue
        try:
            with open(f, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            manifest.append({
                "id":        data["id"],
                "title":     data["title"],
                "emoji":     data.get("emoji", "✈️"),
                "dateRange": data.get("dateRange", ""),
                "file":      os.path.basename(f),
            })
            print(f"  + {os.path.basename(f)}")
        except Exception as e:
            print(f"  ! Skipping {os.path.basename(f)}: {e}", file=sys.stderr)

    with open(INDEX_FILE, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    print(f"\nWrote {len(manifest)} trip(s) to trips/index.json")

if __name__ == "__main__":
    build()
