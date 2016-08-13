# coding:utf-8

from mlnotifer import *
from config import config

if __name__ == "__main__":
    host = config.get("host")
    user = config.get("user")
    password = config.get("password")
    mail_recv = ImapReceiver(host, user, password)
    mail_recv.active_receiver()
    print(mail_recv.get_recent_mail_header())
