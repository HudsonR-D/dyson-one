"""Deterministic scores. No LLM in this module."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

WATER_TOKENS = {"C", "B", "G", "F", "CG", "CH", "CB", "Cgh", "Cg", "Ctype"}
METAL_TOKENS = {"M", "X", "XE", "XC", "Xk", "Xn"}
STONY_TOKENS = {"S", "SQ", "SR", "SV", "Q", "V", "A", "K", "L", "O", "R"}


@dataclass
class Score:
    designation: str
    name: str | None
    spec: str | None
    spec_family: str
    h_mag: float | None
    diameter_km: float | None
    dv_kms: float | None
    next_approach: str | None
    approach_au: float | None
    water_score: float
    pgm_score: float
    confidence: float
    earth_spot_usd_vanity: float
    notes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _norm_spec(raw: str | None) -> str | None:
    if not raw:
        return None
    return raw.strip().replace("-", "").replace(" ", "")


def family(spec: str | None) -> str:
    token = _norm_spec(spec)
    if not token:
        return "unknown"
    upper = token.upper()
    compact = token
    if upper in {t.upper() for t in WATER_TOKENS} or upper.startswith("C") or upper.startswith("B"):
        if upper.startswith("S") or upper.startswith("Q"):
            return "stony"
        return "water"
    if upper in {t.upper() for t in METAL_TOKENS} or compact in METAL_TOKENS:
        return "metal"
    if upper in {t.upper() for t in STONY_TOKENS} or upper.startswith("S") or upper.startswith("Q"):
        return "stony"
    if upper.startswith("X") or upper.startswith("M"):
        return "metal"
    return "unknown"


def diameter_from_h(h_mag: float | None, albedo: float) -> float | None:
    if h_mag is None:
        return None
    return (1329.0 / (albedo**0.5)) * (10 ** (-0.2 * h_mag))


def albedo_for(fam: str) -> float:
    return {"water": 0.06, "metal": 0.15, "stony": 0.25, "unknown": 0.14}[fam]


def score_body(
    *,
    designation: str,
    name: str | None = None,
    spec: str | None = None,
    h_mag: float | None = None,
    diameter_km: float | None = None,
    dv_kms: float | None = None,
    next_approach: str | None = None,
    approach_au: float | None = None,
) -> Score:
    notes: list[str] = []
    fam = family(spec)
    alb = albedo_for(fam)
    diam = diameter_km
    if diam is None:
        diam = diameter_from_h(h_mag, alb)
        if diam is not None:
            notes.append(f"diameter estimated from H with albedo {alb}")

    dv = dv_kms if dv_kms and dv_kms > 0 else None
    if dv is None:
        dv = 12.0
        notes.append("delta-v missing; penalty dv=12 km/s applied")

    size = max(diam or 0.0, 0.0)
    size_term = size**1.5

    water_w = {"water": 1.0, "unknown": 0.25, "stony": 0.05, "metal": 0.02}[fam]
    metal_w = {"metal": 1.0, "unknown": 0.2, "stony": 0.08, "water": 0.04}[fam]

    water = water_w * size_term / (dv + 0.5)
    pgm = metal_w * size_term / (dv + 0.5)

    conf = 0.35
    if spec:
        conf += 0.25
    if diameter_km:
        conf += 0.2
    if dv_kms:
        conf += 0.2
    conf = min(conf, 0.95)
    if fam == "unknown":
        conf = min(conf, 0.45)
        notes.append("spectral class unknown; scores capped in meaning")

    vanity = 0.0
    if diam:
        vol_m3 = (4 / 3) * 3.1415926535 * ((diam * 500) ** 3)
        mass_t = vol_m3 * 3.0 / 1000.0
        vanity = mass_t * 100.0
        notes.append("earth_spot_usd_vanity is a toy mass*price, not NPV")

    return Score(
        designation=designation,
        name=name,
        spec=spec,
        spec_family=fam,
        h_mag=h_mag,
        diameter_km=round(diam, 4) if diam is not None else None,
        dv_kms=round(dv, 3) if dv else None,
        next_approach=next_approach,
        approach_au=approach_au,
        water_score=round(water, 6),
        pgm_score=round(pgm, 6),
        confidence=round(conf, 3),
        earth_spot_usd_vanity=round(vanity, 2),
        notes=notes,
    )
