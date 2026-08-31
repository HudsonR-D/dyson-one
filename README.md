# Dyson One

**HudsonR&D world-model of near-Earth bodies, scored for in-space resource potential.**

Observe and rank. No actuators. No token furnace.

If you are an agent, start at [`AGENT.md`](./AGENT.md).  
If you want the tower of layers, read [`docs/SYSTEM.md`](./docs/SYSTEM.md).

Dyson One is one system: frozen constitution, read-only sensors, deterministic optics, a single snapshot that *is* the world, and an attention queue for the next cheap lookup. It does not fly, buy, or spawn miners.

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python -m dyson_one observe --out data
python -m dyson_one show --out data
python -m dyson_one gaps --out data
```

No API key. JPL SSD is public; budgets in `config/budgets.json`.

## Verbs

| Verb | Meaning |
| --- | --- |
| `observe` | refresh `data/latest.json` from JPL |
| `show` | print the brief |
| `explain DES` | expand why a body ranked as it did |
| `gaps` | print attention queues |
| `diff` | latest vs previous snapshot |

## Status

v0.2.0 — system layer. Experiment, not a mine.

## License

MIT. See `LICENSE` and `NOTICE`.
