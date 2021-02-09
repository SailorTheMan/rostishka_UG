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
    #self.name
    #self.type
    #self.address
    #self.last_value

    def __init__(self, address, name):
        self.name = name
        self.address = address
    
    def get_value(self):
        self.last_value = requests.get(self.address+'/api/tags?name='+self.name).json()[0]['value']
        return(self.last_value)

    def set_value(self, value):
        if value == False:
            value = 'false'
        if value == True:
            value = 'true'

        payload = [
        {
            "name": self.name,
            "value": value
        },        ]

        requests.put(self.address+'/api/tags?name='+self.name, json=payload)


class FIO_Controller:
    
    def __init__(self, address):
        self.address = address
        self.tag_table = []
        
    def attach_tag(self, tag_name):
        temp_tag = Tag(self.address, tag_name)
        self.tag_table.append(temp_tag)
        return temp_tag
    
    def fetch_tags(self):
        for tg in self.tag_table:
            tg.get_value()
