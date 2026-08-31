# Golden case 1 — Bennu water rank

Input:

- Bennu: spec B, diameter 0.49 km, Δv 5.1 km/s
- Control: spec Sq, same size and Δv

Expected:

- `family("B") == "water"`
- Bennu `water_score` > control `water_score`

This case does not move unless HudsonR&D says so.
