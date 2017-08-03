# -*- encoding:utf-8 -*-

import abc
from twilio.rest import Client


class SMSNotifer(object):

    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def notify(self,from_, to_, body):
        pass



class TwilioSMSNotifer(SMSNotifer):

    SV = 'twilio'


    def __init__(self, sid=None, token=None):
        super(SMSNotifer, self).__init__()
        self._twilio_client = Client(sid, token)
        
    def notify(self, from_, to_, body):
        self._twillio_client.messages.create(to=to_,\
            from_=from_, body=body)


class SubmailSMSNotifer(SMSNotifer):
    
    SV = 'submail'


    def notify(self, from_, to_, body):
        pass


def get_notifers():
    """
    get all notifer class
    return the list of notifer class
    """
    def get_subclasses(cls):
        subclasses = set()
        for subclass in cls.__subclasses__():
            subclasses.add(subclass)
            subclasses.update(get_subclasses(subclass))
        return subclasses
    return [notifer for notifer in list(get_subclasses(SMSNotifer))\
            if hasattr(notifer, 'SV') and notifer.SV]


def get_notifer_by_sv(sv=None):
    """
    returns: notifer class
    """
    if not sv or type(sv) is not str:
        raise TypeError("Invalid sv %s" % sv)
    selected_notifers = list(filter(lambda notifer: hasattr(notifer, 'SV') \
        and notifer.SV == sv, get_notifers()))
    if len(selected_notifers) == 0:
        raise ValueError("Can't found notifer for sv '%s'" % sv)
    else:
        return selected_notifers[0]


