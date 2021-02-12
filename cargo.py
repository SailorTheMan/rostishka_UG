
import asyncio
import FactoryController as fio



class Cargo:
    def __init__(self, controller: fio.FIO_Controller, rfid=None, position='en route', destination=-1 ):
        self.controller = controller
        
        self.external_id = 0
        self.rf_id = rfid
        self.current_position = position
        self.crane = destination // 2
        self.destination = destination            # TODO check all known positions and racks
        self.route_commands = asyncio.Queue()
        self.machines = asyncio.Queue()
    '''
    async def plan_route(self, crane):        # lays route to a certain crane for now
        cntrl = self.controller
        com_qu = self.route_commands

        
        self.machines.put_nowait('JN1')
        self.machines.put_nowait('Arc1')
        
        await asyncio.gather(cntrl.machines['RC1'].transit_next(), cntrl.machines['CT1'].accept_to('from'))
        await cntrl.machines['CT1'].move_to()
        await cntrl.machines['RC1'].tasks.put(task2)

        
        com_qu.get()
        if cntrl.machines['CT1'].tasks.empty():
            pass
    '''
    async def execute(self):
        if self.crane == 1:
            pass
        
        if self.crane == 2:
            ctrl_m = self.controller.machines
            await asyncio.gather(ctrl_m['RC1'].transit_next(), ctrl_m['CT1'].accept_to('forward'))
            await ctrl_m['CT1'].move_to('forward')
            await ctrl_m['Bridge1'].move_to('forward')
        
        



class Storekeeper:
    def __init__(self, controller):
        self.active_cargo = {}   # dictionary for all cargos en route | [rfid]: Cargo()
        self.controller = controller

    def add_cargo(self, new_cargo: Cargo):
        self.active_cargo[new_cargo.rf_id] = new_cargo

