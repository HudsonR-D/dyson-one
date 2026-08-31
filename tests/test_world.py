from dyson_one.ledger import write_snapshot
from dyson_one.score import score_body
from dyson_one.world import attention, diff_worlds, explain_row, find_object


def _rows():
    return [
        score_body(designation="101955", name="Bennu", spec="B", diameter_km=0.49, dv_kms=5.1),
        score_body(designation="dummy-s", spec="Sq", diameter_km=0.49, dv_kms=5.1),
        score_body(designation="2026 AA", h_mag=24.0, dv_kms=4.2),
    ]


def test_attention_puts_unknown_low_dv_first(tmp_path):
    payload = write_snapshot(tmp_path, _rows(), generated_at="2026-08-31T00:00:00Z")
    assert payload["schema_version"] == 1
    assert payload["charter"] == "observe-and-rank"
    assert "2026 AA" in payload["attention"]["unknown_low_dv"]
    assert payload["attention"]["high_water"][0] == "101955"


def test_explain_mentions_optics():
    row = score_body(designation="101955", spec="B", diameter_km=0.49, dv_kms=5.1).to_dict()
    text = explain_row(row)
    assert "101955" in text
    assert "water_score" in text
    assert "Not NPV" in text


def test_find_and_diff(tmp_path):
    write_snapshot(tmp_path, _rows()[:2], generated_at="2026-08-31T00:00:00Z")
    write_snapshot(tmp_path, _rows(), generated_at="2026-08-31T01:00:00Z")
    import json

    snap = json.loads((tmp_path / "latest.json").read_text(encoding="utf-8"))
    assert find_object(snap, "Bennu")["designation"] == "101955"
    prev = json.loads((tmp_path / "previous.json").read_text(encoding="utf-8"))
    text = diff_worlds(snap, prev)
    assert "2026 AA" in text
    assert attention(snap["objects"])["unknown_low_dv"]
