#!/bin/env python
#Copyright ReportLab Europe Ltd. 2000-2016
#see license.txt for license details
__doc__='Test all demos'
__version__='3.3.0'
_globals=globals().copy()
import os, sys
from reportlab import pdfgen

for p in ('pythonpoint/pythonpoint.py','stdfonts/stdfonts.py','odyssey/odyssey.py', 'gadflypaper/gfe.py'):
    fn = os.path.normcase(os.path.normpath(os.path.join(os.path.dirname(pdfgen.__file__),'..','demos',p)))
    os.chdir(os.path.dirname(fn))
    exec(compile(open(fn).read(), fn, 'exec'),_globals.copy())
