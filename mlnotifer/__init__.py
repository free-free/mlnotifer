# -*- encoding:utf-8 -*-

import re
import os
import yaml

from notifer import get_notifer_by_sv
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

def get_profile(profile_path=None):
    profile_path = profile_path or os.path.join(os.path.dirname(\
        os.path.dirname(os.path.realpath(__file__))), 'profile.yaml')
    try:
        with open(profile_path, 'r+') as f:
            profile = yaml.load(f)
    except IOError as e:
        print(e)
        print("No profile exists! please check your profile")
    return profile


class Client(object):

    def __init__(self):
        self._notifer = None

    def setup_notifer(self, notifer_name, notifer_acount):
        if not isinstance(notifer_acount, dict):
            raise TypeError("NO notifer acount information found")
        self._notifer = get_notifer_by_sv(notifer_name)(**notifer_acount)

    def run(self):
        profile = get_profile()
        self.setup_notifer(profile.get('notifer','twilio'),\
            profile.get('twilio')),


if __name__ == '__main__':
    Client().run()
