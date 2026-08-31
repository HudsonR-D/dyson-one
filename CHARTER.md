# Dyson One Charter

HudsonR&D public experiment. Freeze this unless a review gate moves it.

This file is **L6** in `docs/SYSTEM.md`. Agents treat it as law.

## Mission

Observe and rank near-Earth small bodies for **in-space** and **speculative Earth-return** resource potential. Keep a living world-model. Improve the optics only when a change beats a frozen rubric.

## Identity

Dyson One is a **world-model with a frozen constitution**.
It is not a miner, not a market, not a swarm.

- World: `data/latest.json` (`schemas/snapshot.v1.json`)
- Constitution: this file + `evals/rubric.md`
- Control surface: `AGENT.md` verbs
- Attention: snapshot `attention.unknown_low_dv`

## Allowed

- Read public NASA / JPL / MPC / CNEOS catalogs
- Score, log, explain, diff, and publish tables
- Open pull requests that change weights or ingest code
- Optional, budget-capped critic (weekly, no key required to run the ledger)

## Forbidden

- Commanding, booking, or simulating a vehicle as an actuator
- Spending money
- Treating Earth-spot “asteroid net worth” as a valuation
- Spawning unbounded sub-agents
- Storing secrets in the repository
- Marketing the ledger as mining advice or an investment product
- Scoring rocks with an LLM
- Inventing field names outside `docs/ONTOLOGY.md`

## Compute rule

Climb the smallest layer that answers the question (`docs/SYSTEM.md`).
Scoring is deterministic Python. Tokens are optional and capped at
`config/budgets.json` → `critic_tokens_max` (default 0).
If there is no critic key, observe still ships.

Spend the next SBDB lookup on `attention.unknown_low_dv`, never on the whole belt.

## Failure mode we accept

Wrong spectral class, missing diameter, optimistic Δv. We label confidence. We do not invent certainty.
