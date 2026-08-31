"""Append-only ledger + snapshot writers."""

from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dyson_one.score import Score
from dyson_one.world import SCHEMA_VERSION, CHARTER_ID, attention, load_budgets


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def snapshot_hash(rows: list[dict[str, Any]]) -> str:
    blob = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:16]


def write_snapshot(
    out_dir: Path,
    scores: list[Score],
    generated_at: str | None = None,
    budgets: dict[str, Any] | None = None,
) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    latest = out_dir / "latest.json"
    if latest.exists():
        shutil.copyfile(latest, out_dir / "previous.json")

    rows = [s.to_dict() for s in scores]
    rows.sort(key=lambda r: (-r["water_score"], -r["pgm_score"], r["designation"]))
    used = budgets or load_budgets()
    n = int(used.get("attention_n") or 8)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "project": "dyson-one",
        "charter": CHARTER_ID,
        "generated_at": generated_at or utc_now(),
        "count": len(rows),
        "hash": snapshot_hash(rows),
        "budgets": used,
        "attention": attention(rows, n=n),
        "objects": rows,
    }
    latest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (out_dir / "BRIEF.md").write_text(render_brief(payload), encoding="utf-8")
    log_path = out_dir / "ledger.jsonl"
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(
            json.dumps(
                {
                    "generated_at": payload["generated_at"],
                    "hash": payload["hash"],
                    "count": payload["count"],
                    "schema_version": SCHEMA_VERSION,
                }
            )
            + "\n"
        )
    return payload


def render_brief(payload: dict[str, Any]) -> str:
    att = payload.get("attention") or {}
    top_n = int((payload.get("budgets") or {}).get("top_n_brief") or 25)
    lines = [
        f"# Dyson One brief — {payload['generated_at']}",
        "",
        f"schema v{payload.get('schema_version', 1)} · objects **{payload['count']}** · `{payload['hash']}`",
        "",
        "Scores are research ranks, not mine plans. `earth_spot_usd_vanity` is a toy number.",
        "",
        "## Attention (spend the next lookup here)",
        "",
        f"- unknown_low_dv: {', '.join(att.get('unknown_low_dv') or []) or '—'}",
        f"- missing_approach: {', '.join(att.get('missing_approach') or []) or '—'}",
        f"- high_water: {', '.join(att.get('high_water') or []) or '—'}",
        "",
        "## Rank",
        "",
        "| Rank | Designation | Family | dv km/s | Next approach | Water | PGM | Conf |",
        "| ---: | --- | --- | ---: | --- | ---: | ---: | ---: |",
    ]
    for i, row in enumerate(payload["objects"][:top_n], start=1):
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
    lines.append("Start at `AGENT.md`. Constitution in `CHARTER.md`. No actuators.")
    lines.append("")
    return "\n".join(lines)
