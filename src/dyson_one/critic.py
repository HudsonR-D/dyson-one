"""Optional weekly critic. Offline unless a key exists.

v0 writes a stub so CI stays keyless.
"""

from __future__ import annotations

from pathlib import Path

STUB = """# Critic stub

No model key configured. Ledger ran without tokens.

To enable a budget-capped critic later:
1. Keep `evals/rubric.md` frozen unless HudsonR&D moves the bar.
2. Feed only the top-20 score deltas plus failing tests.
3. Cap the prompt. Reject any proposal that fails `tests/test_score.py`.
"""


def run_critic(out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "CRITIC.md"
    path.write_text(STUB, encoding="utf-8")
    return path
