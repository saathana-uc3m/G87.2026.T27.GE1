'''Enterprise request logic'''

import json

class EnterpriseRequest:
    '''Enterprise request class'''
    def __init__(self, cif, phone, e_name):
        '''Initialize enterprise request class'''
        self.__enterprise_name = e_name
        self.__cif = cif
        self.__phone = phone

    def __str__(self):
        return "Enterprise:" + json.dumps(self.__dict__)

    @property
    def enterprise_cif(self):
        '''get CIF value'''
        return self.__cif
    @enterprise_cif.setter
    def enterprise_cif(self, value):
        '''set CIF value'''
        self.__cif = value

    @property
    def phone_number(self):
        '''get phone number'''
        return self.__phone
    @phone_number.setter
    def phone_number(self, value):
        '''set phone number'''
        self.__phone = value

    @property
    def enterprise_name(self):
        '''get enterprise name'''
        return self.__enterprise_name
    @enterprise_name.setter
    def enterprise_name(self, value):
        '''set enterprise name'''
        self.__enterprise_name = value
