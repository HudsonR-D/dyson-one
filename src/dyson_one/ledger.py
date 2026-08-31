"""Append-only ledger + snapshot writers."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dyson_one.score import Score


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def snapshot_hash(rows: list[dict[str, Any]]) -> str:
    blob = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:16]


def write_snapshot(out_dir: Path, scores: list[Score], generated_at: str | None = None) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = [s.to_dict() for s in scores]
    rows.sort(key=lambda r: (-r["water_score"], -r["pgm_score"], r["designation"]))
    payload = {
        "project": "dyson-one",
        "charter": "observe-and-rank",
        "generated_at": generated_at or utc_now(),
        "count": len(rows),
        "hash": snapshot_hash(rows),
        "objects": rows,
    }
    (out_dir / "latest.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (out_dir / "BRIEF.md").write_text(render_brief(payload), encoding="utf-8")
    log_path = out_dir / "ledger.jsonl"
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"generated_at": payload["generated_at"], "hash": payload["hash"], "count": payload["count"]}) + "\n")
    return payload


def render_brief(payload: dict[str, Any]) -> str:
    lines = [
        f"# Dyson One brief — {payload['generated_at']}",
        "",
        f"Objects scored: **{payload['count']}**. Snapshot `{payload['hash']}`.",
        "",
        "Scores are research ranks, not mine plans. `earth_spot_usd_vanity` is a toy number.",
        "",
        "| Rank | Designation | Family | Δv km/s | Next approach | Water | PGM | Conf |",
        "| ---: | --- | --- | ---: | --- | ---: | ---: | ---: |",
    ]
    for i, row in enumerate(payload["objects"][:25], start=1):
        lines.append(
            "| {i} | {des} | {fam} | {dv} | {ca} | {w} | {p} | {c} |".format(
                i=i,
                des=row["designation"],
                fam=row["spec_family"],
                dv=row["dv_kms"] if row["dv_kms"] is not None else "—",
                ca=row["next_approach"] or "—",
                w=row["water_score"],
                p=row["pgm_score"],
                c=row["confidence"],
            )
        )
    lines.append("")
    lines.append("See `CHARTER.md`. Observe and rank. No actuators.")
    lines.append("")
    return "\n".join(lines)
