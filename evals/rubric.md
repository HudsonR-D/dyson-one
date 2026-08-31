# Dyson One rubric

Owner: HudsonR&D. The builder does not edit this file to make a score pass.
This is L6 together with `CHARTER.md`.

## Pass bar

1. `pytest -q` is green (`tests/test_score.py` and `tests/test_world.py`).
2. Bennu (B-type) water_score beats an equal-size, equal-Δv Sq-type.
3. Unknown spectral class never claims confidence > 0.45.
4. Snapshot includes `earth_spot_usd_vanity` only with a note that it is not NPV.
5. Snapshot `schema_version` is 1 and `charter` is `observe-and-rank`.
6. Snapshot contains `attention.unknown_low_dv`.
7. No module under `src/dyson_one` may call a write API, payment API, or spacecraft API.
8. Field names match `docs/ONTOLOGY.md`. No aliases.

## Critic budget

If a model critic runs: one proposal per week, must cite a failing or held-out case, must not expand actuators, must not exceed `critic_tokens_max` in `config/budgets.json`.
