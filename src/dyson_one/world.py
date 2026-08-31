"""L3/L4 world-model helpers. Disk only. No network. No tokens."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
CHARTER_ID = "observe-and-rank"


def load_budgets(root: Path | None = None) -> dict[str, Any]:
    path = (root or Path.cwd()) / "config" / "budgets.json"
    if not path.exists():
        return {
            "nhats_limit": 60,
            "cad_limit": 60,
            "sbdb_lookups": 12,
            "attention_n": 8,
            "top_n_brief": 25,
            "critic_tokens_max": 0,
        }
    return json.loads(path.read_text(encoding="utf-8"))


def load_snapshot(out_dir: Path) -> dict[str, Any]:
    path = out_dir / "latest.json"
    if not path.exists():
        raise FileNotFoundError(f"no world at {path}; run observe")
    return json.loads(path.read_text(encoding="utf-8"))


def load_previous(out_dir: Path) -> dict[str, Any] | None:
    path = out_dir / "previous.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def find_object(snapshot: dict[str, Any], designation: str) -> dict[str, Any] | None:
    needle = designation.strip().lower()
    for row in snapshot.get("objects") or []:
        des = str(row.get("designation") or "")
        name = str(row.get("name") or "")
        if des.lower() == needle or needle in name.lower():
            return row
    return None


def attention(objects: list[dict[str, Any]], *, n: int = 8) -> dict[str, list[str]]:
    unknown = [o for o in objects if o.get("spec_family") == "unknown"]
    unknown.sort(key=lambda o: (o.get("dv_kms") is None, o.get("dv_kms") or 99, o.get("designation")))
    missing = [o for o in objects if not o.get("next_approach")]
    missing.sort(key=lambda o: o.get("designation") or "")
    high = sorted(objects, key=lambda o: (-o.get("water_score", 0), o.get("designation") or ""))
    return {
        "unknown_low_dv": [o["designation"] for o in unknown[:n]],
        "missing_approach": [o["designation"] for o in missing[:n]],
        "high_water": [o["designation"] for o in high[:n]],
    }


def explain_row(row: dict[str, Any]) -> str:
    notes = row.get("notes") or []
    lines = [
        f"# explain {row.get('designation')}",
        "",
        f"family: {row.get('spec_family')} (spec={row.get('spec') or 'none'})",
        f"diameter_km: {row.get('diameter_km')}",
        f"dv_kms: {row.get('dv_kms')}",
        f"water_score: {row.get('water_score')}",
        f"pgm_score: {row.get('pgm_score')}",
        f"confidence: {row.get('confidence')}",
        f"next_approach: {row.get('next_approach') or '—'}",
        "",
        "optics: water_w[family] * diameter_km^1.5 / (dv_kms + 0.5)",
        "unknown family => confidence <= 0.45; do not treat scores as treasure.",
        "earth_spot_usd_vanity is a toy. Not NPV.",
        "",
        "notes:",
    ]
    for note in notes:
        lines.append(f"- {note}")
    if not notes:
        lines.append("- (none)")
    lines.append("")
    return "\n".join(lines)


def diff_worlds(current: dict[str, Any], previous: dict[str, Any] | None) -> str:
    if previous is None:
        return "no previous.json; diff needs two observes\n"
    cur = {o["designation"]: o for o in current.get("objects") or []}
    prev = {o["designation"]: o for o in previous.get("objects") or []}
    added = sorted(set(cur) - set(prev))
    removed = sorted(set(prev) - set(cur))
    lines = [
        f"# diff {previous.get('hash')} -> {current.get('hash')}",
        "",
        f"count {previous.get('count')} -> {current.get('count')}",
        f"added ({len(added)}): " + ", ".join(added[:20]),
        f"removed ({len(removed)}): " + ", ".join(removed[:20]),
        "",
        "water_score moves (abs >= 0.001):",
    ]
    moved = []
    for des in sorted(set(cur) & set(prev)):
        delta = (cur[des].get("water_score") or 0) - (prev[des].get("water_score") or 0)
        if abs(delta) >= 0.001:
            moved.append((abs(delta), des, delta))
    moved.sort(reverse=True)
    if not moved:
        lines.append("- none")
    for _, des, delta in moved[:15]:
        lines.append(f"- {des}: {delta:+.6f}")
    lines.append("")
    return "\n".join(lines)
