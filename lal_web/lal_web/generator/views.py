# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import logging

logger = logging.getLogger('lal_web')


def main_page(request):
    return render(request, 'main.html')


def generate(request):
    sender = request.POST.get('sender')
    sender_addr = request.POST.get('senderAddr')
    receiver = request.POST.get('receiver')
    receiver_addr = request.POST.get('receiverAddr')
    cc = request.POST.get('cc')
    cc_addr = request.POST.get('ccAddr')
    content = request.POST.get('content')
    logger.debug(sender)
    logger.debug(sender_addr)
    logger.debug(receiver)
    logger.debug(receiver_addr)
    logger.debug(cc)
    logger.debug(cc_addr)
    logger.debug(content)
    return HttpResponseRedirect('/')
