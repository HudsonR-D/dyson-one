# Dyson One rubric

Owner: HudsonR&D. The builder does not edit this file to make a score pass.

## Pass bar

1. `tests/test_score.py` is green.
2. Bennu (B-type) water_score beats an equal-size, equal-Δv Sq-type.
3. Unknown spectral class never claims confidence > 0.45.
4. Output snapshot includes `earth_spot_usd_vanity` only with a note that it is not NPV.
5. No module under `src/dyson_one` may call a write API, payment API, or spacecraft API.

## Critic budget

If a model critic runs: one proposal per week, must cite a failing or held-out case, must not expand actuators.
