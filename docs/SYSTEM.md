# Dyson One as a system

Not a pile of scripts. A **world-model under a constitution**.

```
L6  CONSTITUTION     CHARTER.md + evals/rubric.md     frozen
L5  AMENDMENT        critic stub → gated PR           optional, token-capped
L4  ATTENTION        gaps / unknown_low_dv            where the next joule goes
L3  MEMORY           data/latest.json + ledger.jsonl  the world + hashes
L2  OPTICS           score.py                         two currencies + confidence
L1  DERIVED          family, diameter-from-H          labeled inference
L0  FACTS            JPL NHATS / CAD / SBDB           read-only sensors
```

An agent climbs only as high as the question requires.

- “What is Bennu’s water rank?” → L3, then L2 via `explain`
- “Why is this S-type above a C-type?” → L2 + test
- “Where do I spend 12 lookups?” → L4
- “Should weights change?” → L5, only after L6 still holds

## Coherence rules

1. **One primary key.** `designation` in every layer.
2. **One snapshot schema.** `schemas/snapshot.v1.json`. Bump the version if you break a field.
3. **One budget file.** `config/budgets.json`. HTTP and tokens are explicit.
4. **One pair of currencies.** Water (in-space) and PGM (speculative). No third secret score.
5. **Provenance over polish.** Missing class is `unknown`, not a guessed C-type.
6. **Accretion is state, not processes.** A good run leaves a better snapshot, a previous snapshot, a gap list, and a hash line. It does not leave another agent.

## Control loop

```
observe → write latest.json + previous.json + BRIEF.md + ledger.jsonl
        → attention block inside the snapshot
show    → render L3 for a human or a later agent
diff    → L3 now minus L3 previous
test    → lock L2 to L6
```

Sensors never write the constitution. The critic never writes the snapshot.
Optics never call the network.

## Resource ethic

The scarce goods are JPL courtesy, CI minutes, and (later) tokens.

Order of spend:

1. Read `data/latest.json`
2. Compute on disk (`explain`, `gaps`, `diff`)
3. `observe` with `sbdb_lookups` from budgets
4. Tokens only inside a future critic, and only against the rubric

If a task can be answered at a lower layer, doing it at a higher layer is a bug.

## What “best results” means here

Accuracy is **rank-order under uncertainty**, not a dollar on Psyche.
Optimal control is **spending the next lookup on the object whose unknown
class most changes a top-N rank**.
Least expenditure is **zero tokens on the daily path**.

That is the whole system.
