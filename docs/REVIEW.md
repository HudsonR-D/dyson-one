# Adversarial review — 2026-09-06

## Production failure

`daily-ledger` failed 6/6 scheduled runs.

```
python -m dyson_one observe --out data
dyson-one: error: unrecognized arguments: --out data
```

`--out` lived only on the parent parser. Argparse does not accept parent flags after the subcommand. CI unit tests never invoked that argv shape.

## Fixes in 0.2.1

- Common flags registered on every verb (`observe --out data` and `--out data observe`)
- CLI contract tests
- Sensor retries + `SensorError`; observe degrades if one catalog dies, exits 1 if both empty
- Daily workflow timeout, unbuffered logs, commit only when snapshot changes

## Remaining (not blockers)

- Medium: CAD-only rocks get penalty Δv=12 and can crowd ranks
- Medium: `cad_limit` ignores `--limit` (uses budgets)
- Nit: actions/checkout@v4 Node 20 deprecation warning
- Nit: no offline fixture observe in CI (network path is daily-only)
