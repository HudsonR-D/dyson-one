# Plan (living)

Ordered so each rung leaves the tower taller without new compute classes.

## Done (v0.1 → v0.2)

- [x] Constitution and rubric
- [x] Deterministic optics + Bennu golden case
- [x] Observe path on JPL SSD
- [x] Agent surface: AGENT.md, SYSTEM, ONTOLOGY
- [x] Verbs: observe / show / explain / gaps / diff
- [x] Snapshot schema v1 + attention block + previous.json

## Next (still cheap)

1. Persist `attention` into BRIEF.md so a skimming agent sees gaps first.
2. Golden fixture snapshot under `evals/fixtures/` so `explain`/`gaps` tests never need network.
3. Cap observe runtime in budgets; fail loud if JPL is down rather than writing an empty world.
4. Weekly critic remains stub until a key exists; if added, hard-cap tokens and require a test.

## Later (only if the ledger is used)

- Rubin / NEO Surveyor ingest as another L0 sensor, same object schema
- Apophis-2029 window as a first-class attention event
- Pages site that is just BRIEF.md + latest.json (no app)

## Never

- Vehicle GNC
- Market-making
- Unbounded sub-agents
- Scoring rocks with an LLM
