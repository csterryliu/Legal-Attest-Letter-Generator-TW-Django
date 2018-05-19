import logging
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed,\
    HttpResponseServerError
import json
import os
import uuid
import datetime
from lal_web.generator.lal_module import core

logger = logging.getLogger('lal_web')


def main_page(request):
    return render(request, 'main.html')


def generate(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    try:
        logger.debug(request.body)
        data = json.loads(request.body.decode('utf-8'))
        logger.debug(data)
        text_path, letter_path = core.generate_text_and_letter(
            data['senders'],
            data['senders_addr'],
            data['receivers'],
            data['receivers_addr'],
            data['ccs'],
            data['ccs_addr'],
            data['content'])
        temp_filename =\
            ('/tmp/%s-%s.pdf' % (str(uuid.uuid4()),
             '{0:%Y-%m-%d-%H-%M-%S-%f}'.format(datetime.datetime.now())))
        core.merge_text_and_letter(text_path, letter_path, temp_filename)
        core.clean_temp_files(text_path, letter_path)
    except Exception as e:
        error_str = ('Failed to generate pdf: %s' % str(e))
        logger.error(error_str)
        return HttpResponseServerError(error_str)
    pdf_file = open(temp_filename, 'rb')
    response = HttpResponse(pdf_file, content_type='application/pdf')
    os.remove(temp_filename)
    return response


def add_info(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    role = request.POST.get('role', '')
    role_name = request.POST.get('roleName', '')
    role_addr = request.POST.get('roleAddr', '')
    num_of_info = request.POST.get('num_of_info', 1)

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
