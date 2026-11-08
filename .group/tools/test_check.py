"""Regression tests for Strategy basis, accuracy and document checks.

Run: python3 -m unittest discover -s workers/strategy/.group/tools -p 'test_*.py'
"""

import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check
import strategy_docs as sd


VENTURE = """# Reporting venture

Owner: venture-strategist/define-venture · Updated: 2026-10-30
Built from: none

## Conclusion
Develop reporting tools that carry professional judgment into client reports.

## Perspective and ambition
Professional judgment should shape the report.

## Purpose and customers
Help independent inspectors explain their findings to clients.

## What it provides
A proposed report assembly tool and template conversion service.

## How it works
Recorded findings are placed in the inspector's mapped report sections.

## Commercial relationship
Inspectors buy a licence and can commission template conversion.

## Scope and current form
| Part | Status | Scope note |
| --- | --- | --- |
| Report assembly | proposed | [proposed] carries the inspector's findings into their chosen structure |
"""


class CheckTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "strategy"
        self.root.mkdir()

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def text_findings(self, body, corpus=""):
        path = self.write("price-book.md", "# Prices\n\n## Conclusion\n" + body)
        doc = sd.parse_document(path, "price-book")
        checker = check.Checker(self.root, {}, corpus)
        checker.check_text_rules(doc)
        return checker.findings

    def rules(self, body, corpus=""):
        return {f.rule for f in self.text_findings(body, corpus)}

    def run_cli(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = check.main([str(self.root), "--json", *args])
        return code, json.loads(output.getvalue())

    def test_amount_and_percentage_accept_basis_or_source_cell(self):
        for column in ("Basis", "Source"):
            for value in ("49 USD", "20%"):
                for basis_first in (False, True):
                    with self.subTest(column=column, value=value, basis_first=basis_first):
                        headers = ["Amount", column]
                        cells = [value, "[proposed] bounded commercial test"]
                        if basis_first:
                            headers.reverse()
                            cells.reverse()
                        body = "| " + " | ".join(headers) + " |\n| --- | --- |\n"
                        body += "| " + " | ".join(cells) + " |\n"
                        self.assertEqual(self.text_findings(body), [])

    def test_unsupported_amount_and_percentage_report_basis_error(self):
        for body in ("Test at 49 USD.", "Test a 20% concession.",
                     "| Amount | Basis |\n| --- | --- |\n| 49 USD | none |\n"):
            with self.subTest(body=body):
                findings = self.text_findings(body)
                self.assertEqual([f.rule for f in findings], ["NUM-BASIS"])
                self.assertIn("without basis in its row or sentence", findings[0].message)

    def test_basis_in_another_row_does_not_support_an_amount(self):
        body = """| Amount | Basis |
| --- | --- |
| free | [proposed] inspection entry |
| 49 USD | none |
"""
        findings = self.text_findings(body)
        self.assertEqual([f.rule for f in findings], ["NUM-BASIS"])
        self.assertIn("49 USD", findings[0].message)

    def test_decision_status_alone_does_not_supply_basis(self):
        body = "| Amount | Status |\n| --- | --- |\n| 49 USD | proposed |\n"
        self.assertEqual(self.rules(body), {"NUM-BASIS"})

    def test_prose_amount_with_its_basis_passes(self):
        self.assertEqual(self.text_findings("Test 49 USD [proposed] for one conversion."), [])

    def test_conviction_and_ambition_need_no_prose_markers(self):
        self.assertEqual(self.text_findings(
            "Professional judgment should shape reports. "
            "We aim to make own-format reporting a professional standard."
        ), [])

    def test_owner_quote_in_source_cell_supports_attributed_amount(self):
        body = """| Amount | Status | Source |
| --- | --- | --- |
| 49 USD | owner-set | [owner: "Charge 49 USD for conversion."] |
"""
        self.assertEqual(self.text_findings(body, sd.normalise("Charge 49 USD for conversion.")), [])

    def test_owner_marker_requires_a_quote(self):
        self.assertEqual(self.rules("49 USD [owner]"), {"ATTRIB-QUOTE"})

    def test_owner_attribution_phrase_requires_a_quote(self):
        self.assertEqual(self.rules("Owner-set price: 49 USD [proposed]."), {"ATTRIB-PHRASE"})

    def test_quote_absent_from_owner_material_is_rejected(self):
        self.assertEqual(self.rules('49 USD [owner: "Charge 49 USD."]',
                                    sd.normalise("Charge 99 USD.")), {"ATTRIB-ABSENT"})

    def test_no_owner_material_leaves_quote_unchecked(self):
        findings = self.text_findings('49 USD [owner: "Charge 49 USD."]', corpus=None)
        self.assertEqual([(f.rule, f.level) for f in findings], [("ATTRIB-ABSENT", "unchecked")])

    def test_strategy_documents_cannot_supply_observations(self):
        for ref in ("strategy/price-book.md#PRC-1", "price-book/main#PRC-1"):
            with self.subTest(ref=ref):
                self.assertEqual(self.rules(f"49 USD [observed: {ref}]"), {"CIRCULAR"})
        self.assertEqual(self.rules("49 USD [observed: finance/readout#ROW-1]"), set())

    def test_arithmetic_keeps_value_and_currency_checks(self):
        for expression in ("49 USD - 2 USD = 10 USD", "49 USD + 2 EUR = 51 USD"):
            with self.subTest(expression=expression):
                self.assertEqual(self.rules(expression + " [derived: stated inputs]"), {"ARITH"})
        self.assertEqual(self.rules("49 USD - 2 USD = 47 USD [derived: stated inputs]"), set())

    def test_current_contract_requires_perspective_and_ambition(self):
        self.write("venture.md", VENTURE.replace(
            "## Perspective and ambition\nProfessional judgment should shape the report.\n\n", ""
        ))
        code, result = self.run_cli()
        self.assertEqual(code, 1)
        self.assertEqual([f["rule"] for f in result["findings"]], ["SECTION"])
        self.assertIn("Perspective and ambition", result["findings"][0]["message"])

    def test_cli_checks_candidate_overlay_and_can_read_current_only(self):
        self.write("venture.md", VENTURE)
        code, result = self.run_cli()
        self.assertEqual((code, result["findings"]), (0, []))
        self.write("candidate/venture.md", VENTURE.replace(
            "Develop reporting tools that carry professional judgment into client reports.",
            "Test a licence at 49 USD."
        ))
        code, result = self.run_cli()
        self.assertEqual(code, 1)
        self.assertEqual(result["documents"], ["candidate/venture.md"])
        self.assertEqual([f["rule"] for f in result["findings"]], ["NUM-BASIS"])
        code, result = self.run_cli("--no-candidates")
        self.assertEqual((code, result["findings"]), (0, []))
        self.assertEqual(result["documents"], ["venture.md"])


if __name__ == "__main__":
    unittest.main()
