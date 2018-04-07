import logging
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,\
    HttpResponseNotAllowed

from lal_web.generator.lal_module import core

logger = logging.getLogger('lal_web')


def main_page(request):
    return render(request, 'main.html')


def generate(request):
    senders = [[request.POST.get('sender')]]
    senders_addr = [request.POST.get('senderAddr')]
    receivers = [[request.POST.get('receiver')]]
    receivers_addr = [request.POST.get('receiverAddr')]
    ccs = [[request.POST.get('cc')]]
    cc_addr = [request.POST.get('ccAddr')]
    content = request.POST.get('content')
    logger.debug(senders)
    logger.debug(senders_addr)
    logger.debug(receivers)
    logger.debug(receivers_addr)
    logger.debug(ccs)
    logger.debug(cc_addr)
    logger.debug(content)
    text_path, letter_path = core.generate_text_and_letter(senders,
                                                           senders_addr,
                                                           receivers,
                                                           receivers_addr,
                                                           ccs,
                                                           cc_addr,
                                                           content)
    logger.debug(text_path)
    logger.debug(letter_path)
    core.merge_text_and_letter(text_path, letter_path, 'test.pdf')
    core.clean_temp_files(text_path, letter_path)
    logger.debug('done')
    return HttpResponseRedirect('/')


def add_info(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    sender = request.GET.get('sender', '')
    sender_addr = request.GET.get('senderAddr', '')
    receiver = request.GET.get('receiver', '')
    receiver_addr = request.GET.get('receiverAddr', '')
    cc = request.GET.get('cc', '')
    cc_addr = request.GET.get('ccAddr', '')
    num_of_info = request.GET.get('num_of_info', 1)

    ret_value = {
        'sender': sender,
        'sender_addr': sender_addr,
        'receiver': receiver,
        'receiver_addr': receiver_addr,
        'cc': cc,
        'cc_addr': cc_addr,
        'num_of_info': num_of_info
    }

    return render(request, 'info_card.html', ret_value)
