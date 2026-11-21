"""Checks derived readers preserve native sources and contain hostile text safely."""
import json
import tempfile
import unittest
from pathlib import Path
import result_html


class ResultReaderTests(unittest.TestCase):
    def test_exact_native_source_and_safe_contained_payload(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source='# A source\n\nStatus: candidate\n\n## Conclusion\n\n</script><script>window.injected=true</script> & a choice.\n'
            (root/'venture.md').write_text(source)
            rendered=result_html.render(root)
            payload=rendered.split('<script id="result-data" type="application/json">',1)[1].split('</script>',1)[0]
            self.assertEqual(json.loads(payload)['documents'][0]['text'],source)
            self.assertEqual((root/'venture.md').read_text(),source)
            self.assertNotIn('</script><script>window.injected=true',rendered)
            self.assertNotIn('<script src=',rendered)
            self.assertNotIn('url("fonts/',rendered)

    def test_native_download_retains_original_line_endings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=b'# Source\r\n\r\n## Conclusion\r\n\r\nA choice.\r\n'
            (root/'venture.md').write_bytes(source)
            html=result_html.render(root)
            payload=html.split('<script id="result-data" type="application/json">',1)[1].split('</script>',1)[0]
            self.assertEqual(json.loads(payload)['documents'][0]['text'].encode(),source)

    def test_an_empty_state_remains_a_usable_document(self):
        with tempfile.TemporaryDirectory() as tmp:
            rendered=result_html.render(Path(tmp))
            self.assertIn('No sources match',rendered)
            self.assertIn('result-data',rendered)
            self.assertIn('0 sources',rendered)

    def test_explicit_candidate_working_view_keeps_the_delivered_revision(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'venture.md').write_text('# Current\n\n## Conclusion\n\nCurrent decision.\n')
            (root/'candidate').mkdir();(root/'candidate/venture.md').write_text('# Proposed\n\nStatus: candidate\n\n## Conclusion\n\nProposed revision.\n')
            rendered=result_html.render(root,include_candidates=True)
            payload=rendered.split('<script id="result-data" type="application/json">',1)[1].split('</script>',1)[0]
            docs=json.loads(payload)['documents']
            self.assertEqual(len(docs),1)
            self.assertEqual(docs[0]['file'],'candidate/venture.md')
            self.assertIn('Proposed revision.',docs[0]['text'])
            self.assertIn('Current decision.',(root/'venture.md').read_text())

    def test_candidates_and_evidence_do_not_overlay_current_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'message-system.md').write_text('# Current\n\n## Conclusion\n\nCurrent source.\n')
            (root/'candidate').mkdir();(root/'candidate/message-system.md').write_text('UNACCEPTED OVERLAY')
            (root/'evidence').mkdir();(root/'evidence/private.md').write_text('PRIVATE EVIDENCE')
            rendered=result_html.render(root)
            self.assertIn('Current source.',rendered)
            self.assertNotIn('UNACCEPTED OVERLAY',rendered)
            self.assertNotIn('PRIVATE EVIDENCE',rendered)

if __name__=='__main__':unittest.main()
