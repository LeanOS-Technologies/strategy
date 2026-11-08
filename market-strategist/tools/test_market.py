"""Tests for market.py. Run: python3 -m unittest discover -s workers/strategy/market-strategist/tools -p 'test_*.py'"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import market  # noqa: E402

TARGETS = """# Target segments

Owner: market-strategist/choose-targets · Updated: 2026-10-29
Built from: segments@abc

## Conclusion
Independent inspectors first.

## Target choice
Independent inspectors buy alone and fast.

## Target profile

| ID | Segment | Buyer and user | Buying situation | Need | Advantage |
| --- | --- | --- | --- | --- | --- |
| TGT-1 | SEG-1 | Inspector, same person | Between jobs | Faster reports | ADV-1 |

## Qualification

| ID | Target | Kind | Indicator | When unknown |
| --- | --- | --- | --- | --- |
| QR-1 | TGT-1 | qualifier | Writes their own reports | Ask in the first conversation |
| QR-2 | TGT-1 | disqualifier | Bound to a firm-mandated report tool | Treat as possible; ask |
| QR-3 | TGT-2 | qualifier | Several inspectors | n/a |

## Sequence and sensitivity

| Segment | Disposition | Strongest alternative | Enabling condition | Reversing assumption |
| --- | --- | --- | --- | --- |
| SEG-2 | later | SEG-1 | Team accounts exist | Firms decide faster than stated |
"""


class EstimateTest(unittest.TestCase):
    def test_product_and_units(self):
        rows = [
            {"factor": "inspectors", "low": "100", "base": "150", "high": "200", "unit": "inspector", "basis": "[observed: x]"},
            {"factor": "reports", "low": "100", "base": "200", "high": "300", "unit": "report/inspector", "basis": "[observed: y]"},
            {"factor": "share", "low": "10", "base": "20", "high": "30", "unit": "%", "basis": "[estimate: z]"},
        ]
        out = market.estimate(rows)
        self.assertEqual(out["unit"], "report")
        self.assertAlmostEqual(out["estimate"]["low"], 1000)
        self.assertAlmostEqual(out["estimate"]["base"], 6000)
        self.assertAlmostEqual(out["estimate"]["high"], 18000)

    def test_unknown_value_gives_unknown_estimate(self):
        rows = [
            {"factor": "inspectors", "low": "unknown", "base": "unknown", "high": "unknown", "unit": "inspector", "basis": "[observed: x]"},
            {"factor": "share", "low": "10", "base": "20", "high": "30", "unit": "%", "basis": "[estimate: z]"},
        ]
        out = market.estimate(rows)
        self.assertEqual(out["estimate"], "unknown")
        self.assertEqual(out["missing"], [{"factor": "inspectors", "reason": "value unknown"}])

    def test_missing_basis_gives_unknown_estimate(self):
        rows = [{"factor": "inspectors", "low": "100", "base": "150", "high": "200", "unit": "inspector", "basis": ""}]
        out = market.estimate(rows)
        self.assertEqual(out["estimate"], "unknown")
        self.assertEqual(out["missing"][0]["reason"], "no basis")

    def test_bounds_out_of_order_rejected(self):
        rows = [{"factor": "f", "low": "5", "base": "2", "high": "9", "unit": "x", "basis": "b"}]
        with self.assertRaises(market.InputError):
            market.estimate(rows)


class ScoreTest(unittest.TestCase):
    rows = [
        {"option": "SEG-1", "urgency": "4", "reach": "5", "speed": "5", "basis": "b"},
        {"option": "SEG-2", "urgency": "5", "reach": "3", "speed": "1", "basis": "b"},
    ]

    def test_ranking_and_reversal(self):
        out = market.score(self.rows, (1, 5), {"urgency": 1, "reach": 1, "speed": 1})
        self.assertEqual(out["ranking"], ["SEG-1", "SEG-2"])
        rv = out["reversal"]
        # totals 14 vs 9; only urgency favours SEG-2 (delta -1): weight must rise by 5
        self.assertEqual(rv["criterion"], "urgency")
        self.assertAlmostEqual(rv["weight_change"], 5)

    def test_score_off_scale_rejected(self):
        rows = [dict(self.rows[0], urgency="7"), self.rows[1]]
        with self.assertRaises(market.InputError):
            market.score(rows, (1, 5), {"urgency": 1, "reach": 1, "speed": 1})

    def test_weights_must_match_criteria(self):
        with self.assertRaises(market.InputError):
            market.score(self.rows, (1, 5), {"urgency": 1})


class QualifyTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.doc = Path(self.tmp.name) / "target-segments.md"
        self.doc.write_text(TARGETS, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_qualified(self):
        out = market.qualify(self.doc, {"QR-1": True, "QR-2": False}, "TGT-1")
        self.assertEqual(out["result"], "qualified")

    def test_disqualifier_true_disqualifies_even_with_unknowns(self):
        out = market.qualify(self.doc, {"QR-1": None, "QR-2": True}, "TGT-1")
        self.assertEqual(out["result"], "disqualified")

    def test_unknown_is_not_rejection(self):
        out = market.qualify(self.doc, {"QR-1": True}, "TGT-1")
        self.assertEqual(out["result"], "unknown")
        self.assertEqual(out["unknown"][0]["id"], "QR-2")
        self.assertIn("ask", out["unknown"][0]["treatment"])

    def test_cli_exit_codes(self):
        p = Path(self.tmp.name) / "p.json"
        p.write_text(json.dumps({"QR-1": "yes"}), encoding="utf-8")
        self.assertEqual(market.main(["qualify", str(self.doc), str(p), "--target", "TGT-1"]), 2)
        p.write_text(json.dumps({"QR-1": False}), encoding="utf-8")
        self.assertEqual(market.main(["qualify", str(self.doc), str(p), "--target", "TGT-1", "--json"]), 0)


if __name__ == "__main__":
    unittest.main()
