import unittest
from types import SimpleNamespace
from unittest.mock import patch

from pypdf import PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, NameObject, TextStringObject

import check_public_pdfs


class AnnotationCompatibilityTest(unittest.TestCase):
    def test_direct_and_indirect_annotation_arrays(self):
        writer = PdfWriter()
        annotations = ArrayObject([
            DictionaryObject({NameObject('/A'): DictionaryObject({
                NameObject('/URI'): TextStringObject('mailto:example@example.com')
            })})
        ])
        indirect = writer._add_object(annotations)
        for value in (annotations, indirect, None):
            with self.subTest(annotation_type=type(value).__name__):
                class Page(dict):
                    def extract_text(self):
                        return 'Example resume'

                page = Page() if value is None else Page({'/Annots': value})
                reader = SimpleNamespace(pages=[page], metadata={})
                with patch.object(check_public_pdfs, 'PdfReader', return_value=reader):
                    _, _, uris, _ = check_public_pdfs.read_pdf('unused.pdf')
                self.assertEqual(uris, [] if value is None else ['mailto:example@example.com'])


if __name__ == '__main__':
    unittest.main()
