# Dyson One

**HudsonR&D open ledger of near-Earth bodies scored for in-space resource potential.**

Observe and rank. No actuators. No token furnace.

Dyson One is a public notebook: pull NASA/JPL catalogs, score a small accessible set with boring Python, publish a snapshot. An optional critic may propose scorer patches later. It does not fly, buy, or spawn miners.

This is the missing layer between [JPL SBDB](https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html) / [NHATS](https://cneos.jpl.nasa.gov/nhats/) and poster-math sites that multiply iron mass by Earth spot prices.

## Charter (short)

- Two currencies: **water/in-space** and **speculative PGM**
- `earth_spot_usd_vanity` is labeled a toy number
- Unknown spectra stay low-confidence
- Compute lives on GitHub Actions free minutes

Full rules: [`CHARTER.md`](./CHARTER.md)

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python -m dyson_one --out data --limit 40 --lookup 8
```

No API key. JPL SSD is public; be polite.

## What it writes

| File | Role |
| --- | --- |
| `data/latest.json` | scored snapshot + hash |
| `data/BRIEF.md` | top-25 table |
| `data/ledger.jsonl` | append-only run log |

## How scoring works

Deterministic. Spectral family (C/B → water, M/X → metal, S/Q → stony, else unknown) × size term ÷ (Δv + 0.5). NHATS supplies Δv when present. Missing class is not treated as treasure.

Golden case: Bennu (B-type) must beat an equal-size Sq-type on `water_score`. See `evals/`.

## Self-improvement (intentionally small)

Daily CI refreshes the ledger. The critic is a stub until someone adds a budget-capped model key. Rubric does not move to make a run pass.

## Status

v0.1.0 — first public skeleton. Experiment, not a mine.

## License

MIT. See `LICENSE` and `NOTICE`.
