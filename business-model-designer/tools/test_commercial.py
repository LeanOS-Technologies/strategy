"""Tests for commercial.py: python3 -m unittest discover -s tools -p 'test_*.py'"""

import contextlib
import io
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import commercial as c  # noqa: E402


def run(*argv):
    buf = io.StringIO()
    err = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(err):
        code = c.main(list(argv))
    return code, buf.getvalue(), err.getvalue()


class Contribution(unittest.TestCase):
    def test_known_inputs(self):
        out = c.contribution("49 USD", "2.9% + 0.30 USD", ["hosting=1.20 USD"])
        self.assertEqual(out["fee"], "1.72 USD")
        self.assertEqual(out["net_collected"], "47.28 USD")
        self.assertEqual(out["contribution"], "46.08 USD")
        self.assertIn("49.00 USD − 1.72 USD = 47.28 USD", out["expressions"])
        self.assertIn("47.28 USD − 1.20 USD = 46.08 USD", out["expressions"])

    def test_unknown_cost_gives_unknown_contribution_and_names_it(self):
        out = c.contribution("49 USD", "2.9% + 0.30 USD", ["support=unknown"])
        self.assertEqual(out["net_collected"], "47.28 USD")
        self.assertEqual(out["contribution"], "unknown")
        self.assertEqual(out["missing"], ["support"])

    def test_unknown_price(self):
        out = c.contribution("unknown", "2.9%", [])
        self.assertEqual(out["contribution"], "unknown")
        self.assertIn("price", out["missing"])

    def test_unknown_fee(self):
        out = c.contribution("49 USD", "unknown", ["none"])
        self.assertEqual(out["net_collected"], "unknown")
        self.assertEqual(out["missing"], ["fee"])

    def test_mixed_currency_refused(self):
        code, _, err = run("contribution", "--price", "49 USD", "--fee", "0.25 EUR")
        self.assertEqual(code, 2)
        self.assertIn("mixed currencies", err)

    def test_amount_without_currency_refused(self):
        code, _, err = run("contribution", "--price", "49", "--fee", "none")
        self.assertEqual(code, 2)

    def test_declared_no_fee_and_no_costs(self):
        out = c.contribution("300 USD", "none", ["none"])
        self.assertEqual(out["contribution"], "300.00 USD")

    def test_omitted_costs_leave_contribution_unknown(self):
        out = c.contribution("300 USD", "none", [])
        self.assertEqual(out["net_collected"], "300.00 USD")
        self.assertEqual(out["contribution"], "unknown")
        self.assertTrue(any(m.startswith("variable costs") for m in out["missing"]))

    def test_fee_is_required(self):
        with self.assertRaises(SystemExit) as exc:
            run("contribution", "--price", "300 USD")
        self.assertEqual(exc.exception.code, 2)


class Timing(unittest.TestCase):
    def test_upfront(self):
        out = c.timing("300 USD", "upfront")
        self.assertEqual(out["periods"], [{"period": 0, "amount": "300.00 USD"}])

    def test_split(self):
        out = c.timing("300 USD", "split:50%,50%")
        self.assertEqual([p["amount"] for p in out["periods"]], ["150.00 USD", "150.00 USD"])

    def test_monthly_remainder_in_last_period(self):
        out = c.timing("100 USD", "monthly:3")
        self.assertEqual([p["amount"] for p in out["periods"]], ["33.33 USD", "33.33 USD", "33.34 USD"])
        self.assertTrue(out["expression"].endswith("= 100.00 USD"))

    def test_split_must_sum_to_100(self):
        code, _, _ = run("timing", "--price", "300 USD", "--schedule", "split:50%,40%")
        self.assertEqual(code, 2)

    def test_unknown_price(self):
        self.assertEqual(c.timing("unknown", "upfront")["periods"], "unknown")


class Discount(unittest.TestCase):
    def test_within(self):
        out = c.discount("49 USD", "20%", "25%", None)
        self.assertEqual(out["net_price"], "39.20 USD")
        self.assertTrue(out["within_authority"])

    def test_outside_bound_exit_1(self):
        code, stdout, _ = run("discount", "--list", "49 USD", "--discount", "30%", "--bound", "25%", "--json")
        self.assertEqual(code, 1)
        self.assertFalse(json.loads(stdout)["within_authority"])

    def test_floor(self):
        out = c.discount("49 USD", "10 USD", "25%", "40 USD")
        self.assertFalse(out["within_authority"])
        self.assertIn("below floor", out["message"])

    def test_unknown_bound(self):
        out = c.discount("49 USD", "20%", "unknown", None)
        self.assertEqual(out["within_authority"], "unknown")

    def test_mixed_currency(self):
        code, _, _ = run("discount", "--list", "49 USD", "--discount", "5 EUR", "--bound", "25%")
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
