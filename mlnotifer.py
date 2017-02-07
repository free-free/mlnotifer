# coding:utf-8

import imaplib
import email


class ImapReceiver(imaplib.IMAP4_SSL):
    
    def __init__(self, host, user, password, port=None):
        self._host = host
        self._user = user
        self._passwd = password
        self._port = port 
        if self._port:
            super(ImapReceiver, self).__init__(self._host, self._port)
        else:    
            super(ImapReceiver, self).__init__(self._host)
    
    def activate_receiver(self):
        try:
            self.login(self._user, self._passwd)
        except Exception:
            raise Exception("Login Faield")
    
    def get_total_mail_num(self, mailbox="INBOX"):       
        typ, data = self.select(mailbox)
        return int(data[0].decode())

    def get_recent_mail_num(self, mailbox="INBOX"):
        self.select(mailbox)
        typ, data = self.recent()
        return int(data[0].decode())
    
    def get_recent_mail_header(self, mailbox="INBOX", readonly=True):
        self.select(mailbox, readonly)
        typ, data = self.search(None, "RECENT")
        msg_set = data[0].split()[::-1]
        msg_headers = []
        for msg_id in msg_set:
            try:
                typ, data = self.fetch(msg_id, '(BODY[HEADER])')
                msg_headers.append(dict(email.message_from_string(data[0][1].decode())))
            except Exception:
                print("get mail %s error" % msg_id)
        return msg_headers
    
