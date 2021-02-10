import requests
import json
import time
import asyncio
from time import sleep

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

    def __init__(self, address, name, tag_id=''):
        self.name = name
        self.address = address
        self.id = tag_id
        

    
    def get_value(self):                            # dunno why but brakes encoding otherwise
        if self.id != '':
            query = self.address+'/api/tags/'+self.id
            self.value = requests.get(query).json()['value']
        else:
            query = self.address+'/api/tags?name='+self.name
            self.value = requests.get(query).json()[0]['value']
        #print(query)
        
        return(self.value)

    def set_value(self, value):
        if value == False:
            value = "false"
        if value == True:
            value = "true"
        self.value = value
        
        #print(payload)
        if self.id != '':
            query = self.address+'/api/tag/values'
            payload = [   {
                "id": self.id,
                "value": self.value
            },        ]
            #print(query)
            #print(payload)
        else:
            query = self.address+'/api/tag/values/by-name'
            payload = [   {
                "name": self.name,
                "value": self.value
            },        ]
        requests.put(query, json=payload)


class FIO_Controller:
    
    def __init__(self, address):
        self.address = address
        self.tag_table = []

        self.run = self.attach_tag("FACTORY I/O (Run)")
        #self.check_simstat()

    # creates new tag object
    def attach_tag(self, tag_name, tag_id=''):
        temp_tag = Tag(self.address, tag_name, tag_id)
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


'''class Machine:

    def __init__(self, tag: Tag, ):
        self.actuator = tag'''

class Conveyor():
    # busy
    # actuator
    # laser
    # (rfid)
    # 
    def __init__(self, conv_tag: Tag, end_laser: Tag, rfid_reader=()):
        self.actuator = conv_tag
        self.laser = end_laser
        if rfid_reader != ():
            self.rfid_command, self.rfid_exec, self.rfid_iread, self.rfid_stat = rfid_reader
        # rfid stuff

    async def move(self):
        self.busy = True
        while( self.laser.get_value() == True ): 
            await asyncio.sleep(0.05)
            if self.actuator.value != True:
                self.actuator.set_value(True)
        self.actuator.set_value(False)
        return('1')
    
    async def transit_next(self):
        while( self.laser.get_value() == False ): 
            await asyncio.sleep(0.05)
            if self.actuator.value != True:
                self.actuator.set_value(True)
        self.actuator.set_value(False)
        self.busy = False

    def read_rfid(self):
        self.rfid_command.set_value(1)
        self.rfid_exec.set_value('true')
        rfid_data = self.rfid_iread.get_value()
        rfid_error = self.rfid_stat.get_value()

        if (rfid_error == 0):
            print(rfid_data)
        elif (rfid_error == 1):
            print("Error No Tag")
        elif (rfid_error == 2):
            print("Error Too Many Tags")
        else:
            print('Another Error')
        self.rfid_exec.set_value('false')

        return(rfid_data)
