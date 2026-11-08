"""Tests for positioning.py. Run: python3 -m unittest discover -s tools -p 'test_*.py'"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import positioning  # noqa: E402

HEAD = "# {t}\n\nOwner: positioning-strategist/{s} · Updated: 2026-01-01\nBuilt from: none\n\n## Conclusion\nIllustrative.\n\n"

DIFF = HEAD.format(t="Differentiation", s="define-differentiation") + """## Leading value
Illustrative [proposed].

## Alternative basis

| ID | Alternative | Target | Why considered | Basis |
| --- | --- | --- | --- | --- |
| ALT-1 | Own word-processor template | SEG-1 | Status quo | [hypothesis] |
| ALT-2 | Vendor report product | SEG-1 | Direct competitor | [hypothesis] |
{extra_alt}
## Advantage chains

| ID | Capability | Availability | Against | Customer consequence | Target |
| --- | --- | --- | --- | --- | --- |
| ADV-1 | Capture once | available | ALT-1 | Faster report [hypothesis] | SEG-1 |
| ADV-2 | Photo sync | planned | {against2} | Photos flow [hypothesis] | SEG-1 |

## Support and trade-offs

| Advantage | Support | Sacrifice | Needed proof or development |
| --- | --- | --- | --- |
| ADV-1 | Users [hypothesis] | Desktop step | Time reports |
{support2}
"""


def write(d: Path, name: str, text: str) -> Path:
    p = d / name
    p.write_text(text, encoding="utf-8")
    return p


def diff(extra_alt="", against2="ALT-2", support2="| ADV-2 | Roadmap | Phone users | Build photo sync |"):
    return DIFF.format(extra_alt=extra_alt, against2=against2, support2=support2)


class PositioningTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def rules(self, findings, level=None):
        return sorted(f["rule"] for f in findings if level is None or f["level"] == level)

    def test_valid_document_has_no_errors(self):
        p = write(self.d, "differentiation.md", diff())
        self.assertEqual(self.rules(positioning.check(p), "error"), [])

    def test_undeclared_alternative_is_an_error(self):
        p = write(self.d, "differentiation.md", diff(against2="ALT-9"))
        self.assertIn("AGAINST", self.rules(positioning.check(p), "error"))

    def test_missing_alternative_reference_is_an_error(self):
        p = write(self.d, "differentiation.md", diff(against2="none"))
        self.assertIn("AGAINST", self.rules(positioning.check(p), "error"))

    def test_missing_support_row_is_an_error(self):
        p = write(self.d, "differentiation.md", diff(support2=""))
        self.assertIn("SUPPORT", self.rules(positioning.check(p), "error"))

    def test_planned_without_development_need_is_an_error(self):
        p = write(self.d, "differentiation.md", diff(support2="| ADV-2 | Roadmap | Phone users | none |"))
        self.assertIn("DEVELOPMENT", self.rules(positioning.check(p), "error"))

    def test_unused_alternative_is_info_only(self):
        p = write(self.d, "differentiation.md",
                  diff(extra_alt="| ALT-3 | Hire a typist | SEG-1 | Outsourcing | [hypothesis] |\n"))
        f = positioning.check(p)
        self.assertEqual(self.rules(f, "error"), [])
        self.assertIn("UNUSED-ALT", self.rules(f, "info"))

    def test_planned_advantage_in_frame_is_flagged_for_review(self):
        p = write(self.d, "differentiation.md", diff())
        pos = write(self.d, "positioning-decision.md", HEAD.format(t="Positioning", s="choose-frame")
                    + "## Positioning choice\nFor SEG-1, leading with ADV-1 and ADV-2 [proposed].\n")
        f = positioning.check(p, positioning=pos)
        self.assertEqual(self.rules(f, "review"), ["PLANNED-FRAME"])
        self.assertEqual(self.rules(f, "error"), [])

    def test_available_offer_citing_planned_advantage_is_flagged(self):
        p = write(self.d, "differentiation.md", diff())
        off = write(self.d, "offer-catalogue.md", HEAD.format(t="Offers", s="design-offers") + """## Offers

| ID | Offer | Target | Opportunity | Promised outcome | Entitlement | Revenue model | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OFR-1 | App | TGT-1 | OPP-1 | Report with photos (ADV-2) | Licence | RM-1 | available |
| OFR-2 | Sync add-on | TGT-1 | OPP-1 | Photos (ADV-2) | Add-on | RM-1 | future |
""")
        f = positioning.check(p, offers=off)
        review = [x for x in f if x["level"] == "review"]
        self.assertEqual(len(review), 1)
        self.assertIn("OFR-1", review[0]["message"])

    def test_cli_exit_codes(self):
        good = write(self.d, "good.md", diff())
        bad = write(self.d, "bad.md", diff(against2="ALT-9"))
        self.assertEqual(positioning.main(["check", str(good)]), 0)
        self.assertEqual(positioning.main(["check", str(bad)]), 1)
        self.assertEqual(positioning.main(["check", str(self.d / "missing.md")]), 2)

    def test_read_only_and_deterministic(self):
        p = write(self.d, "differentiation.md", diff(against2="ALT-9"))
        before = p.read_text(encoding="utf-8")
        self.assertEqual(positioning.check(p), positioning.check(p))
        self.assertEqual(p.read_text(encoding="utf-8"), before)


if __name__ == "__main__":
    unittest.main()
