from dyson_one.__main__ import build_parser


def test_observe_accepts_out_after_verb():
    args = build_parser().parse_args(["observe", "--out", "data"])
    assert args.cmd == "observe"
    assert str(args.out) == "data"


def test_observe_accepts_out_before_verb():
    args = build_parser().parse_args(["--out", "data", "observe"])
    assert args.cmd == "observe"
    assert str(args.out) == "data"


def test_explain_keeps_designation():
    args = build_parser().parse_args(["explain", "101955", "--out", "data"])
    assert args.cmd == "explain"
    assert args.designation == "101955"
