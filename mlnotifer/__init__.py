# -*- encoding:utf-8 -*-

import re
from notifer import TwilioSMSNotifer
from mlfetcher import IMAPFetcher




_IMAP_HOST = {
    'qq': 'imap.qq.com',
    '163': 'imap.163.com',
    'gmail': 'imap.gmail.com'
}


def get_imap_host(email_addr):
    email_type = re.findall('[a-zA-Z0-9_-]+@([0-9a-zA-Z-_]+).[0-9a-zA-Z]+',\
        email_addr)
    try:
        return _IMAP_HOST.get(email_type[0], '')
    except IndexError:
        return ''


class Mlnofiter(object):

    def __init__(self):
        pass



