from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dyson_one.critic import run_critic
from dyson_one.ingest import enrich_specs, fetch_close_approaches, fetch_nhats
from dyson_one.ledger import write_snapshot
from dyson_one.score import score_body
from dyson_one.world import (
    diff_worlds,
    explain_row,
    find_object,
    load_budgets,
    load_previous,
    load_snapshot,
)


def merge_rows(nhats: list[dict], approaches: list[dict]) -> list[dict]:
    by_des: dict[str, dict] = defaultdict(dict)
    for row in nhats + approaches:
        des = (row.get("des") or "").strip()
        if not des:
            continue
        by_des[des].update({k: v for k, v in row.items() if v is not None})
        by_des[des]["des"] = des
    return list(by_des.values())


def observe(out_dir: Path, *, limit: int | None, lookup: int | None, critic: bool) -> None:
    budgets = load_budgets()
    nhats_limit = limit if limit is not None else int(budgets.get("nhats_limit") or 60)
    cad_limit = int(budgets.get("cad_limit") or nhats_limit)
    lookups = lookup if lookup is not None else int(budgets.get("sbdb_lookups") or 12)
    today = datetime.now(timezone.utc).date()
    nhats = fetch_nhats(limit=nhats_limit)
    approaches = fetch_close_approaches(
        date_min=today.isoformat(),
        date_max=(today + timedelta(days=1100)).isoformat(),
        limit=cad_limit,
    )
    rows = merge_rows(nhats, approaches)
    enrich_specs(rows, max_lookup=lookups)

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
    write_snapshot(out_dir, scores, budgets=budgets)
    if critic:
        run_critic(out_dir)


def cmd_show(out_dir: Path) -> None:
    snap = load_snapshot(out_dir)
    brief = out_dir / "BRIEF.md"
    print(brief.read_text(encoding="utf-8") if brief.exists() else snap.get("hash"))


def cmd_explain(out_dir: Path, designation: str) -> None:
    snap = load_snapshot(out_dir)
    row = find_object(snap, designation)
    if row is None:
        raise SystemExit(f"not in snapshot: {designation}")
    print(explain_row(row), end="")


def cmd_gaps(out_dir: Path) -> None:
    snap = load_snapshot(out_dir)
    att = snap.get("attention") or {}
    print(f"snapshot {snap.get('hash')}  n={snap.get('count')}")
    for key in ("unknown_low_dv", "missing_approach", "high_water"):
        print(f"{key}:")
        for des in att.get(key) or []:
            print(f"  {des}")


def cmd_diff(out_dir: Path) -> None:
    print(diff_worlds(load_snapshot(out_dir), load_previous(out_dir)), end="")


def main() -> None:
    p = argparse.ArgumentParser(prog="dyson-one")
    p.add_argument("--out", type=Path, default=Path("data"))
    sub = p.add_subparsers(dest="cmd")

    obs = sub.add_parser("observe", help="refresh the world from JPL")
    obs.add_argument("--limit", type=int, default=None)
    obs.add_argument("--lookup", type=int, default=None)
    obs.add_argument("--critic", action="store_true")

    sub.add_parser("show", help="print BRIEF.md")
    ex = sub.add_parser("explain", help="expand optics for one designation")
    ex.add_argument("designation")
    sub.add_parser("gaps", help="print attention queues")
    sub.add_parser("diff", help="latest vs previous snapshot")

    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--lookup", type=int, default=None)
    p.add_argument("--critic", action="store_true")

    args = p.parse_args()
    out = args.out
    cmd = args.cmd
    if cmd in (None, "observe"):
        observe(
            out,
            limit=getattr(args, "limit", None),
            lookup=getattr(args, "lookup", None),
            critic=bool(getattr(args, "critic", False)),
        )
        return
    if cmd == "show":
        cmd_show(out)
        return
    if cmd == "explain":
        cmd_explain(out, args.designation)
        return
    if cmd == "gaps":
        cmd_gaps(out)
        return
    if cmd == "diff":
        cmd_diff(out)
        return
    raise SystemExit(f"unknown verb: {cmd}")


if __name__ == "__main__":
    main()
