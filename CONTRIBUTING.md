# Contributing

Read `CHARTER.md` first.

- Scoring changes need a test. The Bennu case in `evals/cases.md` is frozen.
- Do not add actuators, paid APIs, or secrets.
- Keep ingest polite: cache, sleep between SBDB lookups, send a real User-Agent.
- PRs that only change vanity dollar formulas should label them as vanity.
