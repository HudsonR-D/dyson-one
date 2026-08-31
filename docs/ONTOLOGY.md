# Ontology

Every field that appears in `data/latest.json` is defined here.
Agents must not invent aliases.

## Envelope

| Field | Layer | Meaning |
| --- | --- | --- |
| `schema_version` | L3 | Integer. Current: `1`. |
| `project` | L6 | Always `dyson-one`. |
| `charter` | L6 | Always `observe-and-rank`. |
| `generated_at` | L3 | UTC ISO-8601 with `Z`. |
| `hash` | L3 | 16-char sha256 prefix of canonical `objects`. |
| `count` | L3 | `len(objects)`. |
| `budgets` | L4 | Copy of budgets used for this observe. |
| `attention` | L4 | Where the next lookup should go. |
| `objects` | L3 | Ranked list. Water desc, PGM desc, designation asc. |

## Object

| Field | Layer | Meaning |
| --- | --- | --- |
| `designation` | L0 | Primary key. JPL/MPC packed or unpacked des. |
| `name` | L0 | Common name if known. |
| `spec` | L0 | SMASS/Tholen token if known. |
| `spec_family` | L1 | `water` \| `metal` \| `stony` \| `unknown`. |
| `h_mag` | L0 | Absolute magnitude H. |
| `diameter_km` | L0 or L1 | Measured, else estimated from H + family albedo. |
| `dv_kms` | L0 | NHATS min Δv when present; else penalty 12. |
| `next_approach` | L0 | CNEOS CAD calendar string, or null. |
| `approach_au` | L0 | Geocentric distance AU, or null. |
| `water_score` | L2 | In-space water/volatiles rank. Not dollars. |
| `pgm_score` | L2 | Speculative metal rank. Not a mine plan. |
| `confidence` | L2 | 0–0.95. Unknown family capped at 0.45. |
| `earth_spot_usd_vanity` | L2 | Toy mass × $100/t. Never NPV. |
| `notes` | L2 | Human-readable inference flags. |

## Attention

| Field | Meaning |
| --- | --- |
| `unknown_low_dv` | designations with family unknown and lowest Δv |
| `missing_approach` | scored but no CAD date |
| `high_water` | top water_score ids (context, not a buy list) |

## Forbidden synonyms

Do not write `id`, `asteroid_id`, `value`, `worth`, `profit`, `class`
when you mean the fields above.
