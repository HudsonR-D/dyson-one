from dyson_one.score import family, score_body


def test_bennu_is_water_family():
    bennu = score_body(
        designation="101955",
        name="Bennu",
        spec="B",
        h_mag=20.21,
        diameter_km=0.49,
        dv_kms=5.1,
    )
    stony = score_body(
        designation="dummy-s",
        spec="Sq",
        h_mag=20.21,
        diameter_km=0.49,
        dv_kms=5.1,
    )
    assert family("B") == "water"
    assert family("Sq") == "stony"
    assert bennu.water_score > stony.water_score
    assert bennu.spec_family == "water"


def test_unknown_confidence_capped():
    s = score_body(designation="2026 AA", h_mag=24.0)
    assert s.spec_family == "unknown"
    assert s.confidence <= 0.45


def test_vanity_is_present_and_noted():
    s = score_body(designation="x", diameter_km=0.1, spec="C", dv_kms=5.0)
    assert s.earth_spot_usd_vanity > 0
    assert any("not NPV" in n for n in s.notes)
