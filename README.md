# Dyson One

**HudsonR&D world-model of near-Earth bodies, scored for in-space resource potential.**

Observe and rank. No actuators. No token furnace.

If you are an agent, start at [`AGENT.md`](./AGENT.md).  
If you want the tower of layers, read [`docs/SYSTEM.md`](./docs/SYSTEM.md).

## Frontend

Buildable-style single page (no framework): [`web/index.html`](./web/index.html)

```bash
python3 -m http.server 8765 --directory web
# another shell: cp data/latest.json web/latest.json
# open http://127.0.0.1:8765
```

Live sources, in order: `./latest.json`, `../data/latest.json`, raw GitHub `main`.

Enable GitHub Pages (Actions source) so `pages.yml` can publish `https://hudsonr-d.github.io/dyson-one/`.

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python -m dyson_one observe --out data
python -m dyson_one show --out data
```

## Verbs

| Verb | Meaning |
| --- | --- |
| `observe` | refresh `data/latest.json` from JPL |
| `show` | print the brief |
| `explain DES` | expand why a body ranked as it did |
| `gaps` | print attention queues |
| `diff` | latest vs previous snapshot |

## License

MIT. See `LICENSE` and `NOTICE`.
