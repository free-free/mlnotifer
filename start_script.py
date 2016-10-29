# coding:utf-8

from mlnotifer import *
from config import config


def email_notify(conf):
    host = conf.get("host")
    user = conf.get("user")
    password = conf.get("password")
    port = conf.get("port")
    mail_recv = ImapReceiver(host, user, password, port)
    mail_recv.activate_receiver()
    print(mail_recv.get_recent_mail_header())

def starter():
    cgroups = config.get("groups", [])
    for conf in cgroups:
        email_notify(conf)
    
if __name__ == "__main__":
    starter()    
