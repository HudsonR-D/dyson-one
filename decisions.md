# decisions

## 2026-08-31 — world-model, not a swarm

Dyson One accretes **state** (snapshot, previous, attention, hashes), not processes.
An agent’s first move is to read `data/latest.json`, not to spawn helpers.

## 2026-08-31 — two currencies only

`water_score` (in-space) and `pgm_score` (speculative). Vanity dollars stay labeled and unused for rank.

## 2026-08-31 — attention is the control knob

The next SBDB lookup is `attention.unknown_low_dv[0]`. That is optimal control under the compute cap.
