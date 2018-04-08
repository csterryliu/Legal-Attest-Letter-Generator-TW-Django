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

    role = request.GET.get('role', '')
    role_name = request.GET.get('roleName', '')
    role_addr = request.GET.get('roleAddr', '')
    num_of_info = request.GET.get('num_of_info', 1)

    role_map = {
        'sender': '寄件人',
        'receiver': '收件人',
        'cc': '副本收件人',
    }

    ret_value = {
        'role': role_map[role],
        'role_name': role_name,
        'role_addr': role_addr,
        'num_of_info': int(num_of_info) + 1
    }

    return render(request, 'info_card.html', ret_value)
