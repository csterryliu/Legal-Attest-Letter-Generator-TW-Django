# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import logging

logger = logging.getLogger('lal_web')

def main_page(request):
    logger.debug('main')
    return render(request, 'main.html')
