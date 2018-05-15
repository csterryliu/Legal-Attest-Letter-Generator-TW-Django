#Copyright ReportLab Europe Ltd. 2000-2012
#see license.txt for license details
#history http://www.reportlab.co.uk/cgi-bin/viewcvs.cgi/public/reportlab/trunk/reportlab/tools/docco/yaml.py
# parses "Yet Another Markup Language" into a list of tuples.
# Each tuple says what the data is e.g.
# ('Paragraph', 'Heading1', 'Why Reportlab Rules')
# and the pattern depends on type.
"""
Parser for "Aaron's Markup Language" - a markup language
which is easier to type in than XML, yet gives us a
reasonable selection of formats.

The general rule is that if a line begins with a '.',
it requires special processing. Otherwise lines
are concatenated to paragraphs, and blank lines
separate paragraphs.

If the line ".foo bar bletch" is encountered,
it immediately ends and writes out any current
paragraph.

It then looks for a parser method called 'foo';
if found, it is called with arguments (bar, bletch).

If this is not found, it assumes that 'foo' is a
paragraph style, and the text for the first line
of the paragraph is 'bar bletch'.  It would be
up to the formatter to decide whether on not 'foo'
was a valid paragraph.

Special commands understood at present are:
.image filename
- adds the image to the document
.beginPre Code
- begins a Preformatted object in style 'Code'
.endPre
- ends a preformatted object.
"""


import sys
import imp
from . import codegrab

#modes:
PLAIN = 1
PREFORMATTED = 2

BULLETCHAR = '\267'  # assumes font Symbol, but works on all platforms

class Parser:
    def __init__(self):
        self.reset()

    def reset(self):
        self._lineNo = 0
        self._style = 'Normal'  # the default
        self._results = []
        self._buf = []
        self._mode = PLAIN

    def parseFile(self, filename):
        #returns list of objects
        data = open(filename, 'r').readlines()

        for line in data:
            #strip trailing newlines
            self.readLine(line[:-1])
        self.endPara()
        return self._results

    def readLine(self, line):
        #this is the inner loop
        self._lineNo = self._lineNo + 1
        stripped = line.lstrip()
        if len(stripped) == 0:
            if self._mode == PLAIN:
                self.endPara()
            else:  #preformatted, append it
                self._buf.append(line)
        elif line[0]=='.':
            # we have a command of some kind
            self.endPara()
            words = stripped[1:].split()
            cmd, args = words[0], words[1:]

            #is it a parser method?
            if hasattr(self.__class__, cmd):
                #this was very bad; any type error in the method was hidden
                #we have to hack the traceback
                try:
                    getattr(self,cmd)(*args)
                except TypeError as err:
                    sys.stderr.write("Parser method: %s(*%s) %s at line %d\n" % (cmd, tuple(args), err, self._lineNo))
                    raise
            else:
                # assume it is a paragraph style -
                # becomes the formatter's problem
                self.endPara()  #end the last one
                words = stripped.split(' ', 1)
                assert len(words)==2, "Style %s but no data at line %d" % (words[0], self._lineNo)
                (styletag, data) = words
                self._style = styletag[1:]
                self._buf.append(data)
        else:
            #we have data, add to para
            self._buf.append(line)

    def endPara(self):
        #ends the current paragraph, or preformatted block

        text = ' '.join(self._buf)
        if text:
            if self._mode == PREFORMATTED:
                #item 3 is list of lines
                self._results.append(('Preformatted', self._style,
                                 '\n'.join(self._buf)))
            else:
                self._results.append(('Paragraph', self._style, text))
        self._buf = []
        self._style = 'Normal'

    def beginPre(self, stylename):
        self._mode = PREFORMATTED
        self._style = stylename

    def endPre(self):
        self.endPara()
        self._mode = PLAIN

    def image(self, filename):
        self.endPara()
        self._results.append(('Image', filename))

    def vSpace(self, points):
        """Inserts a vertical spacer"""
        self._results.append(('VSpace', points))

    def pageBreak(self):
        """Inserts a frame break"""
        self._results.append(('PageBreak','blah'))  # must be a tuple

    def custom(self, moduleName, funcName):
        """Goes and gets the Python object and adds it to the story"""
        self.endPara()
        self._results.append(('Custom',moduleName, funcName))



    def getModuleDoc(self, modulename, pathname=None):
        """Documents the entire module at this point by making
        paragraphs and preformatted objects"""
        docco = codegrab.getObjectsDefinedIn(modulename, pathname)
        if docco.doc != None:
            self._results.append(('Paragraph', 'DocString', docco.doc))
        if len(docco.functions) > 0:
            for fn in docco.functions:
                if fn.status == 'official':
                    self._results.append(('Preformatted','FunctionHeader', fn.proto))
                    self._results.append(('Preformatted','DocString', fn.doc))

        if len(docco.classes) > 0:
            for cls in docco.classes:
                if cls.status == 'official':
                    self._results.append(('Preformatted','FunctionHeader', 'Class %s:' % cls.name))
                    self._results.append(('Preformatted','DocString', cls.doc))
                    for mth in cls.methods:
                        if mth.status == 'official':
                            self._results.append(('Preformatted','FunctionHeader', mth.proto))
                            self._results.append(('Preformatted','DocStringIndent', mth.doc))


    def getClassDoc(self, modulename, classname, pathname=None):
        """Documents the class and its public methods"""
        docco = codegrab.getObjectsDefinedIn(modulename, pathname)
        found = 0
        for cls in docco.classes:
            if cls.name == classname:
                found = 1
                self._results.append(('Preformatted','FunctionHeader', 'Class %s:' % cls.name))
                self._results.append(('Preformatted','DocString', cls.doc))
                for mth in cls.methods:
                    if mth.status == 'official':
                        self._results.append(('Preformatted','FunctionHeader', mth.proto))
                        self._results.append(('Preformatted','DocStringIndent', mth.doc))
                break
        assert found, 'No Classes Defined in ' + modulename

    def nextPageTemplate(self, templateName):
        self._results.append(('NextPageTemplate',templateName))

if __name__=='__main__': #NORUNTESTS
    if len(sys.argv) != 2:
        print('usage: yaml.py source.txt')
    else:
        p = Parser()
        results = p.parseFile(sys.argv[1])
        import pprint
        pprint.pprint(results)
