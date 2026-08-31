# Dyson One Charter

HudsonR&D public experiment. Freeze this unless a review gate moves it.

## Mission

Observe and rank near-Earth small bodies for **in-space** and **speculative Earth-return** resource potential. Keep a living ledger. Improve the scorer only when a change beats a frozen rubric.

## Allowed

- Read public NASA / JPL / MPC / CNEOS catalogs
- Score, log, and publish tables
- Open pull requests that change weights or ingest code
- Optional, budget-capped critic (weekly, no key required to run the ledger)

## Forbidden

- Commanding, booking, or simulating a vehicle as an actuator
- Spending money
- Treating Earth-spot “asteroid net worth” as a valuation
- Spawning unbounded sub-agents
- Storing secrets in the repository
- Marketing the ledger as mining advice or an investment product

## Compute rule

Scoring is deterministic Python. Tokens are optional and capped. If there is no critic key, the daily job still ships.

## Failure mode we accept

Wrong spectral class, missing diameter, optimistic Δv. We label confidence. We do not invent certainty.
