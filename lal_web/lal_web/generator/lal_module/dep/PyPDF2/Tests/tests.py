import os
import sys
import unittest

from PyPDF2 import PdfFileReader, PdfFileWriter


# Configure path environment
TESTS_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(TESTS_ROOT)
RESOURCE_ROOT = os.path.join(PROJECT_ROOT, 'Resources')

sys.path.append(PROJECT_ROOT)


class PdfReaderTestCases(unittest.TestCase):

    def test_PdfReaderFileLoad(self):
        '''
        Test loading and parsing of a file. Extract text of the file and compare to expected
        textual output. Expected outcome: file loads, text matches expected.
        '''

        with open(os.path.join(RESOURCE_ROOT, 'crazyones.pdf'), 'rb') as inputfile:
            # Load PDF file from file
            ipdf = PdfFileReader(inputfile)
            ipdf_p1 = ipdf.getPage(0)

            # Retrieve the text of the PDF
            pdftext_file = open(os.path.join(RESOURCE_ROOT, 'crazyones.txt'), 'r')
            pdftext = pdftext_file.read()
            ipdf_p1_text = ipdf_p1.extractText().replace('\n', '')

            # Compare the text of the PDF to a known source
            self.assertEqual(ipdf_p1_text.encode('utf-8', errors='ignore'), pdftext,
                msg='PDF extracted text differs from expected value.\n\nExpected:\n\n%r\n\nExtracted:\n\n%r\n\n'
                    % (pdftext, ipdf_p1_text.encode('utf-8', errors='ignore')))


class AddJsTestCase(unittest.TestCase):

    def setUp(self):
        ipdf = PdfFileReader(os.path.join(RESOURCE_ROOT, 'crazyones.pdf'))
        self.pdf_file_writer = PdfFileWriter()
        self.pdf_file_writer.appendPagesFromReader(ipdf)

    def test_add(self):

        self.pdf_file_writer.addJS("this.print({bUI:true,bSilent:false,bShrinkToFit:true});")

        self.assertIn('/Names', self.pdf_file_writer._root_object, "addJS should add a name catalog in the root object.")
        self.assertIn('/JavaScript', self.pdf_file_writer._root_object['/Names'], "addJS should add a JavaScript name tree under the name catalog.")
        self.assertIn('/OpenAction', self.pdf_file_writer._root_object, "addJS should add an OpenAction to the catalog.")

    def test_overwrite(self):

        self.pdf_file_writer.addJS("this.print({bUI:true,bSilent:false,bShrinkToFit:true});")
        first_js = self.get_javascript_name()

        self.pdf_file_writer.addJS("this.print({bUI:true,bSilent:false,bShrinkToFit:true});")
        second_js = self.get_javascript_name()

        self.assertNotEqual(first_js, second_js, "addJS should overwrite the previous script in the catalog.")

    def get_javascript_name(self):
        self.assertIn('/Names', self.pdf_file_writer._root_object)
        self.assertIn('/JavaScript', self.pdf_file_writer._root_object['/Names'])
        self.assertIn('/Names', self.pdf_file_writer._root_object['/Names']['/JavaScript'])
        return self.pdf_file_writer._root_object['/Names']['/JavaScript']['/Names'][0]
