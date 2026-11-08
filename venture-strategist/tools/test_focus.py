"""Tests for focus.py: ready set, cycles, timing findings and comparison."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import focus  # noqa: E402

PLAN = """# Focus plan

Owner: venture-strategist/set-focus · Updated: 2026-01-10
Built from: bet-portfolio@abc

## Conclusion
Convert current users first.

## Current focus
Convert current users.

## Work sequence
| ID | Bet | Action and output | Executor | Timing | Prerequisite |
| --- | --- | --- | --- | --- | --- |
| ACT-1 | BET-1 | Draft offer | business-model-designer | now | none |
| ACT-2 | BET-1 | Contact users | owner | after | ACT-1, ENB-1 |
| ACT-3 | BET-2 | Trial outline | owner | parallel | none |
| ACT-4 | BET-2 | Run trial | owner | {t4} | {p4} |

## Enabling actions
| ID | Action | Missing condition | Enabling step or alternative | Owner | Continuing work |
| --- | --- | --- | --- | --- | --- |
| ENB-1 | ACT-2 | No payment method | Finance question; manual invoice | Finance | ACT-1, ACT-3 |

## Change conditions
- A user declines citing scope.
"""


def plan(t4="after", p4="firm agrees to a trial"):
    d = tempfile.mkdtemp()
    p = Path(d) / "focus-plan.md"
    p.write_text(PLAN.format(t4=t4, p4=p4), encoding="utf-8")
    return p


class ReadyTests(unittest.TestCase):
    def run_ready(self, path, satisfied):
        actions, enabling = focus.load_plan(path)
        return focus.ready(actions, enabling, satisfied)

    def codes(self, result, level=None):
        return [f["code"] for f in result["findings"] if level is None or f["level"] == level]

    def test_independent_work_stays_ready_when_one_action_blocked(self):
        r = self.run_ready(plan(), [])
        self.assertIn("ACT-1", r["ready"])
        self.assertIn("ACT-3", r["ready"])
        self.assertNotIn("ACT-2", r["ready"])
        self.assertIn("ENB-1", r["ready"])
        self.assertEqual(self.codes(r, "error"), [])

    def test_satisfied_ids_and_conditions(self):
        r = self.run_ready(plan(), ["ACT-1", "ENB-1", "Firm agrees to  a trial"])
        self.assertIn("ACT-2", r["ready"])
        self.assertIn("ACT-4", r["ready"])
        self.assertIn("WAITING-READY", self.codes(r, "info"))

    def test_now_action_with_unmet_prerequisite_is_error(self):
        r = self.run_ready(plan(t4="now"), [])
        self.assertIn("TIMING-UNREADY", self.codes(r, "error"))

    def test_cycle_detected(self):
        r = self.run_ready(plan(p4="ACT-4"), [])
        self.assertIn("CYCLE", self.codes(r, "error"))

    def test_undeclared_prerequisite(self):
        r = self.run_ready(plan(p4="ACT-9"), [])
        self.assertIn("UNDECLARED", self.codes(r, "error"))

    def test_cli_exit_codes(self):
        self.assertEqual(focus.main(["ready", str(plan())]), 0)
        self.assertEqual(focus.main(["ready", str(plan(t4="now"))]), 1)
        self.assertEqual(focus.main(["ready", "/nonexistent/focus-plan.md"]), 2)

    def test_deterministic(self):
        p = plan()
        self.assertEqual(self.run_ready(p, ["ACT-1"]), self.run_ready(p, ["ACT-1"]))


class CompareTests(unittest.TestCase):
    def test_difference_and_ratio(self):
        r = focus.compare("3 inspectors", "1 inspector")
        self.assertEqual(r["difference"], -2)
        self.assertAlmostEqual(r["ratio"], 1 / 3, places=5)

    def test_unknown_not_comparable(self):
        self.assertFalse(focus.compare("3 inspectors", "unknown")["comparable"])
        self.assertEqual(focus.main(["compare", "--expected", "3 inspectors", "--observed", "unknown"]), 3)

    def test_incompatible_units_refused(self):
        with self.assertRaises(ValueError):
            focus.compare("10 USD", "10 EUR")
        self.assertEqual(focus.main(["compare", "--expected", "10 USD", "--observed", "10 EUR"]), 2)

    def test_zero_expected_has_no_ratio(self):
        self.assertIsNone(focus.compare("0 inspectors", "2 inspectors")["ratio"])


if __name__ == "__main__":
    unittest.main()
