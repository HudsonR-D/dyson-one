# AGENT.md — start here

You are driving **Dyson One**, a world-model with a frozen constitution.
You are not flying a mine. You are keeping a ledger of near-Earth bodies
accurate enough that a later, richer system could choose well.

If you only read one file after this, read `docs/SYSTEM.md`.

## Constitution (do not violate)

`CHARTER.md` + `evals/rubric.md` are law. You may not:

- add actuators, payments, vendor mail, or spawn loops
- treat `earth_spot_usd_vanity` as value
- edit `evals/rubric.md` or the Bennu golden case to make a run pass
- spend tokens on scoring rocks

## The only object you need to *see*

```
data/latest.json
```

That file is the world. Schema: `schemas/snapshot.v1.json`.
If it is missing or stale, run `observe`. Do not re-fetch JPL to answer
a question the snapshot already holds.

## Verbs (control surface)

| Verb | Command | Cost | When |
| --- | --- | --- | --- |
| observe | `python -m dyson_one observe` | HTTP, no tokens | snapshot missing/stale |
| show | `python -m dyson_one show` | disk | brief the world |
| explain | `python -m dyson_one explain DES` | disk | why this rank |
| gaps | `python -m dyson_one gaps` | disk | where the next lookup goes |
| diff | `python -m dyson_one diff` | disk | what changed since last observe |
| test | `pytest -q` | disk | before any scorer patch |

Default `python -m dyson_one` is `observe` (CI compat).

## Attention rule

Spend the next SBDB lookup on `attention.unknown_low_dv` in the snapshot.
Never spray lookups across the whole catalog. Budgets live in
`config/budgets.json`.

## How to change the scorer

1. Add or extend a test under `tests/` that encodes the new truth.
2. Change `src/dyson_one/score.py` only.
3. `pytest -q` must stay green, including Bennu vs Sq.
4. One concern per patch. Open a PR. Do not “also add a critic model.”

## Session protocol

1. Read this file and `data/BRIEF.md` if present.
2. State the snapshot hash you are working from.
3. Prefer `explain` / `gaps` / `diff` over rereading source.
4. Write durable notes into `progress.md` and `decisions.md`, not chat.
5. Stop. Do not start the next feature in the same breath.

## Ontology cheat sheet

Primary key: `designation`.
Families: `water | metal | stony | unknown`.
Currencies: `water_score` (in-space), `pgm_score` (speculative).
Trust: `confidence` (unknown family ≤ 0.45).
Toy: `earth_spot_usd_vanity`.

Full field dictionary: `docs/ONTOLOGY.md`.
Tower of layers: `docs/SYSTEM.md`.
