# -*- encoding:utf-8 -*-

import abc
from twilio.rest import Client


class SMSNotifer(object):

    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def notify(self,from_, to_, body):
        pass



class TwilioSMSNotifer(SMSNotifer):


    def __init__(self, acount_id=None, token=None):
        super(SMSDriver, self).__init__()
        self._twilio_client = Client(acount_id, token)
        
    def send(self, from_, to_, body):
        self._twillio_client.messages.create(to=to_,\
            from_=from_, body=body)


class SubmailSMSNotifer(SMSNotifer):
    
    
    def send(self, from_, to_, body):
        pass

