"""Read-only JPL SSD / CNEOS pulls. Cache and be polite."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

SSD = "https://ssd-api.jpl.nasa.gov"
UA = "DysonOne/0.1 (+https://github.com/HudsonR-D/dyson-one; research ledger)"


def _get(url: str, timeout: float = 45.0) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_nhats(
    *,
    dv: int = 8,
    dur: int = 450,
    stay: int = 8,
    launch: str = "2020-2045",
    h: int = 26,
    limit: int = 80,
) -> list[dict[str, Any]]:
    q = urllib.parse.urlencode(
        {"dv": dv, "dur": dur, "stay": stay, "launch": launch, "h": h}
    )
    payload = _get(f"{SSD}/nhats.api?{q}")
    rows = payload.get("data") or []
    out: list[dict[str, Any]] = []
    for raw in rows[:limit]:
        min_dv = raw.get("min_dv") or {}
        out.append(
            {
                "des": (raw.get("des") or "").strip(),
                "fullname": (raw.get("fullname") or "").strip(),
                "h": _f(raw.get("h")),
                "dv_kms": _f(min_dv.get("dv")),
                "min_size_m": _f(raw.get("min_size")),
                "max_size_m": _f(raw.get("max_size")),
                "source": "nhats",
            }
        )
    return out


def fetch_close_approaches(
    *,
    date_min: str,
    date_max: str,
    dist_max_au: float = 0.05,
    limit: int = 40,
) -> list[dict[str, Any]]:
    q = urllib.parse.urlencode(
        {
            "date-min": date_min,
            "date-max": date_max,
            "dist-max": dist_max_au,
            "sort": "date",
            "limit": limit,
        }
    )
    payload = _get(f"{SSD}/cad.api?{q}")
    fields = payload.get("fields") or []
    rows = payload.get("data") or []
    out: list[dict[str, Any]] = []
    for row in rows:
        rec = dict(zip(fields, row))
        out.append(
            {
                "des": rec.get("des"),
                "next_approach": rec.get("cd"),
                "approach_au": _f(rec.get("dist")),
                "h": _f(rec.get("h")),
                "source": "cad",
            }
        )
    return out


def fetch_sbdb(des: str) -> dict[str, Any]:
    q = urllib.parse.urlencode({"sstr": des, "phys-par": 1})
    payload = _get(f"{SSD}/sbdb.api?{q}")
    obj = payload.get("object") or {}
    phys = payload.get("phys_par") or []
    params = {p.get("name"): p.get("value") for p in phys if isinstance(p, dict)}
    return {
        "des": obj.get("des") or des,
        "name": obj.get("shortname") or obj.get("fullname"),
        "spec": params.get("spec_B") or params.get("spec_T"),
        "diameter_km": _f(params.get("diameter")),
        "h": _f(params.get("H")),
        "pha": obj.get("pha"),
    }


def enrich_specs(rows: list[dict[str, Any]], *, max_lookup: int = 15, pause_s: float = 0.25) -> None:
    """Best-effort spectral/diameter fill. Failures stay unknown."""
    seen: set[str] = set()
    lookups = 0
    for row in rows:
        des = row.get("des")
        if not des or des in seen or lookups >= max_lookup:
            continue
        seen.add(des)
        try:
            extra = fetch_sbdb(des)
            lookups += 1
            time.sleep(pause_s)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError):
            continue
        if extra.get("spec"):
            row["spec"] = extra["spec"]
        if extra.get("diameter_km"):
            row["diameter_km"] = extra["diameter_km"]
        if extra.get("name"):
            row["name"] = extra["name"]
        if extra.get("h") and not row.get("h"):
            row["h"] = extra["h"]


def _f(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
