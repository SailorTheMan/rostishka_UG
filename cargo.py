
import asyncio

class Storekeeper:
    def __init__(self):
        self.active_cargo = {}   # dictionary for all cargos en route [rfid]: Cargo()

    def add_cargo(self):
        new_cargo = Cargo()
        return 



class Cargo:
    def __init__(self, rfid=None, position='en route', destination=-1 ):
        self.external_id
        self.rf_id = rfid
        self.current_position = position
        self.destination = destination            # TODO check all known positions and racks
        self.route_commands = asyncio.Queue()