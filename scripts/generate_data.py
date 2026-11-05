"""Generate synthetic historical stock events in data/ for local analysis.

Output is deterministic (fixed seed). Default size is about 300 MB.
Usage: python scripts/generate_data.py [--files N] [--rows-per-file N]
"""

import argparse
import csv
import random
from pathlib import Path

SKUS = ["KB-001", "MS-002", "MN-003", "MN-004", "HB-005", "CB-006"]
EVENTS = ["restock", "sale", "return", "adjustment"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--files", type=int, default=6)
    parser.add_argument("--rows-per-file", type=int, default=1_000_000)
    args = parser.parse_args()

    out_dir = Path(__file__).resolve().parent.parent / "data" / "events"
    out_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(20261105)

    for index in range(args.files):
        path = out_dir / f"events_{index:02d}.csv"
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["event_id", "timestamp", "sku", "event", "quantity", "warehouse", "note"])
            for row in range(args.rows_per_file):
                writer.writerow([
                    f"{index:02d}-{row:08d}",
                    f"2026-{rng.randint(1, 10):02d}-{rng.randint(1, 28):02d}T{rng.randint(0, 23):02d}:{rng.randint(0, 59):02d}:00Z",
                    rng.choice(SKUS),
                    rng.choice(EVENTS),
                    rng.randint(1, 50),
                    f"WH-{rng.randint(1, 9)}",
                    "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(8)),
                ])
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
