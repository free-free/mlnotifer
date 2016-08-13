# coding:utf-8

import imaplib
import email


class ImapReceiver(imaplib.IMAP4_SSL):
    
    def __init__(self, host, user, password):
        self._host = host
        self._user = user
        self._passwd = password
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
    
    def get_recent_mail_header(self, mailbox="INBOX", readonly=False):
        self.select(mailbox, readonly)
        typ, data = self.search(None, "NEW")
        msg_set = data[0].split()[::-1]
        msg_headers = []
        for msg_id in msg_set:
            try:
                typ, data = self.fetch(msg_id, '(BODY[HEADER])')
                msg_headers.append(dict(email.message_from_string(data[0][1].decode())))
            except Exception:
                print("get mail %s error" % msg_id)
        return msg_headers
    
    
#recv = ImapReceiver(HOST, USERNAME, PASSWORD)
#recv.active_receiver()
#print(recv.get_total_mail_num())
#print(recv.get_recent_mail_num())
#print(recv.get_recent_mail_header(readonly=True))
#exit()
if __name__ == '__main__':
    imap_server = imaplib.IMAP4_SSL(HOST)
    imap_server.login(USERNAME, PASSWORD)
    msgnums = imap_server.select(readonly=True)
    #print(imap_server.recent())
    #exit()
    typ, data = imap_server.search(None, 'NEW')
    # reverse msg id 
    data = data[0].split()[::-1]
    msg = []
    for msgid in data:
        try:
            typ, data = imap_server.fetch(msgid, '(BODY[HEADER])') 
            header_dict = dict(email.message_from_string(data[0][1].decode()))
            msg.append(header_dict)
        except Exception as e:
            print(e)
            print("get mail %s failed!" % msgid)
    print(msg)
