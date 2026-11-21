"""Compatibility and information-preservation checks for the consolidated views."""
import json
import tempfile
import unittest
from pathlib import Path
import result_html
import view


class TwoViewTests(unittest.TestCase):
    def test_current_and_candidate_can_be_examined_together(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'character.md').write_text('# Current character\n\nStatus: accepted\n\n## Conclusion\n\nCurrent expression.\n')
            (root/'candidate').mkdir();(root/'candidate/character.md').write_text('# Proposed character\n\nStatus: candidate\nChange: update-1\n\n## Conclusion\n\nProposed expression.\n')
            page=result_html.render(root,candidate_mode='compare')
            payload=json.loads(page.split('<script id="result-data" type="application/json">')[1].split('</script>')[0])
            self.assertEqual(len(payload['documents']),2)
            self.assertEqual([d['variant'] for d in payload['documents']],['current','candidate'])
            self.assertIn('candidate-pair',page)
            self.assertIn('Candidate · update-1',page)
            self.assertIn('Current expression.',page)
            self.assertIn('Proposed expression.',page)

    def test_product_scoped_value_references_do_not_collide(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);models=root/'product-value-models';models.mkdir()
            for name in ['one-product','other-product']:
                (models/(name+'.md')).write_text('# Value\n\n## Situations\n\n### SIT-1 · A situation\n\nDevelops MCH-1 and other-product/MCH-1.\n\n### MCH-1 · Mechanism\n\nThe method.\n')
            page=result_html.render(root)
            self.assertIn("id='one-product/SIT-1'",page)
            self.assertIn("id='other-product/SIT-1'",page)
            self.assertIn("href='#other-product/MCH-1'",page)
            self.assertIn("href='#one-product/MCH-1'",page)

    def test_definition_and_result_have_the_same_packaged_visual_sources(self):
        import reader_support
        page=reader_support.tool_shell('Example','Mechanics','Scope.','<h2>Definitions</h2>')
        self.assertIn('Tool guide',page)
        self.assertIn('tool-search',page)
        self.assertIn(reader_support.styles(),page)
        self.assertNotIn('url("fonts/',page)

    def test_candidate_overlay_keeps_its_visible_candidate_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'candidate').mkdir();(root/'candidate/venture.md').write_text('# Proposed\n\nChange: next-choice\n\n## Conclusion\n\nA proposed revision.\n')
            page=result_html.render(root,include_candidates=True)
            self.assertIn('Candidate · next-choice',page)

    def test_record_links_use_the_named_id_column(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'message-system.md').write_text('# Messages\n\n## Message units\n\n| Kind | ID | Point |\n| --- | --- | --- |\n| Idea | MSG-7 | A meaningful choice. |\n\nDevelops MSG-7.\n')
            page=result_html.render(root)
            self.assertIn("id='MSG-7'",page)
            self.assertIn("href='#doc-0--MSG-7'",page)
