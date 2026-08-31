from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dyson_one.critic import run_critic
from dyson_one.ingest import enrich_specs, fetch_close_approaches, fetch_nhats
from dyson_one.ledger import write_snapshot
from dyson_one.score import score_body


def merge_rows(nhats: list[dict], approaches: list[dict]) -> list[dict]:
    by_des: dict[str, dict] = defaultdict(dict)
    for row in nhats + approaches:
        des = (row.get("des") or "").strip()
        if not des:
            continue
        by_des[des].update({k: v for k, v in row.items() if v is not None})
        by_des[des]["des"] = des
    return list(by_des.values())


def run(out_dir: Path, *, limit: int, lookup: int, critic: bool) -> None:
    today = datetime.now(timezone.utc).date()
    nhats = fetch_nhats(limit=limit)
    approaches = fetch_close_approaches(
        date_min=today.isoformat(),
        date_max=(today + timedelta(days=1100)).isoformat(),
        limit=limit,
    )
    rows = merge_rows(nhats, approaches)
    enrich_specs(rows, max_lookup=lookup)

    scores = []
    for row in rows:
        diam = row.get("diameter_km")
        if diam is None and row.get("min_size_m"):
            diam = float(row["min_size_m"]) / 1000.0
        scores.append(
            score_body(
                designation=row["des"],
                name=row.get("name") or row.get("fullname"),
                spec=row.get("spec"),
                h_mag=row.get("h"),
                diameter_km=diam,
                dv_kms=row.get("dv_kms"),
                next_approach=row.get("next_approach"),
                approach_au=row.get("approach_au"),
            )
        )
    write_snapshot(out_dir, scores)
    if critic:
        run_critic(out_dir)


def main() -> None:
    p = argparse.ArgumentParser(prog="dyson-one")
    p.add_argument("--out", type=Path, default=Path("data"))
    p.add_argument("--limit", type=int, default=60)
    p.add_argument("--lookup", type=int, default=12)
    p.add_argument("--critic", action="store_true")
    args = p.parse_args()
    run(args.out, limit=args.limit, lookup=args.lookup, critic=args.critic)


if __name__ == "__main__":
    main()
