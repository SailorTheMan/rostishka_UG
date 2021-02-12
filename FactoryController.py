import requests
import json
import time
import asyncio
from time import sleep

ASYNC_SLEEP_TIME = 0.05
DEFAULT_ACCEPT_TIME = 2.7

'''         JSON EXAMPLE
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
            #print(query)
            self.value = requests.get(query).json()[0]['value']
        
        
        return(self.value)

    def set_value(self, value):
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
        self.machines = {}
        self.run = self.attach_tag("FACTORY I/O (Run)")
        #self.check_simstat()

    # creates new tag object
    def attach_tag(self, tag_name, tag_id=''):
        temp_tag = Tag(self.address, tag_name, tag_id)
        self.tag_table.append(temp_tag)
        return temp_tag
    
    def attach_machine(self, name, machine):
        self.machines[name] = machine
        return machine

        
    ### WRITES BY-NAME
    def batch_write(self, payload):
        requests.put(self.address+'/api/tag/values/by-name', json=payload)
    
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
            # print('Controller: Start simulation!')
            return 0
        else:
            return 1



class Conveyor():
    # busy
    # actuator
    # laser
    # (rfid)
    # 
    def __init__(self, conv_tag: Tag, end_laser: Tag, rfid_reader=()):
        self.actuator = conv_tag
        self.laser = end_laser
        self.busy = False
        self.tasks = asyncio.Queue()        # queue for upcoming tasks

        if rfid_reader != ():
            self.rfid_command, self.rfid_exec, self.rfid_iread, self.rfid_stat = rfid_reader
        # rfid stuff

    async def move(self):
        
        while( self.laser.get_value() == True ): 
            await asyncio.sleep(ASYNC_SLEEP_TIME)
            if self.actuator.value != True:
                self.actuator.set_value(True)
        self.actuator.set_value(False)
        return('1')

    async def accept(self):
        self.busy = True
        self.actuator.set_value(True)
        await self.move()

    async def transit_next(self):
        while( self.laser.get_value() == False ): 
            await asyncio.sleep(ASYNC_SLEEP_TIME)
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
            # print(rfid_data)
            None
        elif (rfid_error == 1):
            print("Error No Tag")
        elif (rfid_error == 2):
            print("Error Too Many Tags")
        else:
            print('Another Error')
        self.rfid_exec.set_value('false')

        return(rfid_data)

class Conv_Series(Conveyor):
    def __init__(self, end_laser: Tag, *convs, rfid_reader=()):
        super().__init__(convs[0], end_laser, rfid_reader)
        self.conv_chain = convs

    async def move(self):
        self.busy = True
        while( self.laser.get_value() == True ): 
            await asyncio.sleep(ASYNC_SLEEP_TIME)
            if self.conv_chain[0].value != True:
                for conv in self.conv_chain:
                    conv.set_value(True)
        for conv in self.conv_chain:
           conv.set_value(False)
        return('1')


class Crossing_conveyor():

    def __init__(self, forw_tag, back_tag, left_tag, right_tag, capacity, laser_out, stop_tag = None, wait_time=DEFAULT_ACCEPT_TIME):
        self.forward = forw_tag
        self.back = back_tag
        self.left = left_tag
        self.right = right_tag
        self.capacity = capacity
        self.laser = laser_out
        self.stop_tag = stop_tag        # barrier 
        self.wait_time = wait_time
        
        self.tasks = asyncio.Queue()
        self.directions = {'forward': self.forward, 'back': self.back, 'left': self.left, 'right': self.right }
    
    async def accept_to(self, direction):
        #self.stop_tag.set_value(True)
        self.directions[direction].set_value(True)
        while( self.capacity.get_value() == True ): 
            if self.directions[direction].value != True:
                self.directions[direction].set_value(True)      # a little http optimiztion
            await asyncio.sleep(ASYNC_SLEEP_TIME)
        await asyncio.sleep(self.wait_time)            # a little delay for better positioning
        self.directions[direction].set_value(False)
        return(1)
    
    async def move_to(self, direction):         ## TODO multidirectional move
        self.directions[direction].set_value(True)
        await asyncio.sleep(3)
        self.directions[direction].set_value(False)
        return(1)

class Junction:
    def __init__(self, ct_: Crossing_conveyor, ct_a: Crossing_conveyor):
        self.ct_a = ct_
        self.ct_b = ct_a
        self.tasks = asyncio.Queue()
    
    async def transit_ab(self):
        await asyncio.gather(self.ct_.move_to('left'), self.ct_a.accept_to('right'))

    async def transit_ba(self):
        await asyncio.gather(self.ct_a.move_to('left'), self.ct_.accept_to('right'))


class Crane:
    # my first class)))

    def __init__(self, 
                mov_x_a: Tag,
                mov_z_a: Tag,
                targ_pos_a: Tag,
                at_mid_a: Tag,
                at_left_a: Tag,
                at_right_a: Tag,
                fork_left_a: Tag,
                fork_right_a: Tag,
                lift_a: Tag):

        self.mov_x_a = mov_x_a
        self.mov_z_a = mov_z_a
        self.targ_pos_a = targ_pos_a
        self.at_mid_a = at_mid_a
        self.at_left_a = at_left_a
        self.at_right_a = at_right_a
        self.fork_left_a = fork_left_a
        self.fork_right_a = fork_right_a
        self.lift_a = lift_a

        self.busy = False


    async def to_shelf(self, number):
        right = False
        # number - 1-54 левая сторона 55-108 - правая сторона
        if (number > 54): 
            number = number % 54
            right = True
        # мозг устал простите:
        if (number == 108): number = 54
        self.busy = True


        self.fork_left_a.set_value(True)
        while(not(self.at_left_a.get_value())): await asyncio.sleep(0.1)

        self.lift_a.set_value(True)
        await asyncio.sleep(0.1)
        while(not(self.mov_z_a.get_value())): await asyncio.sleep(0.1)


        self.fork_left_a.set_value(False)
        while(not((self.at_mid_a.get_value()))): await asyncio.sleep(0.1)

    
        self.targ_pos_a.set_value(number)
        await asyncio.sleep(0.1)
        while (self.mov_z_a.get_value() or self.mov_x_a.get_value()): await asyncio.sleep(0.1)

        if (right):
            self.fork_right_a.set_value(True)
            while(not(self.at_right_a.get_value())): await asyncio.sleep(0.1)
        else:
            self.fork_left_a.set_value(True)
            while(not(self.at_left_a.get_value())): await asyncio.sleep(0.1)

        self.lift_a.set_value(False)
        await asyncio.sleep(0.1)
        while(self.mov_z_a.get_value()): await asyncio.sleep(0.1)
        
        if(right):
            self.fork_right_a.set_value(False)
        else:
            self.fork_left_a.set_value(False)
        while(not(self.at_mid_a.get_value())): await asyncio.sleep(0.1)

        self.targ_pos_a.set_value(55)
        await asyncio.sleep(0.1)
        while(self.mov_z_a.get_value()) or self.mov_x_a.get_value(): await asyncio.sleep(0.1)


    async def from_shelf(self, number):
        right = False
        # number - 1-54 левая сторона 55-108 - правая сторона
        if (number > 54): 
            number = number % 54
            right = True
        # мозг устал простите:
        if (number == 108): number = 54
        self.busy = True

        self.targ_pos_a.set_value(number)
        await asyncio.sleep(0.1)
        while (self.mov_z_a.get_value() or self.mov_x_a.get_value()): await asyncio.sleep(0.1)

        if (right):
            self.fork_right_a.set_value(True)
            while(not(self.at_right_a.get_value())): await asyncio.sleep(0.1)
        else:
            self.fork_left_a.set_value(True)
            while(not(self.at_left_a.get_value())): await asyncio.sleep(0.1)
    
        self.lift_a.set_value(True)
        await asyncio.sleep(0.1)
        while(not(self.mov_z_a.get_value())): await asyncio.sleep(0.1)

        if (right):
            self.fork_right_a.set_value(False)
        else:
            self.fork_left_a.set_value(False)
        while(not((self.at_mid_a.get_value()))): await asyncio.sleep(0.1)

        self.targ_pos_a.set_value(55)
        await asyncio.sleep(0.1)
        while(self.mov_z_a.get_value()) or self.mov_x_a.get_value(): await asyncio.sleep(0.1)
        
        
        self.fork_right_a.set_value(True)
        while(not(self.at_right_a.get_value())): await asyncio.sleep(0.1)
    
        self.lift_a.set_value(False)
        await asyncio.sleep(0.1)
        while(self.mov_z_a.get_value()): await asyncio.sleep(0.1)
        
        self.fork_right_a.set_value(False)
        while(not(self.at_mid_a.get_value())): await asyncio.sleep(0.1)
