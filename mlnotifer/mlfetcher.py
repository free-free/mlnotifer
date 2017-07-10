# -*- encoding:utf-8 -*-

import re
import sys
import functools
import email
from imapclient import IMAPClient
from twilio.rest import Client


EMAIL_ADDR_REG = '[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+.[a-zA-Z0-9_-]+'


def _imap_login_checker(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self._is_login:
            try:
                self.login()
            except Exception:
                return
        return func(self, *args, **kwargs)
    return wrapper


class IMAPFetcher(object):
    

    def __init__(self, host, user, password):
        self._host = host
        self._user = user
        self._passwd = password
        self._is_login = False
        self._imap_client = IMAPClient(self._host)

    @property
    def is_login(self):
        return self._is_login
    
    @is_login.setter
    def is_login(self, value):
        raise AttributeError()
    
    def login(self, user='', password=''):
        username = user or self._user
        passwd = password or self._passwd
        try:
            self._imap_client.login(username, passwd)
        except self._imap_client.Error:
            self._is_login = False
            print("Login failed!")
            raise Exception("Login failed")
        else:
            self._is_login = True
        
    @_imap_login_checker
    def fetch(self):
        '''
            fetch email's subject and sender
            then return a list that each item is
            list type which has two element, first element is sender 
            email and second element is email's subject
        '''
        ret = []
        self._imap_client.select_folder('INBOX', readonly=True)
        msg_id_list = self._imap_client.search("UNSEEN")
        msg_dict = self._imap_client.fetch(msg_id_list,'BODY[HEADER]')
        for msg_id, msg in msg_dict.items():
            e = email.message_from_string(msg[b'BODY[HEADER]'].decode())
            subject = str(email.header.make_header(\
                email.header.decode_header(e['SUBJECT'])))
            from_ = str(email.header.make_header(\
                email.header.decode_header(e['From'])))
            from_ = re.findall(EMAIL_ADDR_REG, from_)[0]
            ret.append([from_, subject])
        return ret
