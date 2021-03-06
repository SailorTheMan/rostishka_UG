
import asyncio
import FactoryController as fio



class Cargo:
    def __init__(self, controller: fio.FIO_Controller, rfid=None, position='en route', destination=-1 ):
        self.controller = controller
        
        self.external_id = 0
        self.rf_id = rfid
        self.current_position = position
        self.destination = destination            # TODO check all known positions and racks
        self.route_commands = asyncio.Queue()

    def plan_route(self, crane):        # lays route to a certain crane for now
        cntrl = self.controller
        com_qu = self.route_commands

        if crane == 1:
            self.route_commands.put(cntrl.machines['RC1'].move())

        
        com_qu.get()
        if cntrl.machines['CT1'].tasks.empty():
            pass

class Storekeeper:
    def __init__(self, controller):
        self.active_cargo = {}   # dictionary for all cargos en route | [rfid]: Cargo()
        self.controller = controller

    def add_cargo(self, new_cargo: Cargo):
        self.active_cargo[new_cargo.rf_id] = new_cargo

