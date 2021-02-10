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

    def __init__(self, address, name):
        self.name = name
        self.address = address

    
    def get_value(self):                            # dunno why but brakes encoding otherwise
        self.value = requests.get(self.address+'/api/tags?name='+self.name).json()[0]['value']
        return(self.value)

    def set_value(self, value):
        if value == False:
            value = "false"
        if value == True:
            value = "true"
        self.value = value
        payload = [
        {
            "name": self.name,
            "value": value
        },        ]
        #print(payload)
        requests.put(self.address+'/api/tag/values/by-name', json=payload)


class FIO_Controller:
    
    def __init__(self, address):
        self.address = address
        self.tag_table = []

        self.run = self.attach_tag("FACTORY I/O (Run)")
        self.check_simstat()

    # creates new tag object
    def attach_tag(self, tag_name):
        temp_tag = Tag(self.address, tag_name)
        self.tag_table.append(temp_tag)
        return temp_tag
        
    ### WRITES BY-NAME
    def batch_write(self, payload):
        requests.put(self.address+'/api//tag/values/by-name', json=payload)
    
    def fetch_tags(self):
        for tg in self.tag_table:
            tg.get_value()

    def push_tags(self):
        for tg in self.tag_table:
            tg.set_value(tg.value)        

    def sim_start(self):
        self.run.set_value("true")
    
    def sim_pause(self):
        pass

    def check_simstat(self):
        if self.run.get_value() != 'true':
            print('Controller: Start simulation!')
            return 0
        else:
            return 1


