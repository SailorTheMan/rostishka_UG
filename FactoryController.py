import requests
import json
import time

'''
{
    "name": "Reset light",
    "id": "55a717c5-0bfc-4398-a3b0-f9855cad38e9",
    "address": 15,
    "type": "Bit",
    "kind": "Output",
    "value": false,
    "openCircuit": false,
    "shortCircuit": false,
    "isForced": false,
    "forcedValue": false
}

'''
class Tag:
    self.name
    self.type
    self.address
    self.last_value

    def __init__(self, address, name):
        self.name = name
        self.type = tag_type
        self.address = address
    
    def get_value(self):
        self.last_value = requests.get(self.address+'/api/tags?name='+self.name).json()[0]['value']
        return(self.last_value)

    def set_value(self, value):
        payload = [
        {
            "name": self.name,
            "value": value
        },        ]

        requests.put(address+'/api/tags?name='+self.name, json=payload)

'''
class O_Tag(Tag):
    self.name
    self.type

    def __init__(self, address, name):
        super().__init__(address)
    
    def get_value(value):
        return(requests.get('http://127.0.0.1:7410/api/tags?name='+self.name).json()[0]['value'])

class I_Tag:
    self.name
    self.type

    def __init__(self, name, tag_type):
        self.name = name
        self.type = tag_type
    
    def get_value(value):
        return(requests.get('http://127.0.0.1:7410/api/tags?name='+self.name).json()[0]['value'])

class M_Tag:
    self.name
    self.type

    def __init__(self, name, tag_type):
        self.name = name
        self.type = tag_type
    
    def get_value(value):
        return(requests.get('http://127.0.0.1:7410/api/tags?name='+self.name).json()[0]['value'])
'''


class FIO_Controller:
    self.Memory = []
    self.Input = []
    self.Output = []

    rc11 = Tag("RC (4m) 1.1")
    

    def attach_tag(tag_name)

    def __init__(self, address):
        rc11 = Tag("RC (4m) 1.1")
        #Memory.append() rc12 = MemoryMap.Instance.GetBit("RC (6m) 1.2", MemoryType.Output);
